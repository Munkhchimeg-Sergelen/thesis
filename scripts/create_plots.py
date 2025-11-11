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
    """Plot RTF by Whisper model size"""
    whisper_df = df[df['system'] == 'whisper'].copy()
    
    if whisper_df.empty or 'model_size' not in whisper_df.columns:
        print("Skipping Whisper model RTF plot (no data)")
        return
    
    plt.figure(figsize=(10, 6))
    
    # Order models by size
    model_order = ['tiny', 'base', 'small']
    whisper_df['model_size'] = pd.Categorical(
        whisper_df['model_size'], 
        categories=model_order, 
        ordered=True
    )
    
    sns.barplot(data=whisper_df, x='model_size', y='rtf', hue='language_used', ci='sd')
    
    plt.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Real-time threshold')
    plt.xlabel('Whisper Model Size')
    plt.ylabel('Real-Time Factor (RTF)')
    plt.title('Whisper Model Size vs. Inference Speed')
    plt.legend(title='Language', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    plt.savefig(output_dir / 'whisper_model_rtf.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'whisper_model_rtf.pdf', bbox_inches='tight')
    plt.close()
    
    print("✓ Created: whisper_model_rtf.png/pdf")

def plot_system_comparison(df, output_dir):
    """Plot Whisper vs Wav2Vec2 on ES and FR"""
    # Filter to ES and FR
    df_comp = df[df['language_used'].isin(['es', 'fr'])].copy()
    
    # Filter to Whisper-small and Wav2Vec2
    df_comp = df_comp[
        ((df_comp['system'] == 'whisper') & (df_comp['model_size'] == 'small')) |
        (df_comp['system'] == 'wav2vec2')
    ].copy()
    
    if df_comp.empty:
        print("Skipping system comparison plot (no data)")
        return
    
    plt.figure(figsize=(8, 6))
    
    sns.barplot(data=df_comp, x='language_used', y='rtf', hue='system', ci='sd')
    
    plt.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    plt.xlabel('Language')
    plt.ylabel('Real-Time Factor (RTF)')
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
    
    if whisper_small.empty:
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
    
    sns.barplot(data=whisper_small, x='language_used', y='rtf', ci='sd', color='steelblue')
    
    plt.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, label='Real-time threshold')
    plt.xlabel('Language')
    plt.ylabel('Real-Time Factor (RTF)')
    plt.title('Whisper-small Performance by Language')
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(output_dir / 'language_comparison.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'language_comparison.pdf', bbox_inches='tight')
    plt.close()
    
    print("✓ Created: language_comparison.png/pdf")

def plot_speed_accuracy_tradeoff(df, output_dir):
    """Plot speed vs accuracy trade-off (placeholder - needs WER data)"""
    # This will be populated when WER results are available
    whisper_df = df[df['system'] == 'whisper'].copy()
    
    if whisper_df.empty or 'model_size' not in whisper_df.columns:
        print("Skipping speed-accuracy plot (no data)")
        return
    
    # Group by model size
    model_stats = whisper_df.groupby('model_size').agg({
        'rtf': 'mean',
        'processing_time_sec': 'mean'
    }).reset_index()
    
    if model_stats.empty:
        return
    
    plt.figure(figsize=(8, 6))
    
    model_order = ['tiny', 'base', 'small']
    colors = {'tiny': 'green', 'base': 'orange', 'small': 'blue'}
    
    for _, row in model_stats.iterrows():
        model = row['model_size']
        if model in model_order:
            plt.scatter(row['rtf'], row['processing_time_sec'], 
                       s=200, label=f'Whisper-{model}',
                       color=colors.get(model, 'gray'))
    
    plt.xlabel('Real-Time Factor (RTF) - Lower is Faster')
    plt.ylabel('Processing Time (seconds)')
    plt.title('Model Size Speed Trade-off')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig(output_dir / 'speed_tradeoff.png', dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'speed_tradeoff.pdf', bbox_inches='tight')
    plt.close()
    
    print("✓ Created: speed_tradeoff.png/pdf")

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
    
    # Compute summary statistics
    summary = whisper_df.groupby(['model_size', 'language_used']).agg({
        'rtf': ['mean', 'std'],
        'duration_sec': 'count'
    }).round(3)
    
    summary.columns = ['RTF Mean', 'RTF Std', 'Samples']
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
