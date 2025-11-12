#!/usr/bin/env python3
"""
Analyze ASR evaluation results from JSON files
Generates statistics, comparison tables, and summary reports
"""

import json
import glob
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd

def load_all_results(results_dir="results"):
    """Load all JSON result files"""
    results = []
    
    json_files = glob.glob(f"{results_dir}/**/*.json", recursive=True)
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data['json_file'] = json_file  # Track source
                results.append(data)
        except Exception as e:
            print(f"Warning: Failed to load {json_file}: {e}")
    
    return results

def results_to_dataframe(results):
    """Convert results list to pandas DataFrame"""
    if not results:
        return pd.DataFrame()
    
    df = pd.DataFrame(results)
    
    # Add derived columns
    if 'system' in df.columns:
        # Extract model size from system field (e.g., "whisper-small" -> "small")
        df['model_size'] = df['system'].str.extract(r'whisper-(tiny|base|small)', expand=False)
        # Normalize system names (whisper-small -> whisper)
        df['system'] = df['system'].str.replace(r'whisper-(tiny|base|small)', 'whisper', regex=True)
        df['system'] = df['system'].fillna('whisper')
    elif 'model' in df.columns:
        # Fallback: Extract model name (tiny/base/small) from model field
        df['model_size'] = df['model'].str.extract(r'(tiny|base|small)', expand=False)
    
    # Compute RTF if not present (RTF = processing_time / duration)
    if 'rtf' not in df.columns and 'elapsed_sec' in df.columns and 'duration_sec' in df.columns:
        df['rtf'] = df['elapsed_sec'] / df['duration_sec']
    elif 'rtf' not in df.columns and 'processing_time_sec' in df.columns and 'duration_sec' in df.columns:
        df['rtf'] = df['processing_time_sec'] / df['duration_sec']
    
    # Rename elapsed_sec to processing_time_sec for consistency
    if 'elapsed_sec' in df.columns and 'processing_time_sec' not in df.columns:
        df['processing_time_sec'] = df['elapsed_sec']
    
    return df

def compute_statistics(df, group_by=['system', 'model_size', 'language_used']):
    """Compute statistics grouped by specified columns"""
    if df.empty:
        return None
    
    # Metrics to aggregate
    metrics = ['rtf', 'duration_sec', 'processing_time_sec']
    available_metrics = [m for m in metrics if m in df.columns]
    
    if not available_metrics:
        return None
    
    stats = df.groupby(group_by)[available_metrics].agg(['mean', 'std', 'min', 'max', 'count'])
    stats = stats.round(4)
    
    return stats

def compare_whisper_models(df):
    """Compare Whisper model sizes"""
    whisper_df = df[df['system'] == 'whisper'].copy()
    
    if whisper_df.empty or 'model_size' not in whisper_df.columns:
        return None
    
    # Build aggregation dict based on available columns
    agg_dict = {}
    if 'rtf' in whisper_df.columns:
        agg_dict['rtf'] = ['mean', 'std']
    if 'processing_time_sec' in whisper_df.columns:
        agg_dict['processing_time_sec'] = ['mean', 'std']
    
    if not agg_dict:
        return None
    
    comparison = whisper_df.groupby(['model_size', 'language_used']).agg(agg_dict).round(4)
    
    return comparison

def compare_systems(df):
    """Compare Whisper vs Wav2Vec2 on common languages (ES, FR)"""
    # Filter to languages where both systems exist
    common_langs = ['es', 'fr']
    df_common = df[df['language_used'].isin(common_langs)].copy()
    
    if df_common.empty:
        return None
    
    # For Whisper, use 'small' model for fair comparison
    whisper_small = df_common[
        (df_common['system'] == 'whisper') & 
        (df_common['model_size'] == 'small')
    ]
    wav2vec2 = df_common[df_common['system'] == 'wav2vec2']
    
    # Build aggregation dict based on available columns
    agg_dict = {}
    if 'rtf' in df_common.columns:
        agg_dict['rtf'] = 'mean'
    if 'processing_time_sec' in df_common.columns:
        agg_dict['processing_time_sec'] = 'mean'
    
    if not agg_dict or whisper_small.empty or wav2vec2.empty:
        return None
    
    comparison = pd.concat([
        whisper_small.groupby('language_used').agg(agg_dict).add_suffix('_whisper'),
        wav2vec2.groupby('language_used').agg(agg_dict).add_suffix('_wav2vec2')
    ], axis=1).round(4)
    
    return comparison

def language_analysis(df):
    """Analyze performance by language (Whisper only, all models)"""
    whisper_df = df[df['system'] == 'whisper'].copy()
    
    if whisper_df.empty:
        return None
    
    # Build aggregation dict based on available columns
    agg_dict = {}
    if 'rtf' in whisper_df.columns:
        agg_dict['rtf'] = ['mean', 'std', 'min', 'max']
    if 'processing_time_sec' in whisper_df.columns:
        agg_dict['processing_time_sec'] = ['mean', 'std', 'min', 'max']
    if 'duration_sec' in whisper_df.columns:
        agg_dict['duration_sec'] = ['sum', 'count']
    
    if not agg_dict:
        return None
    
    lang_stats = whisper_df.groupby('language_used').agg(agg_dict).round(4)
    
    return lang_stats

def generate_summary_report(df):
    """Generate text summary report"""
    report = []
    report.append("=" * 70)
    report.append("ASR EVALUATION RESULTS SUMMARY")
    report.append("=" * 70)
    report.append("")
    
    # Overall stats
    total_samples = len(df)
    total_duration = df['duration_sec'].sum() if 'duration_sec' in df.columns else 0
    
    report.append(f"Total samples evaluated: {total_samples}")
    report.append(f"Total audio duration: {total_duration:.2f} seconds ({total_duration/60:.1f} minutes)")
    report.append("")
    
    # Systems
    if 'system' in df.columns:
        systems = df['system'].value_counts()
        report.append("Samples by system:")
        for sys, count in systems.items():
            report.append(f"  - {sys}: {count}")
        report.append("")
    
    # Languages
    if 'language_used' in df.columns:
        languages = df['language_used'].value_counts()
        report.append("Samples by language:")
        for lang, count in languages.items():
            report.append(f"  - {lang}: {count}")
        report.append("")
    
    # Models (Whisper)
    whisper_df = df[df['system'] == 'whisper']
    if not whisper_df.empty and 'model_size' in whisper_df.columns:
        models = whisper_df['model_size'].value_counts()
        report.append("Whisper models:")
        for model, count in models.items():
            report.append(f"  - {model}: {count}")
        report.append("")
    
    # RTF statistics
    if 'rtf' in df.columns:
        report.append(f"Overall RTF statistics:")
        report.append(f"  Mean: {df['rtf'].mean():.4f}")
        report.append(f"  Std:  {df['rtf'].std():.4f}")
        report.append(f"  Min:  {df['rtf'].min():.4f}")
        report.append(f"  Max:  {df['rtf'].max():.4f}")
        report.append("")
        
        # Real-time capable?
        realtime_count = (df['rtf'] < 1.0).sum()
        realtime_pct = (realtime_count / len(df)) * 100
        report.append(f"Real-time capable (RTF < 1.0): {realtime_count}/{len(df)} ({realtime_pct:.1f}%)")
        report.append("")
    
    report.append("=" * 70)
    
    return "\n".join(report)

def main():
    print("Analyzing ASR evaluation results...")
    print()
    
    # Load all results
    results = load_all_results()
    
    if not results:
        print("No results found! Have you run the evaluation yet?")
        print("Run: ./scripts/run_full_evaluation.sh")
        return
    
    print(f"Loaded {len(results)} result files")
    print()
    
    # Convert to DataFrame
    df = results_to_dataframe(results)
    
    # Generate summary report
    summary = generate_summary_report(df)
    print(summary)
    print()
    
    # Save summary to file
    output_dir = Path("results/analysis")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "summary.txt", 'w') as f:
        f.write(summary)
    print(f"Saved: results/analysis/summary.txt")
    
    # Overall statistics
    print("\n" + "="*70)
    print("DETAILED STATISTICS")
    print("="*70 + "\n")
    
    overall_stats = compute_statistics(df)
    if overall_stats is not None:
        print("Overall statistics by system, model, and language:")
        print(overall_stats)
        print()
        overall_stats.to_csv(output_dir / "overall_statistics.csv")
        print(f"Saved: results/analysis/overall_statistics.csv")
    
    # Whisper model comparison
    whisper_comp = compare_whisper_models(df)
    if whisper_comp is not None:
        print("\n" + "="*70)
        print("WHISPER MODEL SIZE COMPARISON")
        print("="*70 + "\n")
        print(whisper_comp)
        print()
        whisper_comp.to_csv(output_dir / "whisper_model_comparison.csv")
        print(f"Saved: results/analysis/whisper_model_comparison.csv")
    
    # System comparison (Whisper vs Wav2Vec2)
    system_comp = compare_systems(df)
    if system_comp is not None:
        print("\n" + "="*70)
        print("SYSTEM COMPARISON (Whisper-small vs Wav2Vec2)")
        print("="*70 + "\n")
        print(system_comp)
        print()
        system_comp.to_csv(output_dir / "system_comparison.csv")
        print(f"Saved: results/analysis/system_comparison.csv")
    
    # Language analysis
    lang_analysis_result = language_analysis(df)
    if lang_analysis_result is not None:
        print("\n" + "="*70)
        print("LANGUAGE ANALYSIS (Whisper all models)")
        print("="*70 + "\n")
        print(lang_analysis_result)
        print()
        lang_analysis_result.to_csv(output_dir / "language_analysis.csv")
        print(f"Saved: results/analysis/language_analysis.csv")
    
    # Save full dataframe
    df.to_csv(output_dir / "full_results.csv", index=False)
    print(f"\nSaved: results/analysis/full_results.csv")
    
    print("\n" + "="*70)
    print("Analysis complete! Check results/analysis/ for outputs")
    print("="*70)

if __name__ == '__main__':
    main()
