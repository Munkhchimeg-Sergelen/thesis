#!/usr/bin/env python3
"""
Sample 1000 audio files from Common Voice v23.0 clips
Create clean dataset with perfect TSV alignment
"""

import csv
import random
import shutil
from pathlib import Path
import argparse

def prepare_language(lang, cv_base, output_base, num_samples=1000):
    """Sample and prepare one language"""
    
    print(f"\n{'='*60}")
    print(f"Preparing {lang.upper()}")
    print(f"{'='*60}")
    
    # Paths
    tsv_file = Path(cv_base) / lang / "test.tsv"
    clips_dir = Path(cv_base) / lang / "clips"
    
    audio_out = Path(output_base) / "wav" / lang
    ref_out = Path(output_base) / "ref" / lang
    
    audio_out.mkdir(parents=True, exist_ok=True)
    ref_out.mkdir(parents=True, exist_ok=True)
    
    # Load TSV
    print(f"Loading {tsv_file}")
    samples = []
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            path = row.get('path', '')
            sentence = row.get('sentence', '').strip()
            if path and sentence:
                clip_file = clips_dir / path
                if clip_file.exists():
                    samples.append({
                        'path': clip_file,
                        'sentence': sentence
                    })
    
    print(f"✓ Found {len(samples)} valid samples in test set")
    
    if len(samples) < num_samples:
        print(f"⚠️  Only {len(samples)} available, using all")
        num_samples = len(samples)
    
    # Random sample
    selected = random.sample(samples, num_samples)
    print(f"✓ Randomly selected {num_samples} samples")
    
    # Copy and save
    print("Copying files...")
    copied = 0
    for i, sample in enumerate(selected, 1):
        # New filename
        new_name = f"{lang}{i:04d}"
        
        # Copy audio
        audio_src = sample['path']
        audio_dst = audio_out / f"{new_name}.mp3"
        shutil.copy2(audio_src, audio_dst)
        
        # Save reference
        ref_dst = ref_out / f"{new_name}.txt"
        with open(ref_dst, 'w', encoding='utf-8') as f:
            f.write(sample['sentence'])
        
        copied += 1
        if copied % 100 == 0:
            print(f"  Copied {copied}/{num_samples}...")
    
    print(f"✓ Copied {copied} audio files")
    print(f"✓ Saved {copied} references")
    print(f"  Audio: {audio_out}/")
    print(f"  References: {ref_out}/")
    
    return copied

def main():
    parser = argparse.ArgumentParser(description='Prepare v23.0 dataset')
    parser.add_argument('--cv-base', default='~/cv-datasets/cv-corpus-23.0-2025-09-05',
                        help='Path to extracted CV corpus')
    parser.add_argument('--output-base', default='data_v23',
                        help='Output directory for new dataset')
    parser.add_argument('--num-samples', type=int, default=1000,
                        help='Number of samples per language')
    parser.add_argument('--langs', nargs='+', default=['es', 'fr', 'hu', 'mn'],
                        help='Languages to process')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    # Expand home directory
    cv_base = Path(args.cv_base).expanduser()
    output_base = Path(args.output_base)
    
    # Set seed
    random.seed(args.seed)
    
    print("="*60)
    print("PREPARE COMMON VOICE V23.0 DATASET")
    print("="*60)
    print(f"Source: {cv_base}")
    print(f"Output: {output_base}")
    print(f"Languages: {', '.join(args.langs)}")
    print(f"Samples per language: {args.num_samples}")
    print(f"Random seed: {args.seed}")
    
    # Process each language
    total = 0
    for lang in args.langs:
        count = prepare_language(lang, cv_base, output_base, args.num_samples)
        total += count
    
    print("\n" + "="*60)
    print("✅ DATASET PREPARATION COMPLETE")
    print("="*60)
    print(f"Total samples: {total}")
    print(f"\nNext steps:")
    print(f"1. Backup old data: mv data data_old")
    print(f"2. Use new data: mv {output_base} data")
    print(f"3. Re-run ASR models on new audio")
    print(f"4. Calculate WER/CER (perfect alignment guaranteed!)")

if __name__ == '__main__':
    main()
