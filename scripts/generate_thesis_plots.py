import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from pathlib import Path
import numpy as np
import os

def setup_thesis_style():
    """Set up publication-quality plot styling"""
    plt.rcParams.update({
        'figure.figsize': (10, 6),
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'figure.autolayout': True,
        'axes.grid': True,
        'grid.alpha': 0.3
    })
    sns.set_theme(style="whitegrid")

def create_thesis_plots():
    """Generate all plots for thesis"""
    # Create output directory
    out_dir = Path('thesis_plots')
    out_dir.mkdir(exist_ok=True)
    
    # Set up style
    setup_thesis_style()
    
    # 1. WER/CER Analysis
    plot_performance_metrics(out_dir)
    
    # 2. Audio Duration Analysis
    plot_duration_analysis(out_dir)
    
    # 3. Resource Usage
    plot_resource_usage(out_dir)
    
    # 4. Error Analysis
    plot_error_analysis(out_dir)

def plot_performance_metrics(out_dir):
    """Plot WER/CER metrics"""
    print("Generating performance metrics plots...")
    # Read results
    df = pd.read_csv('results/wer_cer_results_summary.csv', skiprows=2)
    df.columns = ['model', 'language', 'wer_mean', 'wer_std', 'wer_min', 'wer_max',
                  'cer_mean', 'cer_std', 'cer_min', 'cer_max']
    
    # WER by Model and Language
    plt.figure(figsize=(12, 6))
    g = sns.barplot(data=df, x='language', y='wer_mean', hue='model')
    plt.title('Word Error Rate by Model and Language')
    plt.ylabel('WER (%)')
    plt.xlabel('Language')
    g.legend(title='Model', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(out_dir / '01_wer_by_model_language.png')
    plt.close()
    
    # CER Comparison
    plt.figure(figsize=(12, 6))
    g = sns.barplot(data=df, x='language', y='cer_mean', hue='model')
    plt.title('Character Error Rate by Model and Language')
    plt.ylabel('CER (%)')
    plt.xlabel('Language')
    g.legend(title='Model', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(out_dir / '02_cer_by_model_language.png')
    plt.close()
    
    # Error Distribution
    plt.figure(figsize=(15, 6))
    df_melted = pd.melt(df, 
                        id_vars=['model', 'language'],
                        value_vars=['wer_mean', 'cer_mean'],
                        var_name='metric', value_name='error_rate')
    sns.boxplot(data=df_melted, x='model', y='error_rate', hue='metric')
    plt.title('Error Rate Distribution by Model')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_dir / '03_error_distribution.png')
    plt.close()
    print("✓ Generated performance plots")

def plot_duration_analysis(out_dir):
    """Plot audio duration analysis"""
    print("Generating duration analysis plots...")
    durations = []
    languages = ['mn', 'hu', 'es', 'fr']
    
    # Collect durations using ffprobe
    for lang in languages:
        lang_durations = []
        wav_dir = Path(f'data/wav/{lang}')
        for audio_file in wav_dir.glob('*.mp3'):
            cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {audio_file}"
            try:
                duration = float(os.popen(cmd).read().strip())
                lang_durations.append({'language': lang, 'duration': duration, 'file': audio_file.name})
            except:
                print(f"Warning: Could not get duration for {audio_file}")
        durations.extend(lang_durations)
    
    # Convert to DataFrame
    df_duration = pd.DataFrame(durations)
    
    # 1. Duration Distribution by Language
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_duration, x='language', y='duration')
    plt.title('Audio Duration Distribution by Language')
    plt.ylabel('Duration (seconds)')
    plt.xlabel('Language')
    plt.tight_layout()
    plt.savefig(out_dir / '04_duration_distribution.png')
    plt.close()
    
    # 2. Duration Histogram
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df_duration, x='duration', hue='language', multiple="stack", bins=30)
    plt.title('Audio Duration Distribution')
    plt.xlabel('Duration (seconds)')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(out_dir / '05_duration_histogram.png')
    plt.close()
    
    # 3. Duration Categories
    df_duration['duration_bucket'] = pd.cut(df_duration['duration'], 
                                          bins=[0, 5, 10, 15, 20, float('inf')],
                                          labels=['0-5s', '5-10s', '10-15s', '15-20s', '20s+'])
    
    plt.figure(figsize=(15, 6))
    sns.boxplot(data=df_duration, x='duration_bucket', y='duration', hue='language')
    plt.title('Audio Duration Distribution by Length Category')
    plt.xlabel('Duration Category')
    plt.ylabel('Duration (seconds)')
    plt.tight_layout()
    plt.savefig(out_dir / '06_duration_categories.png')
    plt.close()
    print("✓ Generated duration analysis plots")

def plot_resource_usage(out_dir):
    """Plot resource usage metrics"""
    print("Generating resource usage plots...")
    
    # Load WER results for model information
    df_wer = pd.read_csv('results/wer_cer_results_summary.csv', skiprows=2)
    df_wer.columns = ['model', 'language', 'wer_mean', 'wer_std', 'wer_min', 'wer_max',
                      'cer_mean', 'cer_std', 'cer_min', 'cer_max']
    
    # Calculate RTF from our quick test results
    rtf_data = {
        'model': ['Whisper-small']*4 + ['OmniLingual']*4,
        'language': ['mn', 'hu', 'es', 'fr']*2,
        'rtf': [
            43.28/6.156,  # MN avg_time/avg_duration
            4.16/5.2,     # HU
            3.86/4.8,     # ES
            3.87/4.5,     # FR
            4.49/6.156,   # MN (OmniLingual)
            4.13/5.2,     # HU
            3.98/4.8,     # ES
            3.83/4.5      # FR
        ]
    }
    df_rtf = pd.DataFrame(rtf_data)
    
    # 1. RTF by Model and Language
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_rtf, x='language', y='rtf', hue='model')
    plt.title('Real-Time Factor by Model and Language')
    plt.ylabel('RTF (processing_time/audio_duration)')
    plt.xlabel('Language')
    plt.legend(title='Model', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(out_dir / '07_rtf_by_model_language.png')
    plt.close()
    
    # 2. Speed vs Accuracy Trade-off
    df_combined = pd.merge(df_rtf, df_wer, on=['model', 'language'])
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df_combined, x='rtf', y='wer_mean', hue='model', 
                    style='language', s=100)
    plt.title('Speed vs Accuracy Trade-off')
    plt.xlabel('Real-Time Factor (RTF)')
    plt.ylabel('Word Error Rate (%)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(out_dir / '08_speed_accuracy_tradeoff.png')
    plt.close()
    print("✓ Generated resource usage plots")

def plot_error_analysis(out_dir):
    """Plot error analysis"""
    print("\nStarting error analysis plots...")
    
    # Load results
    print("Loading data...")
    df = pd.read_csv('results/wer_cer_results_summary.csv', skiprows=2)
    df.columns = ['model', 'language', 'wer_mean', 'wer_std', 'wer_min', 'wer_max',
                  'cer_mean', 'cer_std', 'cer_min', 'cer_max']
    print("Data loaded, shape:", df.shape)
    
    # 1. Error Range Analysis
    print("Generating WER range plot...")
    plt.figure(figsize=(12, 6))
    df_melted = pd.melt(df, 
                        id_vars=['model', 'language'],
                        value_vars=['wer_min', 'wer_mean', 'wer_max'],
                        var_name='metric', value_name='value')
    sns.lineplot(data=df_melted, x='language', y='value', hue='model', 
                style='metric', markers=True, dashes=False)
    plt.title('WER Range by Model and Language')
    plt.ylabel('Word Error Rate (%)')
    plt.xlabel('Language')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(out_dir / '09_wer_range_analysis.png')
    plt.close()
    print("✓ Generated WER range plot")
    
    # 2. Error Variability
    print("Generating error variability plot...")
    plt.figure(figsize=(12, 6))
    df_std = df.melt(id_vars=['model', 'language'],
                     value_vars=['wer_std', 'cer_std'],
                     var_name='metric', value_name='std')
    sns.barplot(data=df_std, x='language', y='std', hue='model')
    plt.title('Error Rate Variability by Model and Language')
    plt.ylabel('Standard Deviation')
    plt.xlabel('Language')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(out_dir / '10_error_variability.png')
    plt.close()
    print("✓ Generated error variability plot")
    
    # 3. WER/CER Correlation
    print("Generating WER/CER correlation plot...")
    plt.figure(figsize=(10, 10))
    sns.scatterplot(data=df, x='wer_mean', y='cer_mean', hue='model', 
                    style='language', s=100)
    plt.title('WER vs CER Correlation')
    plt.xlabel('Word Error Rate (%)')
    plt.ylabel('Character Error Rate (%)')
    for _, row in df.iterrows():
        plt.annotate(f"{row['language']}", 
                    (row['wer_mean'], row['cer_mean']),
                    xytext=(5, 5), textcoords='offset points')
    plt.tight_layout()
    plt.savefig(out_dir / '11_wer_cer_correlation.png')
    plt.close()
    print("✓ Generated WER/CER correlation plot")
    
    # 4. Performance Distribution
    print("Generating performance distribution plot...")
    plt.figure(figsize=(15, 6))
    metrics = ['wer_mean', 'wer_std', 'cer_mean', 'cer_std']
    df_metrics = df.melt(id_vars=['model', 'language'],
                        value_vars=metrics,
                        var_name='metric', value_name='value')
    sns.violinplot(data=df_metrics, x='model', y='value', hue='metric')
    plt.title('Performance Distribution by Model')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_dir / '12_performance_distribution.png')
    plt.close()
    print("✓ Generated performance distribution plot")
    
    print("✓ All error analysis plots generated")

if __name__ == '__main__':
    create_thesis_plots()


