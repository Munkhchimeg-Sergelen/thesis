#!/usr/bin/env python3
"""
Compare Whisper vs OmniLingual models
Analyze RTF, processing times, and generate comparison plots
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

def load_results(base_dir, system, model, languages):
    """Load all JSON results for a system/model"""
    results = []
    
    for lang in languages:
        result_dir = Path(base_dir) / system / model / lang
        if not result_dir.exists():
            print(f"⚠️  Directory not found: {result_dir}")
            continue
        
        json_files = list(result_dir.glob("*.json"))
        print(f"  {system}/{model}/{lang}: {len(json_files)} files")
        
        for json_file in json_files:
            try:
                with open(json_file) as f:
                    data = json.load(f)
                    # Handle both 'processing_time_sec' (OmniLingual) and 'elapsed_sec' (Whisper)
                    proc_time = data.get('processing_time_sec') or data.get('elapsed_sec', 0)
                    results.append({
                        'system': system,
                        'model': model,
                        'language': lang,
                        'file': data.get('file', json_file.name),
                        'duration_sec': data.get('duration_sec', 0),
                        'processing_time_sec': proc_time,
                        'rtf': data.get('rtf', 0),
                        'transcript': data.get('transcript', '')
                    })
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
    
    return pd.DataFrame(results)

def main():
    base_dir = Path("results/transcripts/hinted")
    languages = ['mn', 'hu', 'es', 'fr']
    
    print("="*60)
    print("WHISPER vs OMNILINGUAL COMPARISON")
    print("="*60)
    print("\nLoading results...")
    
    # Load all results
    all_results = []
    
    # Whisper
    print("\nWhisper-small:")
    df_whisper = load_results(base_dir, "whisper-small", "", languages)
    if not df_whisper.empty:
        df_whisper['model'] = 'Whisper-small'
        all_results.append(df_whisper)
    
    # OmniLingual models
    omni_models = ['omniASR_CTC_300M', 'omniASR_CTC_1B', 'omniASR_LLM_1B']
    for model in omni_models:
        print(f"\n{model}:")
        df = load_results(base_dir, "omnilingual", model, languages)
        if not df.empty:
            df['model'] = model
            all_results.append(df)
    
    if not all_results:
        print("❌ No results found!")
        return
    
    # Combine all results
    df = pd.concat(all_results, ignore_index=True)
    
    print(f"\n✓ Loaded {len(df)} total results")
    print(f"\nDataset summary:")
    print(df.groupby(['model', 'language']).size().unstack(fill_value=0))
    
    # Calculate statistics
    print("\n" + "="*60)
    print("PERFORMANCE STATISTICS")
    print("="*60)
    
    stats = df.groupby(['model', 'language']).agg({
        'rtf': ['mean', 'std', 'median'],
        'processing_time_sec': ['mean', 'std'],
        'duration_sec': 'mean'
    }).round(4)
    
    print("\n" + stats.to_string())
    
    # Overall statistics
    print("\n" + "="*60)
    print("OVERALL MODEL PERFORMANCE")
    print("="*60)
    
    overall = df.groupby('model').agg({
        'rtf': ['mean', 'std', 'median'],
        'processing_time_sec': ['mean', 'median'],
    }).round(4)
    
    print("\n" + overall.to_string())
    
    # Create visualizations
    print("\n" + "="*60)
    print("GENERATING PLOTS")
    print("="*60)
    
    # Create separate plots for better visibility
    
    # PLOT 1: RTF by Model and Language
    print("\n1. Creating RTF by Language plot...")
    fig1, ax1 = plt.subplots(1, 1, figsize=(12, 7))
    df_pivot = df.pivot_table(values='rtf', index='language', columns='model', aggfunc='mean')
    df_pivot.plot(kind='bar', ax=ax1, width=0.8)
    ax1.set_title('Real-Time Factor (RTF) by Model and Language\n(Lower is Better)', 
                  fontweight='bold', fontsize=14)
    ax1.set_xlabel('Language', fontweight='bold', fontsize=12)
    ax1.set_ylabel('RTF (processing_time / audio_duration)', fontweight='bold', fontsize=12)
    ax1.legend(title='Model', fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.axhline(y=1.0, color='r', linestyle='--', alpha=0.7, linewidth=2, label='Real-time threshold')
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    output1 = "results/plot1_rtf_by_language.png"
    plt.savefig(output1, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output1}")
    plt.savefig(output1.replace('.png', '.pdf'), bbox_inches='tight')
    plt.close()
    
    # PLOT 2: Average Processing Time (Simple Bar Chart)
    print("2. Creating Average Processing Time plot...")
    fig2, ax2 = plt.subplots(1, 1, figsize=(12, 7))
    
    # Calculate mean processing time per model
    model_stats = df.groupby('model')['processing_time_sec'].agg(['mean', 'std']).sort_values('mean')
    
    # Create bar chart
    bars = ax2.bar(range(len(model_stats)), model_stats['mean'], 
                   yerr=model_stats['std'], capsize=5, alpha=0.8, 
                   color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    ax2.set_title('Average Processing Time by Model', fontweight='bold', fontsize=14)
    ax2.set_xlabel('Model', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Processing Time (seconds, log scale)', fontweight='bold', fontsize=12)
    ax2.set_yscale('log')
    ax2.set_xticks(range(len(model_stats)))
    ax2.set_xticklabels(model_stats.index, rotation=45, ha='right', fontsize=10)
    ax2.grid(True, alpha=0.3, which='both', axis='y')
    
    # Add value labels on bars
    for i, (idx, row) in enumerate(model_stats.iterrows()):
        ax2.text(i, row['mean'], f'{row["mean"]:.2f}s', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    output2 = "results/plot2_processing_time_avg.png"
    plt.savefig(output2, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {output2}")
    plt.savefig(output2.replace('.png', '.pdf'), bbox_inches='tight')
    plt.close()
    
    # PLOT 3: RTF Distribution by Model (Box Plot)
    print("3. Creating RTF Distribution box plot...")
    fig3, ax3 = plt.subplots(1, 1, figsize=(12, 7))
    df.boxplot(column='rtf', by='model', ax=ax3)
    ax3.set_title('RTF Distribution by Model\n(Log Scale)', fontweight='bold', fontsize=14)
    ax3.set_xlabel('Model', fontweight='bold', fontsize=12)
    ax3.set_ylabel('RTF (log scale)', fontweight='bold', fontsize=12)
    ax3.set_yscale('log')
    ax3.get_figure().suptitle('')  # Remove auto title
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=10)
    ax3.grid(True, alpha=0.3, which='both', axis='y')
    
    plt.tight_layout()
    output3 = "results/plot3_rtf_distribution_boxplot.png"
    plt.savefig(output3, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output3}")
    plt.savefig(output3.replace('.png', '.pdf'), bbox_inches='tight')
    plt.close()
    
    # PLOT 4: Language Comparison
    print("4. Creating Language Comparison plot...")
    fig4, ax4 = plt.subplots(1, 1, figsize=(12, 7))
    
    # Create language comparison
    lang_data = []
    lang_labels = []
    for lang in languages:
        lang_df = df[df['language'] == lang]
        if not lang_df.empty:
            lang_data.append(lang_df['rtf'].values)
            lang_labels.append(lang.upper())
    
    parts = ax4.violinplot(lang_data, positions=range(len(lang_labels)), 
                           showmeans=True, showmedians=True, widths=0.7)
    ax4.set_title('RTF Distribution by Language (All Models)', fontweight='bold', fontsize=14)
    ax4.set_xlabel('Language', fontweight='bold', fontsize=12)
    ax4.set_ylabel('RTF', fontweight='bold', fontsize=12)
    ax4.set_xticks(range(len(lang_labels)))
    ax4.set_xticklabels(lang_labels, fontsize=11)
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output4 = "results/plot4_rtf_by_language_violin.png"
    plt.savefig(output4, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output4}")
    plt.savefig(output4.replace('.png', '.pdf'), bbox_inches='tight')
    plt.close()
    
    # Additional: Speed comparison chart (Log Scale)
    fig2, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    model_stats = df.groupby('model').agg({
        'rtf': 'mean',
        'processing_time_sec': 'mean'
    }).sort_values('rtf')
    
    x = np.arange(len(model_stats))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, model_stats['rtf'], width, label='RTF', alpha=0.8)
    bars2 = ax.bar(x + width/2, model_stats['processing_time_sec'], width, 
           label='Avg Processing Time (s)', alpha=0.8)
    
    # Add value labels on bars
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        ax.text(bar1.get_x() + bar1.get_width()/2., height1,
                f'{height1:.3f}', ha='center', va='bottom', fontsize=8)
        ax.text(bar2.get_x() + bar2.get_width()/2., height2,
                f'{height2:.2f}', ha='center', va='bottom', fontsize=8)
    
    ax.set_xlabel('Model', fontweight='bold')
    ax.set_ylabel('Value (Log Scale)', fontweight='bold')
    ax.set_title('Model Speed Comparison\n(RTF and Average Processing Time - Log Scale)', 
                 fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(model_stats.index, rotation=45, ha='right')
    ax.set_yscale('log')  # Log scale for better visibility
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y', which='both')
    
    plt.tight_layout()
    
    output_file2 = "results/model_speed_comparison.png"
    plt.savefig(output_file2, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file2}")
    plt.savefig(output_file2.replace('.png', '.pdf'), bbox_inches='tight')
    print(f"✓ Saved: {output_file2.replace('.png', '.pdf')}")
    
    # Save statistics to CSV
    csv_file = "results/whisper_omnilingual_statistics.csv"
    stats.to_csv(csv_file)
    print(f"✓ Saved: {csv_file}")
    
    overall_csv = "results/whisper_omnilingual_overall.csv"
    overall.to_csv(overall_csv)
    print(f"✓ Saved: {overall_csv}")
    
    print("\n" + "="*60)
    print("✅ Analysis Complete!")
    print("="*60)
    print(f"\nGenerated 4 separate plots:")
    print(f"  - {output1} (and PDF)")
    print(f"  - {output2} (and PDF)")
    print(f"  - {output3} (and PDF)")
    print(f"  - {output4} (and PDF)")
    print(f"  - {output_file2} (and PDF)")
    print(f"\nGenerated statistics:")
    print(f"  - {csv_file}")
    print(f"  - {overall_csv}")

if __name__ == '__main__':
    main()
