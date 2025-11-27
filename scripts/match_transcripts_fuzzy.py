#!/usr/bin/env python3
"""
Match audio files to TSV transcripts using fuzzy matching on model outputs
Uses model transcriptions to find the correct reference in TSV
"""

import csv
import json
from pathlib import Path
from difflib import SequenceMatcher
import argparse

def normalize_text(text):
    """Normalize text for comparison"""
    import unicodedata
    import re
    # Remove accents, lowercase, remove punctuation
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s]', '', text.lower())
    return ' '.join(text.split())

def similarity(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()

def match_transcripts(lang, tsv_file, model_dir, ref_dir):
    """Match transcripts using fuzzy matching"""
    
    print(f"\n{'='*60}")
    print(f"Matching transcripts for {lang.upper()}")
    print(f"{'='*60}")
    
    # Load TSV transcripts
    print(f"Loading TSV: {tsv_file}")
    tsv_transcripts = []
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            tsv_transcripts.append({
                'path': row.get('path', ''),
                'sentence': row.get('sentence', '').strip()
            })
    
    print(f"✓ Loaded {len(tsv_transcripts)} TSV transcripts")
    
    # Process each audio file
    json_files = sorted(Path(model_dir).glob("*.json"))
    print(f"✓ Found {len(json_files)} model outputs")
    
    matches = []
    matched_indices = set()
    
    for json_file in json_files:
        file_id = json_file.stem
        
        # Load model output
        with open(json_file) as f:
            data = json.load(f)
        
        # Get hypothesis (from JSON or .txt)
        hypothesis = data.get('transcript', '')
        if not hypothesis:
            txt_file = json_file.with_suffix('.txt')
            if txt_file.exists():
                with open(txt_file, 'r', encoding='utf-8') as f:
                    hypothesis = f.read().strip()
        
        if not hypothesis:
            print(f"⚠️  No transcript for {file_id}")
            continue
        
        # Find best match in TSV
        best_match = None
        best_score = 0.0
        best_idx = -1
        
        for idx, tsv_entry in enumerate(tsv_transcripts):
            if idx in matched_indices:
                continue  # Already matched
            
            score = similarity(hypothesis, tsv_entry['sentence'])
            if score > best_score:
                best_score = score
                best_match = tsv_entry
                best_idx = idx
        
        if best_score > 0.5:  # Accept reasonable matches
            matches.append({
                'file_id': file_id,
                'reference': best_match['sentence'],
                'hypothesis': hypothesis,
                'match_score': best_score,
                'tsv_index': best_idx
            })
            matched_indices.add(best_idx)
            
            # Save reference
            ref_file = Path(ref_dir) / f"{file_id}.txt"
            with open(ref_file, 'w', encoding='utf-8') as f:
                f.write(best_match['sentence'])
        else:
            print(f"⚠️  Poor match for {file_id} (score: {best_score:.2f})")
    
    print(f"\n✓ Matched {len(matches)}/{len(json_files)} files")
    print(f"  Average match score: {sum(m['match_score'] for m in matches) / len(matches):.2%}")
    
    # Save matching report
    report_file = Path(f"data/matching_report_{lang}.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"Matching Report for {lang.upper()}\n")
        f.write("="*60 + "\n\n")
        for m in matches[:10]:  # Show first 10
            f.write(f"File: {m['file_id']}\n")
            f.write(f"Score: {m['match_score']:.2%}\n")
            f.write(f"Hypothesis: {m['hypothesis']}\n")
            f.write(f"Reference:  {m['reference']}\n")
            f.write("-"*60 + "\n")
    
    print(f"✓ Saved report: {report_file}")
    
    return len(matches)

def main():
    parser = argparse.ArgumentParser(description='Match transcripts using fuzzy matching')
    parser.add_argument('--lang', required=True, choices=['mn', 'hu', 'es', 'fr'])
    parser.add_argument('--tsv-file', required=True, help='Path to test.tsv')
    parser.add_argument('--model-dir', default=None, help='Model output directory (defaults to OmniLingual CTC_300M)')
    parser.add_argument('--ref-dir', default=None, help='Reference directory (defaults to data/ref/{lang})')
    
    args = parser.parse_args()
    
    # Set defaults
    if not args.model_dir:
        args.model_dir = f"results/transcripts/hinted/omnilingual/omniASR_CTC_300M/{args.lang}"
    if not args.ref_dir:
        args.ref_dir = f"data/ref/{args.lang}"
    
    # Create ref dir
    Path(args.ref_dir).mkdir(parents=True, exist_ok=True)
    
    # Run matching
    matched = match_transcripts(args.lang, args.tsv_file, args.model_dir, args.ref_dir)
    
    print("\n" + "="*60)
    if matched > 900:
        print("✅ SUCCESS - Good matching rate!")
    elif matched > 700:
        print("⚠️  PARTIAL - Some matches may be incorrect")
    else:
        print("❌ POOR - Matching failed")
    print("="*60)

if __name__ == '__main__':
    main()
