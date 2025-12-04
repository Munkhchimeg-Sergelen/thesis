#!/usr/bin/env python
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import json
import numpy as np


def setup_thesis_style():
    """Set up publication-quality plot styling"""
    plt.rcParams.update({
        'figure.figsize': (10, 6),
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'figure.autolayout': True
    })
    sns.set_theme(style="whitegrid")


def analyze_lid_accuracy(results_dir, out_dir):
    """Analyze Language ID accuracy from test results"""
    # Create output directory
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    
    print("Looking for LID results in:", results_dir, flush=True)
    
    # Read results from JSON files
    results = []
    for lang in ['mn', 'hu', 'es', 'fr']:
        print(f"\nAnalyzing {lang.upper()}...", flush=True)
        lang_path = Path(results_dir) / f"whisper-small/{lang}/lid2asr/whisper-small/{lang}"
        print(f"Full path: {lang_path.absolute()}", flush=True)
        
        if not lang_path.exists():
            print(f"❌ Directory not found: {lang_path}", flush=True)
            continue
            
        json_files = list(lang_path.glob('*.json'))
        print(f"Found {len(json_files)} JSON files", flush=True)
        
        for json_file in json_files:
            print(f"Reading {json_file.name}...", flush=True)
            try:
                with open(json_file) as f:
                    data = json.load(f)
                    print(f"Fields in JSON: {list(data.keys())}", flush=True)
                    results.append({
                        'file': json_file.stem,
                        'actual_lang': lang,
                        'detected_lang': data.get('lid_language', ''),
                        'confidence': data.get('lid_prob', 0),
                        'fallback': data.get('fallback', '')
                    })
                    print(f"✓ Processed {json_file.name}", flush=True)
            except Exception as e:
                print(f"❌ Error reading {json_file}: {str(e)}", flush=True)

    if not results:
        print("\n❌ No LID data found!", flush=True)
        return None
        
    df = pd.DataFrame(results)
    print(f"\nFound {len(df)} results", flush=True)
    
    # Count fallbacks
    fallbacks = df['fallback'].value_counts()
    print("\nFallback Analysis:", flush=True)
    print(fallbacks, flush=True)
    
    # 1. Confusion Matrix
    plt.figure(figsize=(10, 8))
    confusion = pd.crosstab(df['actual_lang'], df['detected_lang'])
    sns.heatmap(confusion, annot=True, fmt='d', cmap='YlOrRd')
    plt.title('Language Detection Confusion Matrix')
    plt.xlabel('Detected Language')
    plt.ylabel('Actual Language')
    plt.tight_layout()
    plt.savefig(out_dir / '13_lid_confusion_matrix.png')
    plt.close()
    
    # 2. Accuracy by Language
    accuracy = (df['actual_lang'] == df['detected_lang']).groupby(df['actual_lang']).mean()
    plt.figure(figsize=(10, 6))
    accuracy.plot(kind='bar')
    plt.title('Language Detection Accuracy by Language')
    plt.xlabel('Language')
    plt.ylabel('Accuracy')
    plt.tight_layout()
    plt.savefig(out_dir / '14_lid_accuracy.png')
    plt.close()
    
    # 3. Confidence Distribution
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='actual_lang', y='confidence', hue='detected_lang')
    plt.title('Language Detection Confidence Scores')
    plt.xlabel('Actual Language')
    plt.ylabel('Confidence Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_dir / '15_lid_confidence.png')
    plt.close()
    
    # Save summary statistics
    summary = {
        'overall_accuracy': (df['actual_lang'] == df['detected_lang']).mean(),
        'accuracy_by_language': accuracy.to_dict(),
        'confusion_matrix': confusion.to_dict(),
        'fallback_counts': fallbacks.to_dict()
    }
    
    with open(out_dir / 'lid_accuracy_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\nLID Accuracy Summary:", flush=True)
    print(f"Overall Accuracy: {summary['overall_accuracy']:.2%}", flush=True)
    print("\nAccuracy by Language:", flush=True)
    for lang, acc in summary['accuracy_by_language'].items():
        print(f"{lang.upper()}: {acc:.2%}", flush=True)
    
    return summary


if __name__ == '__main__':
    print("============================================================", flush=True)
    print("LID ACCURACY ANALYSIS", flush=True)
    print("============================================================", flush=True)
    
    setup_thesis_style()
    summary = analyze_lid_accuracy('results_lid_test', 'thesis_plots')    
    print("\n============================================================")
    print("✅ LID ANALYSIS COMPLETE")
    print("============================================================")

    # Debug prints:
    print("\nDEBUG INFO:", flush=True)
    print(f"Current working directory: {Path.cwd()}", flush=True)
    print("\nChecking directories:", flush=True)
    for lang in ['mn', 'hu', 'es', 'fr']:
        lang_path = Path('results_lid_test') / f"whisper-small/{lang}/lid2asr/whisper-small/{lang}"
        print(f"\n{lang.upper()}:", flush=True)
        print(f"Looking in: {lang_path}", flush=True)
        if lang_path.exists():
            json_files = list(lang_path.glob('*.json'))
            print(f"✓ Found directory with {len(json_files)} JSON files", flush=True)
        else:
            print(f"❌ Directory not found", flush=True)