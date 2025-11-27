#!/usr/bin/env python3
"""
Analyze error types (insertion/deletion/substitution) from WER/CER results
"""

import pandas as pd
import jiwer
from pathlib import Path
import argparse

def analyze_error_types(results_csv, ref_dir, model_results_dir, output_file):
    """Analyze detailed error types"""
    
    print("="*60)
    print("ERROR TYPE ANALYSIS")
    print("="*60)
    
    # Load WER/CER results
    df = pd.read_csv(results_csv)
    
    error_data = []
    
    for _, row in df.iterrows():
        file_id = row['file_id']
        model = row.get('model', 'unknown')
        lang = row.get('language', 'unknown')
        
        # Get reference
        ref_file = Path(ref_dir) / lang / f"{file_id}.txt"
        if not ref_file.exists():
            continue
        
        with open(ref_file, 'r', encoding='utf-8') as f:
            reference = f.read().strip()
        
        # Get hypothesis from row
        hypothesis = row.get('hypothesis', '')
        
        if not hypothesis or not reference:
            continue
        
        # Calculate detailed measures
        try:
            measures = jiwer.compute_measures(reference, hypothesis)
            
            error_data.append({
                'file_id': file_id,
                'model': model,
                'language': lang,
                'wer': measures['wer'],
                'mer': measures['mer'],  # Match Error Rate
                'wil': measures['wil'],  # Word Info Lost
                'wip': measures['wip'],  # Word Info Preserved
                'hits': measures['hits'],
                'substitutions': measures['substitutions'],
                'deletions': measures['deletions'],
                'insertions': measures['insertions'],
                'reference_length': len(reference.split()),
                'hypothesis_length': len(hypothesis.split()),
            })
        except Exception as e:
            print(f"Error processing {file_id}: {e}")
    
    # Create DataFrame
    error_df = pd.DataFrame(error_data)
    
    if error_df.empty:
        print("No data to analyze")
        return
    
    print(f"\nAnalyzed {len(error_df)} samples")
    
    # Summary by model and language
    print("\n" + "="*60)
    print("ERROR TYPE DISTRIBUTION")
    print("="*60)
    
    summary = error_df.groupby(['model', 'language']).agg({
        'substitutions': ['sum', 'mean'],
        'deletions': ['sum', 'mean'],
        'insertions': ['sum', 'mean'],
        'wer': 'mean',
        'reference_length': 'sum'
    }).round(3)
    
    print(summary)
    
    # Calculate percentages
    error_df['sub_pct'] = error_df['substitutions'] / error_df['reference_length'] * 100
    error_df['del_pct'] = error_df['deletions'] / error_df['reference_length'] * 100
    error_df['ins_pct'] = error_df['insertions'] / error_df['reference_length'] * 100
    
    # Aggregate
    pct_summary = error_df.groupby(['model', 'language']).agg({
        'sub_pct': 'mean',
        'del_pct': 'mean',
        'ins_pct': 'mean',
    }).round(2)
    
    print("\n" + "="*60)
    print("ERROR TYPE PERCENTAGES")
    print("="*60)
    print(pct_summary)
    
    # Save detailed results
    error_df.to_csv(output_file, index=False)
    print(f"\n✓ Saved detailed error analysis: {output_file}")
    
    # Save summary
    summary_file = output_file.replace('.csv', '_summary.csv')
    pct_summary.to_csv(summary_file)
    print(f"✓ Saved summary: {summary_file}")

def main():
    parser = argparse.ArgumentParser(description='Analyze error types')
    parser.add_argument('--results-csv', default='results/wer_cer_results.csv',
                        help='WER/CER results file')
    parser.add_argument('--ref-dir', default='data/ref',
                        help='Reference directory')
    parser.add_argument('--model-results-dir', default='results/transcripts',
                        help='Model results directory')
    parser.add_argument('--output', default='results/error_type_analysis.csv',
                        help='Output file')
    
    args = parser.parse_args()
    
    analyze_error_types(args.results_csv, args.ref_dir, args.model_results_dir, args.output)
    
    print("\n" + "="*60)
    print("✅ ERROR TYPE ANALYSIS COMPLETE")
    print("="*60)

if __name__ == '__main__':
    main()
