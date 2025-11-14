#!/usr/bin/env python3
"""
Statistical Analysis for Thesis Results
Implements Wilcoxon signed-rank tests and confidence intervals
as recommended by supervisor
"""

import json
import numpy as np
from pathlib import Path
from scipy import stats
from typing import List, Tuple, Dict
import pandas as pd

def load_results(results_dir: str, mode: str) -> Dict[str, List[float]]:
    """Load processing times by language from results"""
    results_path = Path(results_dir) / mode
    times_by_lang = {'es': [], 'fr': [], 'hu': [], 'mn': []}
    
    for json_file in results_path.glob('*.json'):
        try:
            with open(json_file) as f:
                data = json.load(f)
                
            # Extract language from filename
            filename = json_file.stem
            if filename.startswith('es'):
                lang = 'es'
            elif filename.startswith('fr'):
                lang = 'fr'
            elif filename.startswith('hu'):
                lang = 'hu'
            elif filename.startswith('mn'):
                lang = 'mn'
            else:
                continue
            
            # Get processing time
            if 'processing_time' in data:
                times_by_lang[lang].append(data['processing_time'])
                
        except Exception as e:
            print(f"Warning: Could not process {json_file}: {e}")
            continue
    
    return times_by_lang

def wilcoxon_test(group1: List[float], group2: List[float]) -> Tuple[float, float]:
    """
    Perform Wilcoxon signed-rank test
    Returns: (statistic, p-value)
    """
    # Ensure paired samples (same length)
    min_len = min(len(group1), len(group2))
    group1 = group1[:min_len]
    group2 = group2[:min_len]
    
    statistic, p_value = stats.wilcoxon(group1, group2)
    return statistic, p_value

def confidence_interval(data: List[float], confidence=0.95) -> Tuple[float, float, float]:
    """
    Calculate mean and confidence interval
    Returns: (mean, lower_bound, upper_bound)
    """
    data = np.array(data)
    mean = np.mean(data)
    sem = stats.sem(data)  # Standard error of mean
    ci = stats.t.interval(confidence, len(data)-1, loc=mean, scale=sem)
    return mean, ci[0], ci[1]

def cohens_d(group1: List[float], group2: List[float]) -> float:
    """
    Calculate Cohen's d effect size
    """
    group1 = np.array(group1)
    group2 = np.array(group2)
    
    mean_diff = np.mean(group1) - np.mean(group2)
    pooled_std = np.sqrt((np.std(group1, ddof=1)**2 + np.std(group2, ddof=1)**2) / 2)
    
    return mean_diff / pooled_std if pooled_std > 0 else 0

def analyze_lid_vs_hinted(results_dir: str = 'results/transcripts'):
    """Compare LID→ASR vs Language-Hinted modes"""
    print("="*60)
    print("STATISTICAL ANALYSIS: LID→ASR vs Language-Hinted")
    print("="*60)
    
    # Load data
    lid_times = load_results(results_dir, 'lid2asr')
    hinted_times = load_results(results_dir, 'hinted')
    
    print(f"\nSample sizes:")
    for lang in ['es', 'fr', 'hu', 'mn']:
        print(f"  {lang.upper()}: LID={len(lid_times[lang])}, Hinted={len(hinted_times[lang])}")
    
    # Analyze each language
    results = []
    
    for lang in ['es', 'fr', 'hu', 'mn']:
        print(f"\n{'-'*60}")
        print(f"Language: {lang.upper()}")
        print(f"{'-'*60}")
        
        lid = lid_times[lang]
        hinted = hinted_times[lang]
        
        if len(lid) < 2 or len(hinted) < 2:
            print(f"  ⚠️  Insufficient data for {lang.upper()}")
            continue
        
        # Confidence intervals
        lid_mean, lid_lower, lid_upper = confidence_interval(lid)
        hinted_mean, hinted_lower, hinted_upper = confidence_interval(hinted)
        
        print(f"\nLID→ASR:")
        print(f"  Mean: {lid_mean:.2f}s")
        print(f"  95% CI: [{lid_lower:.2f}, {lid_upper:.2f}]")
        
        print(f"\nLanguage-Hinted:")
        print(f"  Mean: {hinted_mean:.2f}s")
        print(f"  95% CI: [{hinted_lower:.2f}, {hinted_upper:.2f}]")
        
        # Speed ratio
        if hinted_mean > 0:
            ratio = hinted_mean / lid_mean
            print(f"\nSpeed Ratio: Hinted is {ratio:.2f}× slower than LID")
        
        # Wilcoxon test
        try:
            statistic, p_value = wilcoxon_test(lid, hinted)
            print(f"\nWilcoxon Signed-Rank Test:")
            print(f"  Statistic: {statistic:.2f}")
            print(f"  P-value: {p_value:.6f}")
            
            if p_value < 0.001:
                print(f"  Result: *** Highly significant (p < 0.001)")
            elif p_value < 0.01:
                print(f"  Result: ** Very significant (p < 0.01)")
            elif p_value < 0.05:
                print(f"  Result: * Significant (p < 0.05)")
            else:
                print(f"  Result: Not significant (p ≥ 0.05)")
        except Exception as e:
            print(f"\n  ⚠️  Could not perform Wilcoxon test: {e}")
        
        # Effect size
        effect_size = cohens_d(lid, hinted)
        print(f"\nEffect Size (Cohen's d): {effect_size:.2f}")
        if abs(effect_size) < 0.2:
            print(f"  Interpretation: Small effect")
        elif abs(effect_size) < 0.5:
            print(f"  Interpretation: Medium effect")
        else:
            print(f"  Interpretation: Large effect")
        
        results.append({
            'language': lang,
            'lid_mean': lid_mean,
            'lid_ci_lower': lid_lower,
            'lid_ci_upper': lid_upper,
            'hinted_mean': hinted_mean,
            'hinted_ci_lower': hinted_lower,
            'hinted_ci_upper': hinted_upper,
            'ratio': ratio if hinted_mean > 0 else None,
            'p_value': p_value if 'p_value' in locals() else None,
            'cohens_d': effect_size
        })
    
    # Save results
    df = pd.DataFrame(results)
    output_path = 'results/statistical_analysis.csv'
    df.to_csv(output_path, index=False)
    print(f"\n{'='*60}")
    print(f"Results saved to: {output_path}")
    print(f"{'='*60}")
    
    return df

def analyze_language_differences(results_dir: str = 'results/transcripts'):
    """Compare processing times across languages"""
    print("\n" + "="*60)
    print("STATISTICAL ANALYSIS: Language Comparison")
    print("="*60)
    
    lid_times = load_results(results_dir, 'lid2asr')
    
    languages = ['es', 'fr', 'hu', 'mn']
    lang_names = {
        'es': 'Spanish',
        'fr': 'French',
        'hu': 'Hungarian',
        'mn': 'Mongolian'
    }
    
    # Compare Mongolian vs others
    print(f"\nComparing Mongolian vs other languages:")
    print(f"{'-'*60}")
    
    mn_times = lid_times['mn']
    
    for lang in ['es', 'fr', 'hu']:
        other_times = lid_times[lang]
        
        if len(mn_times) < 2 or len(other_times) < 2:
            continue
        
        mn_mean, _, _ = confidence_interval(mn_times)
        other_mean, _, _ = confidence_interval(other_times)
        
        print(f"\n{lang_names['mn']} vs {lang_names[lang]}:")
        print(f"  Mongolian: {mn_mean:.2f}s")
        print(f"  {lang_names[lang]}: {other_mean:.2f}s")
        print(f"  Ratio: Mongolian is {mn_mean/other_mean:.2f}× slower")
        
        # Wilcoxon test
        try:
            statistic, p_value = wilcoxon_test(mn_times, other_times)
            print(f"  P-value: {p_value:.6f}")
            if p_value < 0.001:
                print(f"  Result: *** Highly significant")
            elif p_value < 0.05:
                print(f"  Result: * Significant")
        except Exception as e:
            print(f"  ⚠️  Test failed: {e}")

def main():
    """Run complete statistical analysis"""
    print("\n" + "="*60)
    print("THESIS STATISTICAL ANALYSIS")
    print("Wilcoxon Tests & Confidence Intervals")
    print("="*60)
    
    # Check if results exist
    results_path = Path('results/transcripts')
    if not results_path.exists():
        print("\n❌ ERROR: No results found!")
        print(f"Expected directory: {results_path}")
        print("\nRun experiments first:")
        print("  ./scripts/run_comparison_batch.sh")
        return
    
    # Run analyses
    try:
        analyze_lid_vs_hinted()
        analyze_language_differences()
        
        print("\n" + "="*60)
        print("✅ STATISTICAL ANALYSIS COMPLETE!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Review results/statistical_analysis.csv")
        print("  2. Include p-values in thesis")
        print("  3. Report confidence intervals")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
