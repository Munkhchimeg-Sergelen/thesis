#!/usr/bin/env python3
"""
Quick plot of Wav2Vec2 RTF data for MN+HU
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import glob
from pathlib import Path

# Load Wav2Vec2 JSONs only
print("Loading Wav2Vec2 data...")
results = []
for f in glob.glob("results/transcripts/**/wav2vec2/**/*.json", recursive=True):
    try:
        with open(f) as file:
            results.append(json.load(file))
    except: pass

df = pd.DataFrame(results)

print(f"Loaded {len(df)} Wav2Vec2 samples")
print(f"Languages: {df['language_used'].value_counts().to_dict()}")

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Wav2Vec2 Performance Analysis (MN + HU)', fontsize=16, fontweight='bold')

# 1. RTF by Language
ax1 = axes[0, 0]
lang_order = ['hu', 'mn']
df_ordered = df[df['language_used'].isin(lang_order)].copy()
df_ordered['language_used'] = pd.Categorical(df_ordered['language_used'], categories=lang_order, ordered=True)
sns.barplot(data=df_ordered, x='language_used', y='rtf', ax=ax1, errorbar='sd', palette='husl')
ax1.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Real-time threshold')
ax1.set_xlabel('Language', fontsize=12)
ax1.set_ylabel('Real-Time Factor (RTF)', fontsize=12)
ax1.set_title('RTF by Language', fontsize=13, fontweight='bold')
ax1.legend()
ax1.set_xticklabels(['Hungarian', 'Mongolian'])

# 2. Processing Time by Language
ax2 = axes[0, 1]
sns.barplot(data=df_ordered, x='language_used', y='elapsed_sec', ax=ax2, errorbar='sd', palette='husl')
ax2.set_xlabel('Language', fontsize=12)
ax2.set_ylabel('Processing Time (seconds)', fontsize=12)
ax2.set_title('Processing Time by Language', fontsize=13, fontweight='bold')
ax2.set_xticklabels(['Hungarian', 'Mongolian'])

# 3. RTF Distribution
ax3 = axes[1, 0]
for lang in lang_order:
    data = df_ordered[df_ordered['language_used'] == lang]['rtf']
    label = 'Hungarian' if lang == 'hu' else 'Mongolian'
    ax3.hist(data, bins=30, alpha=0.6, label=label)
ax3.axvline(x=1.0, color='red', linestyle='--', linewidth=2, label='Real-time threshold')
ax3.set_xlabel('Real-Time Factor (RTF)', fontsize=12)
ax3.set_ylabel('Frequency', fontsize=12)
ax3.set_title('RTF Distribution', fontsize=13, fontweight='bold')
ax3.legend()

# 4. Audio Duration vs Processing Time
ax4 = axes[1, 1]
for lang in lang_order:
    data = df_ordered[df_ordered['language_used'] == lang]
    label = 'Hungarian' if lang == 'hu' else 'Mongolian'
    ax4.scatter(data['duration_sec'], data['elapsed_sec'], alpha=0.5, label=label, s=20)

# Add diagonal line (y=x, where processing_time = duration_sec, RTF=1.0)
max_val = max(df_ordered['duration_sec'].max(), df_ordered['elapsed_sec'].max())
ax4.plot([0, max_val], [0, max_val], 'r--', linewidth=2, label='RTF = 1.0', alpha=0.7)

ax4.set_xlabel('Audio Duration (seconds)', fontsize=12)
ax4.set_ylabel('Processing Time (seconds)', fontsize=12)
ax4.set_title('Duration vs Processing Time', fontsize=13, fontweight='bold')
ax4.legend()
ax4.grid(alpha=0.3)

plt.tight_layout()

# Save
output_dir = Path("docs/thesis_materials/figures")
output_dir.mkdir(parents=True, exist_ok=True)
plt.savefig(output_dir / 'wav2vec2_rtf_analysis.png', dpi=300, bbox_inches='tight')
plt.savefig(output_dir / 'wav2vec2_rtf_analysis.pdf', bbox_inches='tight')

print(f"\n✓ Saved: {output_dir}/wav2vec2_rtf_analysis.png/pdf")

# Print statistics
print("\n" + "="*60)
print("WAV2VEC2 RTF STATISTICS")
print("="*60)
print("\nRTF by Language:")
print(df.groupby('language_used')['rtf'].describe())
print("\nProcessing Time by Language:")
print(df.groupby('language_used')['elapsed_sec'].describe())
print("\nReal-time capable (RTF < 1.0):")
for lang in df['language_used'].unique():
    total = len(df[df['language_used'] == lang])
    rtf_ok = len(df[(df['language_used'] == lang) & (df['rtf'] < 1.0)])
    print(f"  {lang}: {rtf_ok}/{total} ({100*rtf_ok/total:.1f}%)")
