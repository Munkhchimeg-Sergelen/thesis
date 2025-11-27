#!/usr/bin/env python3
"""
Match references by searching TSV with model outputs (faster than duration)
"""

import csv
import json
from pathlib import Path
from difflib import get_close_matches
import argparse

def load_tsv_fast(tsv_file):
    """Load TSV into searchable dict"""
    print(f"Loading TSV: {tsv_file}")
    data = {}
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            sentence = row.get('sentence', '').strip().lower()
            if sentence:
                data[sentence] = row.get('sentence', '').strip()  # Keep original
    print(f"✓ Loaded {len(data)} unique sentences")
    return data

def match_files(lang, tsv_file, model_dir, output_dir):
    """Match using model transcripts"""
    
    print(f"\n{'='*60}")
    print(f"Matching {lang.upper()} using transcript search")
    print(f"{'='*60}")
    
    # Load TSV
    tsv_data = load_tsv_fast(tsv_file)
    
    # Process model outputs
    json_files = sorted(Path(model_dir).glob("*.json"))
    print(f"Found {len(json_files)} files to match")
    
    matched = 0
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for json_file in json_files:
        file_id = json_file.stem
        
        # Get model output
        with open(json_file) as f:
            data = json.load(f)
        
        hypothesis = data.get('transcript', '').strip().lower()
        
        if not hypothesis:
            txt_file = json_file.with_suffix('.txt')
            if txt_file.exists():
                with open(txt_file, 'r', encoding='utf-8') as f:
                    hypothesis = f.read().strip().lower()
        
        if not hypothesis:
            continue
        
        # Find best match
        matches = get_close_matches(hypothesis, tsv_data.keys(), n=1, cutoff=0.6)
        
        if matches:
            reference = tsv_data[matches[0]]
            
            # Save reference
            ref_file = Path(output_dir) / f"{file_id}.txt"
            with open(ref_file, 'w', encoding='utf-8') as f:
                f.write(reference)
            
            matched += 1
            if matched % 100 == 0:
                print(f"  Matched {matched}...")
    
    print(f"\n✓ Matched {matched}/{len(json_files)} files")
    return matched

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', required=True)
    parser.add_argument('--tsv-file', required=True)
    parser.add_argument('--model-dir', default=None)
    parser.add_argument('--output-dir', required=True)
    
    args = parser.parse_args()
    
    if not args.model_dir:
        args.model_dir = f"results/transcripts/hinted/omnilingual/omniASR_CTC_300M/{args.lang}"
    
    matched = match_files(args.lang, args.tsv_file, args.model_dir, args.output_dir)
    
    print("\n" + "="*60)
    if matched > 900:
        print("✅ EXCELLENT!")
    elif matched > 700:
        print("⚠️  PARTIAL")
    else:
        print("❌ POOR")
    print("="*60)

if __name__ == '__main__':
    main()
