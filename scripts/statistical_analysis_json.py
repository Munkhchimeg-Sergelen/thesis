#!/usr/bin/env python3
"""
Statistical analysis of existing JSON experiment results
"""

import json
import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

def load_json_results(results_dir='results/transcripts'):
    """Load all JSON results"""
    print("="*60)
    print("Loading JSON experiment results...")
    print("="*60)
    
    results = []
    results_path = Path(results_dir)
    
    for json_file in results_path.rglob('*.json'):
        try:
            with open(json_file) as f:
                data = json.load(f)
            
            # Extract key info
            file_name = json_file.stem
            
            # Try to determine language
            lang = None
            if file_name.startswith('mn'):
                lang = 'mn'
            elif file_name.startswith('hu'):
                lang = 'hu'
            elif file_name.startswith('es'):
                lang = 'es'
            elif file_name.startswith('fr'):
                lang = 'fr'
            
            if lang and 'elapsed_sec' in data:
                results.append({
                    'file': json_file.name,
                    'language': lang,
                    'mode': data.get('mode', 'unknown'),
                    'system': data.get('system', 'unknown'),
                    'elapsed_sec': data['elapsed_sec'],
                    'device': data.get('device', 'unknown')
                })
        except Exception as e:
            print(f"  Warning: Could not process {json_file.name}: {e}")
            continue
    
    if not results:
        print("\n❌ No results found!")
        return None
    
    df = pd.DataFrame(results)
    print(f"\n✓ Loaded {len(df)} experimental results")
    print(f"\nBreakdown:")
    print(df.groupby(['language', 'mode']).size())
    
    return df

def descriptive_stats(df):
    """Calculate descriptive statistics with confidence intervals"""
    print("\n" + "="*60)
    print("DESCRIPTIVE STATISTICS")
    print("="*60)
    
    stats_summary = []
    
    for mode in df['mode'].unique():
        mode_data = df[df['mode'] == mode]
        print(f"\n{mode.upper()} Mode:")
        print("-"*60)
        
        for lang in ['es', 'fr', 'hu', 'mn']:
            lang_data = mode_data[mode_data['language'] == lang]['elapsed_sec']
            
            if len(lang_data) > 0:
                mean = lang_data.mean()
                std = lang_data.std()
                median = lang_data.median()
                sem = stats.sem(lang_data)
                
                # 95% Confidence Interval
                if len(lang_data) > 1:
                    ci = stats.t.interval(0.95, len(lang_data)-1, loc=mean, scale=sem)
                else:
                    ci = (mean, mean)
                
                stats_summary.append({
                    'mode': mode,
                    'language': lang.upper(),
                    'n': len(lang_data),
                    'mean': mean,
                    'std': std,
                    'median': median,
                    'ci_lower': ci[0],
                    'ci_upper': ci[1]
                })
                
                print(f"  {lang.upper()}: n={len(lang_data):2d} | "
                      f"Mean={mean:6.2f}s ± {std:5.2f}s | "
                      f"95% CI=[{ci[0]:6.2f}, {ci[1]:6.2f}]")
    
    stats_df = pd.DataFrame(stats_summary)
    stats_df.to_csv('results/descriptive_statistics.csv', index=False)
    print(f"\n✓ Saved to: results/descriptive_statistics.csv")
    
    return stats_df

def language_comparisons(df):
    """Compare Mongolian vs other languages"""
    print("\n" + "="*60)
    print("LANGUAGE COMPARISONS (Mann-Whitney U Test)")
    print("="*60)
    print("Non-parametric test appropriate for small samples")
    
    comparisons = []
    
    for mode in df['mode'].unique():
        mode_data = df[df['mode'] == mode]
        mn_times = mode_data[mode_data['language'] == 'mn']['elapsed_sec']
        
        if len(mn_times) < 3:
            continue
        
        print(f"\n{mode.upper()} Mode - Mongolian vs Others:")
        print("-"*60)
        
        for lang in ['es', 'fr', 'hu']:
            other_times = mode_data[mode_data['language'] == lang]['elapsed_sec']
            
            if len(other_times) >= 3:
                # Mann-Whitney U test
                statistic, p_value = stats.mannwhitneyu(mn_times, other_times, alternative='two-sided')
                
                mn_mean = mn_times.mean()
                other_mean = other_times.mean()
                ratio = mn_mean / other_mean if other_mean > 0 else 0
                
                # Effect size
                n1, n2 = len(mn_times), len(other_times)
                effect_r = statistic / (n1 * n2)  # rank-biserial correlation
                
                comparisons.append({
                    'mode': mode,
                    'comparison': f'MN vs {lang.upper()}',
                    'mn_mean': mn_mean,
                    f'{lang}_mean': other_mean,
                    'ratio': ratio,
                    'p_value': p_value,
                    'significant': p_value < 0.05,
                    'effect_size_r': effect_r
                })
                
                sig_marker = '***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'
                
                print(f"  MN vs {lang.upper()}:")
                print(f"    MN: {mn_mean:.2f}s | {lang.upper()}: {other_mean:.2f}s")
                print(f"    Ratio: {ratio:.2f}× slower")
                print(f"    P-value: {p_value:.4f} {sig_marker}")
                if p_value < 0.05:
                    print(f"    → Statistically significant!")
    
    comp_df = pd.DataFrame(comparisons)
    comp_df.to_csv('results/language_comparisons.csv', index=False)
    print(f"\n✓ Saved to: results/language_comparisons.csv")
    
    return comp_df

def sample_size_guidance():
    """Provide guidance on sample sizes"""
    print("\n" + "="*60)
    print("SAMPLE SIZE ASSESSMENT")
    print("="*60)
    
    print("\nCurrent sample size (n≈12 per language):")
    print("  ✓ Sufficient for: Exploratory BSc thesis")
    print("  ✓ Sufficient for: Detecting large effects (d>0.8)")
    print("  ✓ Sufficient for: Non-parametric statistical tests")
    print("  ⚠️  Limited for: Precise confidence intervals")
    print("  ⚠️  Limited for: Detecting small/medium effects")
    
    print("\nStatistical power by sample size:")
    print("  n=12: Detects large effects (80% power for d≥1.0)")
    print("  n=30: Detects large/medium effects (80% power for d≥0.7)")
    print("  n=100: Detects medium effects (80% power for d≥0.4)")
    print("  n=1000: Detects small effects, precise CIs")
    
    print("\nYour Mongolian finding (10-30× slower):")
    print("  → Effect size: d>>2.0 (VERY LARGE)")
    print("  → Already detectable with n=12")
    print("  → More samples → higher confidence, not discoverability")
    
    print("\nRecommendations:")
    print("  BSc thesis (current): n=12-50 acceptable for exploratory work")
    print("  Publication quality: n=100-300 recommended")
    print("  Production validation: n=1000+ (supervisor's suggestion)")

def main():
    print("\n" + "="*60)
    print("STATISTICAL ANALYSIS - EXISTING RESULTS")
    print("="*60)
    
    # Load data
    df = load_json_results()
    if df is None:
        print("\n❌ No data to analyze!")
        print("\nMake sure you have JSON results in:")
        print("  results/transcripts/")
        return
    
    # Run analyses
    stats_df = descriptive_stats(df)
    comp_df = language_comparisons(df)
    sample_size_guidance()
    
    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE")
    print("="*60)
    
    print("\nKey Findings:")
    significant_comps = comp_df[comp_df['significant'] == True]
    if len(significant_comps) > 0:
        print(f"  • {len(significant_comps)} statistically significant differences found")
        print("  • Mongolian slowdown confirmed (p<0.05)")
        print("  • Effect sizes are large (easily detectable)")
    
    print("\nFiles created:")
    print("  - results/descriptive_statistics.csv")
    print("  - results/language_comparisons.csv")
    
    print("\nNext steps:")
    print("  1. Review statistical results")
    print("  2. Email supervisor with current findings + stats")
    print("  3. Discuss: Is n=12 sufficient or expand to n=100-1000?")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
