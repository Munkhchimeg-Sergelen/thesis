#!/usr/bin/env python3
"""
Analyze LID accuracy by comparing detected language vs ground truth
"""

import json
import glob
from pathlib import Path
import pandas as pd
import re

def extract_ground_truth_lang(filepath):
    """Extract language from file path (e.g., /es/ -> 'es')"""
    match = re.search(r'/(es|fr|hu|mn)/', filepath)
    return match.group(1) if match else None

def load_lid_results(results_dir="results"):
    """Load all LID→ASR JSON results"""
    results = []
    
    # Look for lid2asr results
    json_files = glob.glob(f"{results_dir}/transcripts/lid2asr/**/*.json", recursive=True)
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Extract ground truth from file path
                ground_truth = extract_ground_truth_lang(data.get('file', ''))
                detected = data.get('language_used')
                
                if ground_truth and detected:
                    results.append({
                        'file': Path(data['file']).name,
                        'ground_truth': ground_truth,
                        'detected': detected,
                        'system': data.get('system', 'unknown'),
                        'lid_prob': data.get('lid_prob'),
                        'fallback': data.get('fallback'),
                        'json_file': json_file
                    })
        except Exception as e:
            print(f"Warning: Failed to load {json_file}: {e}")
    
    return results

def analyze_lid_accuracy(df):
    """Compute LID accuracy metrics"""
    if df.empty:
        return None
    
    # Overall accuracy
    df['correct'] = df['ground_truth'] == df['detected']
    overall_acc = df['correct'].mean()
    
    # Accuracy by language
    lang_acc = df.groupby('ground_truth')['correct'].agg(['mean', 'count']).round(4)
    lang_acc.columns = ['accuracy', 'samples']
    
    # Accuracy by model
    if 'system' in df.columns:
        model_acc = df.groupby('system')['correct'].agg(['mean', 'count']).round(4)
        model_acc.columns = ['accuracy', 'samples']
    else:
        model_acc = None
    
    # Confusion matrix
    confusion = pd.crosstab(
        df['ground_truth'], 
        df['detected'],
        rownames=['Ground Truth'],
        colnames=['Detected']
    )
    
    return {
        'overall': overall_acc,
        'by_language': lang_acc,
        'by_model': model_acc,
        'confusion_matrix': confusion
    }

def main():
    print("Analyzing LID accuracy...")
    print()
    
    # Load results
    results = load_lid_results()
    
    if not results:
        print("No LID results found! Run run_lid_evaluation.sh first.")
        return
    
    df = pd.DataFrame(results)
    print(f"Loaded {len(df)} LID results")
    print()
    
    # Analyze
    analysis = analyze_lid_accuracy(df)
    
    if not analysis:
        print("Could not compute LID accuracy!")
        return
    
    # Create output directory
    output_dir = Path("results/analysis")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Print and save results
    print("=" * 70)
    print("LID ACCURACY ANALYSIS")
    print("=" * 70)
    print()
    
    print(f"Overall LID Accuracy: {analysis['overall']:.2%}")
    print()
    
    print("Accuracy by Language:")
    print(analysis['by_language'])
    print()
    
    if analysis['by_model'] is not None:
        print("Accuracy by Model:")
        print(analysis['by_model'])
        print()
    
    print("Confusion Matrix:")
    print(analysis['confusion_matrix'])
    print()
    
    # Save to files
    with open(output_dir / "lid_accuracy_summary.txt", "w") as f:
        f.write(f"Overall LID Accuracy: {analysis['overall']:.2%}\n\n")
        f.write("Accuracy by Language:\n")
        f.write(analysis['by_language'].to_string())
        f.write("\n\n")
        if analysis['by_model'] is not None:
            f.write("Accuracy by Model:\n")
            f.write(analysis['by_model'].to_string())
            f.write("\n\n")
        f.write("Confusion Matrix:\n")
        f.write(analysis['confusion_matrix'].to_string())
    
    # Save CSVs
    analysis['by_language'].to_csv(output_dir / "lid_accuracy_by_language.csv")
    if analysis['by_model'] is not None:
        analysis['by_model'].to_csv(output_dir / "lid_accuracy_by_model.csv")
    analysis['confusion_matrix'].to_csv(output_dir / "lid_confusion_matrix.csv")
    df.to_csv(output_dir / "lid_full_results.csv", index=False)
    
    print("=" * 70)
    print("Saved results to: results/analysis/")
    print("=" * 70)

if __name__ == "__main__":
    main()
