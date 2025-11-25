#!/usr/bin/env python3
"""Analyze full beam comparison results (1000 files per language)"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy import stats

# Read results
results_dir = Path("results/beam_comparison")
languages = ["mn", "hu", "es", "fr"]
lang_names = ["Mongolian", "Hungarian", "Spanish", "French"]

data = {}
for lang in languages:
    data[lang] = {}
    for beam in [1, 5]:
        file = results_dir / f"{lang}_beam{beam}.txt"
        if file.exists():
            df = pd.read_csv(file, header=None, names=['file', 'time'])
            # Remove summary line
            df = df[df['file'] != 'SUMMARY']
            df['time'] = pd.to_numeric(df['time'], errors='coerce')
            data[lang][beam] = df['time'].dropna()

# Calculate statistics
results = []
for lang, name in zip(languages, lang_names):
    if 1 in data[lang] and 5 in data[lang]:
        greedy = data[lang][1]
        beam = data[lang][5]
        
        # Statistics
        greedy_mean = greedy.mean()
        beam_mean = beam.mean()
        speedup_pct = (beam_mean - greedy_mean) / beam_mean * 100
        
        # T-test for statistical significance
        t_stat, p_value = stats.ttest_ind(greedy, beam)
        
        results.append({
            'Language': name,
            'Code': lang.upper(),
            'Greedy Mean (s)': greedy_mean,
            'Greedy Std (s)': greedy.std(),
            'Beam Mean (s)': beam_mean,
            'Beam Std (s)': beam.std(),
            'Speedup (%)': speedup_pct,
            'p-value': p_value,
            'Significant': 'Yes' if p_value < 0.05 else 'No',
            'N': len(greedy)
        })

df_results = pd.DataFrame(results)

# Save results
df_results.to_csv(results_dir / 'full_comparison_summary.csv', index=False)

# Print results
print("=" * 80)
print("FULL BEAM COMPARISON RESULTS (N=1000 per language)")
print("=" * 80)
print()
print(df_results.to_string(index=False))
print()
print(f"Average Speedup: {df_results['Speedup (%)'].mean():.2f}%")
print(f"Greedy faster in: {(df_results['Speedup (%)'] > 0).sum()}/{len(df_results)} languages")
print()

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Mean comparison
ax1 = axes[0, 0]
x = np.arange(len(languages))
width = 0.35
bars1 = ax1.bar(x - width/2, df_results['Greedy Mean (s)'], width, 
                label='Greedy (beam=1)', color='#2ecc71', alpha=0.8, 
                edgecolor='black', linewidth=1.5)
bars2 = ax1.bar(x + width/2, df_results['Beam Mean (s)'], width,
                label='Beam Search (beam=5)', color='#e74c3c', alpha=0.8,
                edgecolor='black', linewidth=1.5)
ax1.set_xlabel('Language', fontsize=12, fontweight='bold')
ax1.set_ylabel('Mean Processing Time (seconds)', fontsize=12, fontweight='bold')
ax1.set_title('Mean Processing Time Comparison\n(N=1000 per language)', 
              fontsize=13, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(df_results['Code'])
ax1.legend(fontsize=10)
ax1.grid(axis='y', alpha=0.3)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}s', ha='center', va='bottom', fontsize=8)

# Plot 2: Speedup percentage
ax2 = axes[0, 1]
colors = ['#2ecc71' if s > 0 else '#e74c3c' for s in df_results['Speedup (%)']]
bars = ax2.bar(x, df_results['Speedup (%)'], color=colors, alpha=0.8,
               edgecolor='black', linewidth=1.5)
ax2.set_xlabel('Language', fontsize=12, fontweight='bold')
ax2.set_ylabel('Speedup (%)', fontsize=12, fontweight='bold')
ax2.set_title('Greedy Speedup vs Beam Search\n(Positive = Faster)', 
              fontsize=13, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(df_results['Code'])
ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax2.grid(axis='y', alpha=0.3)

# Add value labels with significance stars
for i, (bar, row) in enumerate(zip(bars, df_results.itertuples())):
    height = bar.get_height()
    sig = '***' if row._8 < 0.001 else '**' if row._8 < 0.01 else '*' if row._8 < 0.05 else 'ns'
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{row._7:.1f}%\n{sig}',
            ha='center', va='bottom' if height > 0 else 'top', fontsize=9, fontweight='bold')

# Plot 3: Distribution comparison (example: first language)
ax3 = axes[1, 0]
if 1 in data[languages[0]] and 5 in data[languages[0]]:
    ax3.hist([data[languages[0]][1], data[languages[0]][5]], bins=30, 
             label=['Greedy', 'Beam'], alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Processing Time (seconds)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Frequency', fontsize=11, fontweight='bold')
    ax3.set_title(f'{lang_names[0]} - Distribution Comparison', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(alpha=0.3)

# Plot 4: Summary table
ax4 = axes[1, 1]
ax4.axis('tight')
ax4.axis('off')
table_data = df_results[['Code', 'Greedy Mean (s)', 'Beam Mean (s)', 'Speedup (%)', 'Significant']].values
table_data = [[f"{row[0]}", f"{row[1]:.3f}", f"{row[2]:.3f}", f"{row[3]:.1f}%", row[4]] 
              for row in table_data]
table = ax4.table(cellText=table_data, 
                  colLabels=['Lang', 'Greedy', 'Beam', 'Speedup', 'p<0.05'],
                  cellLoc='center', loc='center', bbox=[0, 0.3, 1, 0.6])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
ax4.set_title('Statistical Summary', fontsize=13, fontweight='bold', pad=20)

plt.suptitle('Full Beam Search Comparison: Greedy vs Beam (N=1000)', 
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save
plt.savefig(results_dir / 'full_beam_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig(results_dir / 'full_beam_comparison.pdf', bbox_inches='tight')
print(f"✅ Plots saved: {results_dir}/full_beam_comparison.png/.pdf")
print(f"✅ Summary saved: {results_dir}/full_comparison_summary.csv")
