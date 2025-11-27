#!/usr/bin/env python3
"""
Analyze Language Identification (LID) accuracy
Compare detected language vs actual language
"""

import json
from pathlib import Path
import pandas as pd
import argparse

def analyze_lid_accuracy(results_dir, output_file):
    """Analyze LID accuracy from lid2asr mode results"""
    
    print("="*60)
    print("LID ACCURACY ANALYSIS")
    print("="*60)
    
    data = []
    langs = ['mn', 'hu', 'es', 'fr']
    
    # Language code mapping
    lang_map = {
        'mn': ['mn', 'khk', 'mongolian'],
        'hu': ['hu', 'hun', 'hungarian'],
        'es': ['es', 'spa', 'spanish'],
        'fr': ['fr', 'fra', 'french']
    }
    
    results_path = Path(results_dir)
    
    for actual_lang in langs:
        lang_dir = results_path / "whisper-small" / actual_lang
        
        if not lang_dir.exists():
            print(f"⚠️  No results for {actual_lang}")
            continue
        
        print(f"\nAnalyzing {actual_lang.upper()}...")
        
        json_files = list(lang_dir.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file) as f:
                    result = json.load(f)
                
                detected_lang = result.get('language_used', 'unknown')
                file_id = json_file.stem
                
                # Check if detection is correct
                correct = any(code in detected_lang.lower() 
                             for code in lang_map.get(actual_lang, [actual_lang]))
                
                data.append({
                    'file_id': file_id,
                    'actual_language': actual_lang,
                    'detected_language': detected_lang,
                    'correct': correct,
                    'transcript': result.get('transcript', ''),
                })
            
            except Exception as e:
                print(f"  Error reading {json_file}: {e}")
    
    if not data:
        print("\n❌ No LID data found!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Calculate accuracy
    print("\n" + "="*60)
    print("LID ACCURACY RESULTS")
    print("="*60)
    
    overall_accuracy = df['correct'].mean() * 100
    print(f"\nOverall LID Accuracy: {overall_accuracy:.2f}%")
    
    # Per-language accuracy
    lang_accuracy = df.groupby('actual_language')['correct'].agg(['sum', 'count', 'mean'])
    lang_accuracy['accuracy_%'] = lang_accuracy['mean'] * 100
    lang_accuracy = lang_accuracy.round(2)
    
    print("\nPer-Language Accuracy:")
    print(lang_accuracy)
    
    # Confusion matrix
    print("\nDetected Language Distribution:")
    confusion = pd.crosstab(df['actual_language'], df['detected_language'], margins=True)
    print(confusion)
    
    # Save results
    df.to_csv(output_file, index=False)
    print(f"\n✓ Saved detailed results: {output_file}")
    
    # Save summary
    summary_file = output_file.replace('.csv', '_summary.csv')
    lang_accuracy.to_csv(summary_file)
    print(f"✓ Saved summary: {summary_file}")
    
    # Save confusion matrix
    confusion_file = output_file.replace('.csv', '_confusion.csv')
    confusion.to_csv(confusion_file)
    print(f"✓ Saved confusion matrix: {confusion_file}")
    
    return overall_accuracy

def main():
    parser = argparse.ArgumentParser(description='Analyze LID accuracy')
    parser.add_argument('--results-dir', default='results_lid_test',
                        help='Directory with LID test results')
    parser.add_argument('--output', default='results/lid_accuracy.csv',
                        help='Output CSV file')
    
    args = parser.parse_args()
    
    accuracy = analyze_lid_accuracy(args.results_dir, args.output)
    
    print("\n" + "="*60)
    print("✅ LID ANALYSIS COMPLETE")
    print("="*60)
    if accuracy:
        print(f"Overall Accuracy: {accuracy:.2f}%")

if __name__ == '__main__':
    main()
