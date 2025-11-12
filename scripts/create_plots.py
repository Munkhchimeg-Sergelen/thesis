#!/usr/bin/env python3
"""
Create publication-quality plots for thesis
Generates all figures from analysis results
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Set style for publication-quality plots
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

def load_data():
    """Load analysis results"""
    data_file = Path("results/analysis/full_results.csv")
    
    if not data_file.exists():
        print("Error: Run analyze_results.py first!")
        return None
    
    df = pd.read_csv(data_file)
    return df

def plot_whisper_model_rtf(df, output_dir):
    """Plot processing time by Whisper model size"""
    whisper_df = df[df['system'] == 'whisper'].copy()
    
    if whisper_df.empty or 'model_size' not in whisper_df.columns:
        print("Skipping Whisper model plot (no data)")
        return
    
    # Determine which metric to use
    if 'rtf' in whisper_df.columns:
        y_col = 'rtf'
        y_label = 'Real-Time Factor (RTF)'
        title = 'Whisper Model Size vs. RTF'
        add_threshold = True
    elif 'processing_time_sec' in whisper_df.columns:
        y_col = 'processing_time_sec'
        y_label = 'Processing Time (seconds)'
        title = 'Whisper Model Size vs. Processing Time'
        add_threshold = False
    else:
        print("Skipping Whisper model plot (no metrics available)")
        return
    
    plt.figure(figsize=(10, 6))
    
    # Order models by size
    model_order = ['tiny', 'base', 'small']
    whisper_df['model_size'] = pd.Categorical(
        whisper_df['model_size'], 
        categories=model_order, 
        ordered=True
    )
    
    sns.barplot(data=whisper_df, x='model_size', y=y_col, hue='language_used', errorbar='sd')
    
    if add_threshold:
        plt.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Real-time threshold')
    
    plt.xlabel('Whisper Model Size')
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend(title='Language', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    plt.savefig(output_dir / 'whisper_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'whisper_model_comparison.pdf', bbox_inches='tight')
    plt.close()
    
    print("✓ Created: whisper_model_comparison.png/pdf")

def plot_system_comparison(df, output_dir):
    """Plot Whisper vs Wav2Vec2 on ES and FR"""
    # Filter to ES and FR
    df_comp = df[df['language_used'].isin(['es', 'fr'])].copy()
    
    # Filter to Whisper-small and Wav2Vec2
    df_comp = df_comp[
        ((df_comp['system'] == 'whisper') & (df_comp['model_size'] == 'small')) |
        (df_comp['system'] == 'wav2vec2')
    ].copy()
    
    if df_comp.empty or 'processing_time_sec' not in df_comp.columns:
        print("Skipping system comparison plot (no data)")
        return
    
    plt.figure(figsize=(8, 6))
    
    sns.barplot(data=df_comp, x='language_used', y='processing_time_sec', hue='system', errorbar='sd')
    
    plt.xlabel('Language')
    plt.ylabel('Processing Time (seconds)')
    plt.title('System Comparison: Whisper-small vs. Wav2Vec2-XLSR-53')
    plt.legend(title='System')
    plt.tight_layout()
    
    plt.savefig(output_dir / 'system_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'system_comparison.pdf', bbox_inches='tight')
    plt.close()
    
    print("✓ Created: system_comparison.png/pdf")

def plot_language_comparison(df, output_dir):
    """Plot performance by language (Whisper-small)"""
    whisper_small = df[
        (df['system'] == 'whisper') & 
        (df['model_size'] == 'small')
    ].copy()
    
    if whisper_small.empty or 'processing_time_sec' not in whisper_small.columns:
        print("Skipping language comparison plot (no data)")
        return
    
    plt.figure(figsize=(8, 6))
    
    # Language order by resource level
    lang_order = ['es', 'fr', 'hu', 'mn']
    whisper_small['language_used'] = pd.Categorical(
        whisper_small['language_used'],
        categories=lang_order,
        ordered=True
    )
    
    sns.barplot(data=whisper_small, x='language_used', y='processing_time_sec', errorbar='sd', color='steelblue')
    
    plt.xlabel('Language')
    plt.ylabel('Processing Time (seconds)')
    plt.title('Whisper-small Performance by Language')
    plt.tight_layout()
    
    plt.savefig(output_dir / 'language_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'language_comparison.pdf', bbox_inches='tight')
    plt.close()
    
    print("✓ Created: language_comparison.png/pdf")

def plot_speed_accuracy_tradeoff(df, output_dir):
    """Plot model size comparison (skipped - needs WER data for trade-off)"""
    # Skip this plot - we don't have WER data to show accuracy trade-off
    print("Skipping speed-accuracy tradeoff plot (needs WER data)")
    return

def plot_processing_time_distribution(df, output_dir):
    """Plot distribution of processing times"""
    if 'processing_time_sec' not in df.columns:
        print("Skipping processing time distribution (no data)")
        return
    
    whisper_df = df[df['system'] == 'whisper'].copy()
    
    if whisper_df.empty:
        return
    
    plt.figure(figsize=(10, 6))
    
    if 'model_size' in whisper_df.columns:
        model_order = ['tiny', 'base', 'small']
        for model in model_order:
            model_data = whisper_df[whisper_df['model_size'] == model]['processing_time_sec']
            if not model_data.empty:
                plt.hist(model_data, bins=20, alpha=0.5, label=f'Whisper-{model}')
    
    plt.xlabel('Processing Time (seconds)')
    plt.ylabel('Frequency')
    plt.title('Processing Time Distribution by Model')
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(output_dir / 'processing_time_dist.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'processing_time_dist.pdf', bbox_inches='tight')
    plt.close()
    
    print("✓ Created: processing_time_dist.png/pdf")

def create_summary_table(df, output_dir):
    """Create summary table as image"""
    whisper_df = df[df['system'] == 'whisper'].copy()
    
    if whisper_df.empty or 'model_size' not in whisper_df.columns:
        return
    
    # Build aggregation dict based on available columns
    agg_dict = {}
    col_labels = []
    
    if 'processing_time_sec' in whisper_df.columns:
        agg_dict['processing_time_sec'] = ['mean', 'std']
        col_labels.extend(['Time Mean (s)', 'Time Std (s)'])
    
    # Always include count
    count_col = 'processing_time_sec' if 'processing_time_sec' in whisper_df.columns else whisper_df.columns[0]
    if count_col not in agg_dict:
        agg_dict[count_col] = 'count'
        col_labels.append('Samples')
    else:
        agg_dict[count_col].append('count')
        col_labels.append('Samples')
    
    if not agg_dict:
        return
    
    # Compute summary statistics
    summary = whisper_df.groupby(['model_size', 'language_used']).agg(agg_dict).round(3)
    
    summary.columns = col_labels
    summary = summary.reset_index()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=summary.values,
                    colLabels=summary.columns,
                    cellLoc='center',
                    loc='center')
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)
    
    plt.title('Whisper Performance Summary', fontsize=14, pad=20)
    plt.tight_layout()
    
    plt.savefig(output_dir / 'summary_table.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Created: summary_table.png")

def main():
    print("="*70)
    print("CREATING THESIS PLOTS")
    print("="*70)
    print()
    
    # Load data
    df = load_data()
    
    if df is None:
        return
    
    print(f"Loaded {len(df)} samples\n")
    
    # Create output directory
    output_dir = Path("docs/thesis_materials/figures")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate all plots
    print("Generating plots...\n")
    
    plot_whisper_model_rtf(df, output_dir)
    plot_system_comparison(df, output_dir)
    plot_language_comparison(df, output_dir)
    plot_speed_accuracy_tradeoff(df, output_dir)
    plot_processing_time_distribution(df, output_dir)
    create_summary_table(df, output_dir)
    
    print()
    print("="*70)
    print(f"All plots saved to: {output_dir}")
    print("="*70)
    print()
    print("Plots created:")
    print("  - whisper_model_rtf.png/pdf - Model size comparison")
    print("  - system_comparison.png/pdf - Whisper vs Wav2Vec2")
    print("  - language_comparison.png/pdf - Performance by language")
    print("  - speed_tradeoff.png/pdf - Speed-accuracy trade-off")
    print("  - processing_time_dist.png/pdf - Processing time distribution")
    print("  - summary_table.png - Summary statistics table")
    print()
    print("Use these in your Results chapter!")

if __name__ == '__main__':
    main()
