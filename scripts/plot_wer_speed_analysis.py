#!/usr/bin/env python3
"""
Create comprehensive WER/CER + Speed analysis plots
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load data
wer_summary = pd.read_csv('results/wer_cer_results_summary.csv')
speed_stats = pd.read_csv('results/whisper_omnilingual_statistics.csv')

# Flatten multi-index columns
wer_summary.columns = ['_'.join(col).strip('_') for col in wer_summary.columns]
wer_summary = wer_summary.reset_index()

print("="*60)
print("CREATING WER/CER + SPEED ANALYSIS PLOTS")
print("="*60)

# ============================================================
# PLOT 1: WER by Model and Language
# ============================================================
print("\nGenerating Plot 1: WER by Model and Language...")

fig, ax = plt.subplots(figsize=(14, 8))

models = wer_summary['model'].unique()
languages = wer_summary['language'].unique()
x = np.arange(len(languages))
width = 0.2

for i, model in enumerate(models):
    model_data = wer_summary[wer_summary['model'] == model]
    wer_values = [model_data[model_data['language'] == lang]['wer_mean'].values[0] * 100 
                  for lang in languages]
    ax.bar(x + i*width, wer_values, width, label=model, alpha=0.8)

ax.set_xlabel('Language', fontweight='bold', fontsize=12)
ax.set_ylabel('Word Error Rate (%)', fontweight='bold', fontsize=12)
ax.set_title('Word Error Rate (WER) by Model and Language', fontweight='bold', fontsize=14)
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels([l.upper() for l in languages])
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('results/plot5_wer_by_model_language.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: results/plot5_wer_by_model_language.png")

# ============================================================
# PLOT 2: CER by Model and Language  
# ============================================================
print("\nGenerating Plot 2: CER by Model and Language...")

fig, ax = plt.subplots(figsize=(14, 8))

for i, model in enumerate(models):
    model_data = wer_summary[wer_summary['model'] == model]
    cer_values = [model_data[model_data['language'] == lang]['cer_mean'].values[0] * 100 
                  for lang in languages]
    ax.bar(x + i*width, cer_values, width, label=model, alpha=0.8)

ax.set_xlabel('Language', fontweight='bold', fontsize=12)
ax.set_ylabel('Character Error Rate (%)', fontweight='bold', fontsize=12)
ax.set_title('Character Error Rate (CER) by Model and Language', fontweight='bold', fontsize=14)
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels([l.upper() for l in languages])
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('results/plot6_cer_by_model_language.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: results/plot6_cer_by_model_language.png")

# ============================================================
# PLOT 3: Speed vs Accuracy Tradeoff (RTF vs WER)
# ============================================================
print("\nGenerating Plot 3: Speed vs Accuracy Tradeoff...")

# Merge speed and WER data
speed_stats.columns = speed_stats.columns.str.strip()
merged = pd.merge(
    wer_summary[['model', 'language', 'wer_mean']],
    speed_stats[['model', 'language', 'rtf', 'mean']],
    on=['model', 'language'],
    how='inner'
)

fig, ax = plt.subplots(figsize=(12, 8))

colors = {'mn': 'red', 'hu': 'blue', 'es': 'green', 'fr': 'purple'}
markers = {'Whisper-small': 'o', 'omniASR_CTC_300M': 's', 'omniASR_CTC_1B': '^', 'omniASR_LLM_1B': 'D'}

for model in models:
    for lang in languages:
        data_point = merged[(merged['model'] == model) & (merged['language'] == lang)]
        if not data_point.empty:
            rtf = data_point['rtf'].values[0]
            wer = data_point['wer_mean'].values[0] * 100
            ax.scatter(rtf, wer, s=200, marker=markers[model], 
                      color=colors[lang], alpha=0.7, edgecolors='black', linewidth=1.5,
                      label=f'{model}' if lang == 'mn' else '')

# Add RTF=1.0 line (real-time threshold)
ax.axvline(x=1.0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Real-time (RTF=1.0)')

ax.set_xlabel('Real-Time Factor (RTF, log scale)', fontweight='bold', fontsize=12)
ax.set_ylabel('Word Error Rate (%)', fontweight='bold', fontsize=12)
ax.set_title('Speed vs Accuracy Tradeoff: RTF vs WER', fontweight='bold', fontsize=14)
ax.set_xscale('log')
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3, which='both')

# Add language legend
from matplotlib.patches import Patch
lang_legend = [Patch(facecolor=colors[l], label=l.upper()) for l in languages]
ax.legend(handles=ax.get_legend_handles_labels()[0] + lang_legend, 
          loc='upper right', fontsize=9, ncol=2)

plt.tight_layout()
plt.savefig('results/plot7_speed_vs_accuracy.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: results/plot7_speed_vs_accuracy.png")

# ============================================================
# PLOT 4: Mongolian Focus - Speed AND Accuracy Comparison
# ============================================================
print("\nGenerating Plot 4: Mongolian Detailed Comparison...")

mn_wer = wer_summary[wer_summary['language'] == 'mn'][['model', 'wer_mean']].copy()
mn_speed = speed_stats[speed_stats['language'] == 'mn'][['model', 'rtf', 'mean']].copy()
mn_merged = pd.merge(mn_wer, mn_speed, on='model')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# WER comparison
ax1.bar(range(len(mn_merged)), mn_merged['wer_mean'] * 100, color=['#d62728', '#2ca02c', '#ff7f0e', '#1f77b4'], alpha=0.8)
ax1.set_xticks(range(len(mn_merged)))
ax1.set_xticklabels(mn_merged['model'], rotation=45, ha='right')
ax1.set_ylabel('Word Error Rate (%)', fontweight='bold', fontsize=12)
ax1.set_title('Mongolian WER Comparison', fontweight='bold', fontsize=14)
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels
for i, v in enumerate(mn_merged['wer_mean'] * 100):
    ax1.text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')

# RTF comparison (log scale)
ax2.bar(range(len(mn_merged)), mn_merged['rtf'], color=['#d62728', '#2ca02c', '#ff7f0e', '#1f77b4'], alpha=0.8)
ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Real-time threshold')
ax2.set_xticks(range(len(mn_merged)))
ax2.set_xticklabels(mn_merged['model'], rotation=45, ha='right')
ax2.set_ylabel('Real-Time Factor (RTF, log scale)', fontweight='bold', fontsize=12)
ax2.set_title('Mongolian Speed Comparison', fontweight='bold', fontsize=14)
ax2.set_yscale('log')
ax2.legend()
ax2.grid(True, alpha=0.3, which='both', axis='y')

# Add value labels
for i, v in enumerate(mn_merged['rtf']):
    ax2.text(i, v * 1.3, f'{v:.2f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('results/plot8_mongolian_detailed.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: results/plot8_mongolian_detailed.png")

# ============================================================
# SUMMARY TABLE
# ============================================================
print("\n" + "="*60)
print("PLOT GENERATION COMPLETE")
print("="*60)
print("\nGenerated 4 new plots:")
print("  - plot5_wer_by_model_language.png")
print("  - plot6_cer_by_model_language.png")
print("  - plot7_speed_vs_accuracy.png")
print("  - plot8_mongolian_detailed.png")
print("\nCombine with existing speed plots (plot1-4) for complete analysis!")
