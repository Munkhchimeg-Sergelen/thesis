#!/usr/bin/env python3
"""Visualize Greedy vs Beam Search Comparison"""

import matplotlib.pyplot as plt
import numpy as np

# Data from beam_test_results.txt
languages = ['Mongolian', 'Hungarian', 'Spanish', 'French']
lang_codes = ['MN', 'HU', 'ES', 'FR']
greedy_times = [51.446, 6.327, 4.490, 4.548]  # beam_size=1
beam_times = [55.741, 6.247, 4.866, 4.893]    # beam_size=5

# Calculate speedup
speedup = [(beam - greedy) / beam * 100 for greedy, beam in zip(greedy_times, beam_times)]

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ===== Plot 1: Processing Time Comparison =====
x = np.arange(len(languages))
width = 0.35

bars1 = ax1.bar(x - width/2, greedy_times, width, label='Greedy (beam=1)', 
                color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax1.bar(x + width/2, beam_times, width, label='Beam Search (beam=5)', 
                color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)

ax1.set_xlabel('Language', fontsize=12, fontweight='bold')
ax1.set_ylabel('Average Processing Time (seconds)', fontsize=12, fontweight='bold')
ax1.set_title('Greedy vs Beam Search Decoding\n(5 files per language, Whisper-small, CPU)', 
              fontsize=14, fontweight='bold', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(lang_codes, fontsize=11)
ax1.legend(fontsize=11, loc='upper left')
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}s',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

# ===== Plot 2: Speedup Percentage =====
colors = ['#2ecc71' if s > 0 else '#e74c3c' for s in speedup]
bars3 = ax2.bar(x, speedup, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

ax2.set_xlabel('Language', fontsize=12, fontweight='bold')
ax2.set_ylabel('Speedup (%)', fontsize=12, fontweight='bold')
ax2.set_title('Greedy Speedup vs Beam Search\n(Positive = Greedy is Faster)', 
              fontsize=14, fontweight='bold', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(lang_codes, fontsize=11)
ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels
for i, (bar, val) in enumerate(zip(bars3, speedup)):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.1f}%',
            ha='center', va='bottom' if val > 0 else 'top', 
            fontsize=10, fontweight='bold')

# Add summary statistics
avg_speedup = np.mean(speedup)
fig.text(0.5, 0.02, f'Average Speedup: {avg_speedup:.1f}% | Greedy is faster in 3/4 languages', 
         ha='center', fontsize=11, fontweight='bold', 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout(rect=[0, 0.05, 1, 1])

# Save figure
plt.savefig('beam_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('beam_comparison.pdf', bbox_inches='tight')
print("✅ Saved: beam_comparison.png")
print("✅ Saved: beam_comparison.pdf")

plt.show()
