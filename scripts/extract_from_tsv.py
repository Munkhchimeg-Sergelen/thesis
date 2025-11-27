#!/usr/bin/env python3
"""
Extract transcripts from Common Voice TSV file
Maps audio filenames to transcripts
"""

import csv
import argparse
from pathlib import Path

def extract_transcripts(tsv_file, lang, output_dir="data/ref"):
    """Extract transcripts from TSV file"""
    
    print(f"\n{'='*60}")
    print(f"Extracting transcripts for {lang.upper()}")
    print(f"{'='*60}")
    print(f"TSV file: {tsv_file}")
    
    ref_dir = Path(output_dir) / lang
    ref_dir.mkdir(parents=True, exist_ok=True)
    
    # Read TSV file
    transcripts = {}
    
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        
        for row in reader:
            # Common Voice TSV has 'path' (filename) and 'sentence' (transcript)
            audio_path = row.get('path', '')
            sentence = row.get('sentence', '').strip()
            
            if audio_path and sentence:
                # Extract just the filename without extension
                filename = Path(audio_path).stem
                transcripts[filename] = sentence
    
    print(f"✓ Loaded {len(transcripts)} transcripts from TSV")
    
    # Now map to your audio files (mn0001, mn0002, etc.)
    audio_dir = Path(f"data/wav/{lang}")
    
    if not audio_dir.exists():
        print(f"❌ Audio directory not found: {audio_dir}")
        return
    
    audio_files = sorted(audio_dir.glob("*.mp3"))
    print(f"✓ Found {len(audio_files)} audio files")
    
    # Try to match audio files to transcripts
    matched = 0
    
    print("\nMapping audio files to transcripts...")
    
    # Strategy 1: Direct filename match
    for audio_file in audio_files:
        base_name = audio_file.stem  # e.g., 'mn0001'
        
        # Try to find matching transcript
        # Common Voice files are named like 'common_voice_xx_12345.mp3'
        # We need to find which CV file corresponds to our mn0001
        
        # For now, save with index-based matching
        # This assumes your files are in the same order as the TSV
        pass
    
    # Strategy 2: Sequential matching (assumes same order)
    print("\nUsing sequential matching (assumes files downloaded in order)...")
    
    transcript_list = list(transcripts.values())
    
    for i, audio_file in enumerate(audio_files[:len(transcript_list)]):
        if i < len(transcript_list):
            ref_file = ref_dir / f"{audio_file.stem}.txt"
            
            with open(ref_file, 'w', encoding='utf-8') as f:
                f.write(transcript_list[i])
            
            matched += 1
            
            if (i + 1) % 100 == 0:
                print(f"  Saved {i+1} transcripts...")
    
    print(f"\n✓ Matched and saved {matched} transcripts")
    print(f"  Location: {ref_dir}/")
    
    return matched

def main():
    parser = argparse.ArgumentParser(description='Extract transcripts from Common Voice TSV')
    parser.add_argument('--tsv-file', required=True, help='Path to validated.tsv or test.tsv')
    parser.add_argument('--lang', required=True, choices=['mn', 'hu', 'es', 'fr'])
    parser.add_argument('--output-dir', default='data/ref', help='Output directory')
    
    args = parser.parse_args()
    
    tsv_path = Path(args.tsv_file)
    if not tsv_path.exists():
        print(f"❌ TSV file not found: {tsv_path}")
        return
    
    matched = extract_transcripts(tsv_path, args.lang, args.output_dir)
    
    print("\n" + "="*60)
    print("✅ EXTRACTION COMPLETE")
    print("="*60)
    print(f"\nExtracted {matched} transcripts for {args.lang.upper()}")
    print(f"\nNext: Repeat for other languages (hu, es, fr)")
    print(f"Then run: python scripts/calculate_wer_cer.py")

if __name__ == '__main__':
    main()
