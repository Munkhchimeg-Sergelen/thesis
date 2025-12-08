#!/usr/bin/env python3
"""Analyze resource profiling results"""

import pandas as pd

# Read data
df = pd.read_csv('results/resource_profiling.csv')

print("="*70)
print("RESOURCE PROFILING SUMMARY")
print("="*70)
print()

# Summary by model
print("Resource Usage by Model:")
print("-"*70)
summary = df.groupby('model').agg({
    'cpu_mean': ['mean', 'std', 'min', 'max'],
    'cpu_max': ['mean', 'max'],
    'memory_mean_gb': ['mean', 'std', 'min', 'max'],
    'memory_max_gb': ['mean', 'max'],
    'gpu_util_mean': ['mean', 'max'],
    'gpu_util_max': ['max'],
    'gpu_mem_mean_mb': ['mean', 'max'],
    'gpu_mem_max_mb': ['max'],
    'elapsed_sec': ['mean', 'std', 'min', 'max']
}).round(2)

print(summary)
print()

# Check GPU usage
print("GPU Usage Check:")
print("-"*70)
gpu_used = df[df['gpu_util_mean'] > 0]
print(f"Samples with GPU usage > 0: {len(gpu_used)} / {len(df)}")
print(f"Max GPU utilization: {df['gpu_util_max'].max():.1f}%")
print(f"Max GPU memory: {df['gpu_mem_max_mb'].max():.0f} MB")
print()

# Success rate
print("Processing Success Rate:")
print("-"*70)
success_rate = df.groupby('model')['success'].agg(['sum', 'count', lambda x: (x.sum()/len(x)*100)])
success_rate.columns = ['successful', 'total', 'success_rate_%']
print(success_rate)
print()

# Create clean summary table for thesis
print("THESIS TABLE - Resource Usage Summary:")
print("-"*70)
thesis_summary = df.groupby('model').agg({
    'cpu_mean': 'mean',
    'cpu_max': 'max',
    'memory_max_gb': 'max',
    'elapsed_sec': 'mean'
}).round(2)
thesis_summary.columns = ['CPU Avg (%)', 'CPU Peak (%)', 'Memory Peak (GB)', 'Avg Time (s)']
print(thesis_summary)
print()

# Save summary
thesis_summary.to_csv('results/resource_profiling_summary.csv')
print("✓ Summary saved to: results/resource_profiling_summary.csv")
