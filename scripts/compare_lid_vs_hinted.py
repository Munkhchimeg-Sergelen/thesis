#!/usr/bin/env python3
"""
Compare LID→ASR vs Language-Hinted ASR approaches
Core analysis for thesis
"""

import json
import glob
from pathlib import Path
import pandas as pd
import numpy as np

def load_all_results(results_dir="results"):
    """Load both hinted and LID results"""
    results = {'hinted': [], 'lid2asr': []}
    
    for mode in ['hinted', 'lid2asr']:
        json_files = glob.glob(f"{results_dir}/transcripts/{mode}/**/*.json", recursive=True)
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data['mode'] = mode
                    data['json_file'] = json_file
                    results[mode].append(data)
            except Exception as e:
                print(f"Warning: Failed to load {json_file}: {e}")
    
    return results

def prepare_dataframe(results):
    """Convert results to DataFrame with consistent fields"""
    all_data = results['hinted'] + results['lid2asr']
    
    if not all_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(all_data)
    
    # Extract model size from system name
    if 'system' in df.columns:
        df['model_size'] = df['system'].str.extract(r'whisper-(tiny|base|small)', expand=False)
        df['system'] = df['system'].str.replace(r'whisper-(tiny|base|small)', 'whisper', regex=True)
    
    # Standardize processing time
    if 'elapsed_sec' in df.columns and 'processing_time_sec' not in df.columns:
        df['processing_time_sec'] = df['elapsed_sec']
    
    return df

def compare_modes(df):
    """Compare hinted vs LID modes"""
    if df.empty or 'mode' not in df.columns:
        return None
    
    # Group by mode, model, and language
    comparison = df.groupby(['mode', 'model_size', 'language_used']).agg({
        'processing_time_sec': ['mean', 'std', 'count']
    }).round(4)
    
    return comparison

def compare_efficiency(df):
    """Compare computational efficiency between modes"""
    if df.empty:
        return None
    
    # Average processing time by mode
    mode_stats = df.groupby('mode').agg({
        'processing_time_sec': ['mean', 'std', 'min', 'max', 'count']
    }).round(4)
    
    # Processing time by mode and model
    if 'model_size' in df.columns:
        model_stats = df.groupby(['mode', 'model_size']).agg({
            'processing_time_sec': ['mean', 'std']
        }).round(4)
    else:
        model_stats = None
    
    return {
        'by_mode': mode_stats,
        'by_model': model_stats
    }

def main():
    print("=" * 70)
    print("COMPARING LID→ASR vs LANGUAGE-HINTED ASR")
    print("=" * 70)
    print()
    
    # Load results
    results = load_all_results()
    
    hinted_count = len(results['hinted'])
    lid_count = len(results['lid2asr'])
    
    print(f"Loaded results:")
    print(f"  - Hinted mode: {hinted_count} samples")
    print(f"  - LID→ASR mode: {lid_count} samples")
    print()
    
    if hinted_count == 0 or lid_count == 0:
        print("ERROR: Missing results for one or both modes!")
        print("Make sure to run both:")
        print("  1. ./scripts/run_full_evaluation.sh (hinted)")
        print("  2. ./scripts/run_lid_evaluation.sh (LID→ASR)")
        return
    
    # Prepare data
    df = prepare_dataframe(results)
    
    # Create output directory
    output_dir = Path("results/analysis")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Compare modes
    print("=" * 70)
    print("PROCESSING TIME COMPARISON")
    print("=" * 70)
    print()
    
    comparison = compare_modes(df)
    if comparison is not None:
        print(comparison)
        print()
        comparison.to_csv(output_dir / "mode_comparison_detailed.csv")
    
    # Efficiency comparison
    efficiency = compare_efficiency(df)
    if efficiency:
        print("=" * 70)
        print("EFFICIENCY BY MODE")
        print("=" * 70)
        print()
        print(efficiency['by_mode'])
        print()
        
        if efficiency['by_model'] is not None:
            print("=" * 70)
            print("EFFICIENCY BY MODE AND MODEL")
            print("=" * 70)
            print()
            print(efficiency['by_model'])
            print()
        
        efficiency['by_mode'].to_csv(output_dir / "mode_comparison_summary.csv")
        if efficiency['by_model'] is not None:
            efficiency['by_model'].to_csv(output_dir / "mode_model_comparison.csv")
    
    # Save full comparison
    df.to_csv(output_dir / "full_comparison_results.csv", index=False)
    
    # Summary report
    with open(output_dir / "mode_comparison_report.txt", "w") as f:
        f.write("=" * 70 + "\n")
        f.write("LID→ASR vs LANGUAGE-HINTED ASR COMPARISON\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Total samples:\n")
        f.write(f"  - Hinted mode: {hinted_count}\n")
        f.write(f"  - LID→ASR mode: {lid_count}\n\n")
        
        if efficiency:
            f.write("Processing Time by Mode:\n")
            f.write(efficiency['by_mode'].to_string() + "\n\n")
            
            if efficiency['by_model'] is not None:
                f.write("Processing Time by Mode and Model:\n")
                f.write(efficiency['by_model'].to_string() + "\n\n")
        
        # Calculate percentage difference
        if efficiency and 'processing_time_sec' in df.columns:
            hinted_mean = df[df['mode'] == 'hinted']['processing_time_sec'].mean()
            lid_mean = df[df['mode'] == 'lid2asr']['processing_time_sec'].mean()
            
            if hinted_mean > 0:
                pct_diff = ((lid_mean - hinted_mean) / hinted_mean) * 100
                f.write(f"LID→ASR is {abs(pct_diff):.1f}% ")
                f.write("slower\n" if pct_diff > 0 else "faster\n")
                f.write(f"than language-hinted ASR\n")
    
    print("=" * 70)
    print("✅ Comparison complete!")
    print("=" * 70)
    print()
    print("Results saved to: results/analysis/")
    print("  - mode_comparison_summary.csv")
    print("  - mode_comparison_detailed.csv")
    print("  - mode_comparison_report.txt")
    print()

if __name__ == "__main__":
    main()
