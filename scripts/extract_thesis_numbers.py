#!/usr/bin/env python3
"""
Extract key numbers for thesis writing
Creates a NUMBERS.txt file with essential statistics
"""

import pandas as pd
import json
from pathlib import Path

def extract_key_numbers():
    """Extract and format key statistics for thesis"""
    
    print("="*60)
    print("EXTRACTING KEY NUMBERS FOR THESIS")
    print("="*60)
    
    output = []
    output.append("="*60)
    output.append("KEY STATISTICS FOR THESIS WRITING")
    output.append("="*60)
    output.append("")
    
    # Load WER/CER results
    try:
        results_file = Path("results/wer_cer_results_summary.csv")
        if results_file.exists():
            df = pd.read_csv(results_file)
            
            output.append("ACCURACY RESULTS:")
            output.append("-" * 40)
            
            # Best and worst WER per language
            for lang in ['mn', 'hu', 'es', 'fr']:
                lang_data = df[df['language'] == lang]
                if not lang_data.empty:
                    best = lang_data.loc[lang_data['wer'].idxmin()]
                    worst = lang_data.loc[lang_data['wer'].idxmax()]
                    
                    output.append(f"\n{lang.upper()}:")
                    output.append(f"  Best WER:  {best['wer']:.3f} ({best['model']})")
                    output.append(f"  Worst WER: {worst['wer']:.3f} ({worst['model']})")
                    output.append(f"  Best CER:  {best['cer']:.3f}")
                    output.append(f"  Avg WER:   {lang_data['wer'].mean():.3f}")
            
            # Overall statistics
            output.append(f"\nOVERALL:")
            output.append(f"  Best WER overall:  {df['wer'].min():.3f}")
            output.append(f"  Worst WER overall: {df['wer'].max():.3f}")
            output.append(f"  Mean WER:          {df['wer'].mean():.3f}")
            output.append(f"  Median WER:        {df['wer'].median():.3f}")
            
            # By model
            output.append(f"\nBY MODEL:")
            for model in df['model'].unique():
                model_data = df[df['model'] == model]
                output.append(f"  {model}:")
                output.append(f"    Avg WER: {model_data['wer'].mean():.3f}")
                output.append(f"    Avg CER: {model_data['cer'].mean():.3f}")
            
    except Exception as e:
        output.append(f"ERROR loading WER/CER results: {e}")
    
    output.append("")
    
    # Load RTF results
    try:
        # Try to find RTF in results
        if results_file.exists():
            df = pd.read_csv(results_file)
            if 'rtf' in df.columns:
                output.append("SPEED (RTF):")
                output.append("-" * 40)
                
                for lang in ['mn', 'hu', 'es', 'fr']:
                    lang_data = df[df['language'] == lang]
                    if not lang_data.empty and 'rtf' in lang_data.columns:
                        output.append(f"{lang.upper()}: RTF = {lang_data['rtf'].mean():.2f}")
                
                # Speed comparison
                if 'mn' in df['language'].values and 'es' in df['language'].values:
                    mn_rtf = df[df['language'] == 'mn']['rtf'].mean()
                    es_rtf = df[df['language'] == 'es']['rtf'].mean()
                    if es_rtf > 0:
                        ratio = mn_rtf / es_rtf
                        output.append(f"\nMN/ES speed ratio: {ratio:.1f}×")
    except Exception as e:
        output.append(f"ERROR loading RTF: {e}")
    
    output.append("")
    
    # Load LID results
    try:
        lid_file = Path("results/lid_accuracy_summary.csv")
        if lid_file.exists():
            lid_df = pd.read_csv(lid_file)
            
            output.append("LANGUAGE IDENTIFICATION:")
            output.append("-" * 40)
            output.append(f"Overall accuracy: {lid_df['accuracy'].mean():.1%}")
            
            for _, row in lid_df.iterrows():
                output.append(f"  {row['language'].upper()}: {row['accuracy']:.1%}")
        
    except Exception as e:
        output.append(f"NOTE: LID results not found (expected if not yet run)")
    
    output.append("")
    
    # Dataset info
    output.append("DATASET:")
    output.append("-" * 40)
    output.append("  Source: Common Voice v23.0")
    output.append("  Languages: 4 (MN, HU, ES, FR)")
    output.append("  Samples per language: 1,000")
    output.append("  Total samples: 4,000")
    output.append("  Total transcriptions: 16,000 (4 models)")
    
    output.append("")
    
    # Long-form drift
    try:
        drift_file = Path("data/long_form/drift_analysis.json")
        if drift_file.exists():
            with open(drift_file) as f:
                drift_data = json.load(f)
            
            output.append("LONG-FORM DRIFT:")
            output.append("-" * 40)
            output.append(f"  Samples analyzed: {len(drift_data)}")
            
            avg_wers = [d['avg_wer'] for d in drift_data]
            output.append(f"  Average WER range: {min(avg_wers):.3f} - {max(avg_wers):.3f}")
            output.append(f"  Mean WER: {sum(avg_wers)/len(avg_wers):.3f}")
            
            # Language stability
            all_french = all(d['detected_language'] == 'fr' for d in drift_data)
            output.append(f"  Language stability: {'✓ All correctly identified as French' if all_french else '✗ Some misidentifications'}")
    
    except Exception as e:
        output.append(f"NOTE: Long-form drift data not found")
    
    output.append("")
    output.append("="*60)
    output.append("Copy these numbers to your thesis!")
    output.append("="*60)
    
    # Print to console
    for line in output:
        print(line)
    
    # Save to file
    with open("thesis/NUMBERS.txt", "w") as f:
        f.write("\n".join(output))
    
    print(f"\n✓ Saved to thesis/NUMBERS.txt")

if __name__ == "__main__":
    extract_key_numbers()
