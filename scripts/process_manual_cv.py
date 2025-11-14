#!/usr/bin/env python3
"""
Process manually downloaded Common Voice datasets
Extracts 1000 samples from test.tsv for each language
"""

import os
import sys
import csv
import shutil
from pathlib import Path

def process_language(cv_dir, lang_code, num_samples=1000):
    """
    Process one Common Voice language directory
    
    Args:
        cv_dir: Path to extracted CV corpus (e.g., ~/Downloads/cv-corpus-13.0-2023-03-09-es/)
        lang_code: Language code (es, fr, hu, mn)
        num_samples: Number of samples to extract
    """
    cv_path = Path(cv_dir)
    
    # Find test.tsv
    test_tsv = cv_path / "test.tsv"
    if not test_tsv.exists():
        print(f"❌ {lang_code.upper()}: test.tsv not found in {cv_dir}")
        return 0
    
    # Find clips directory
    clips_dir = cv_path / "clips"
    if not clips_dir.exists():
        print(f"❌ {lang_code.upper()}: clips/ directory not found in {cv_dir}")
        return 0
    
    print(f"\n{'='*60}")
    print(f"Processing {lang_code.upper()} from {cv_path.name}")
    print(f"{'='*60}")
    
    # Create output directories
    os.makedirs(f"data/wav/{lang_code}", exist_ok=True)
    os.makedirs(f"data/ref/{lang_code}", exist_ok=True)
    
    # Read test.tsv
    samples_processed = 0
    samples_copied = 0
    
    with open(test_tsv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        
        for i, row in enumerate(reader):
            if samples_copied >= num_samples:
                break
            
            # Get audio filename and text
            audio_file = row.get('path', row.get('clip', ''))
            text = row.get('sentence', '').strip()
            
            if not audio_file or not text:
                continue
            
            # Source audio file (MP3)
            source_path = clips_dir / audio_file
            
            if not source_path.exists():
                samples_processed += 1
                continue
            
            # Destination (convert to WAV or keep as MP3)
            dest_filename = f"{lang_code}{samples_copied+1:04d}"
            
            # Copy MP3 (we can convert later if needed)
            dest_audio = f"data/wav/{lang_code}/{dest_filename}.mp3"
            shutil.copy2(source_path, dest_audio)
            
            # Save reference text
            dest_ref = f"data/ref/{lang_code}/{dest_filename}.txt"
            with open(dest_ref, 'w', encoding='utf-8') as ref_f:
                ref_f.write(text)
            
            samples_copied += 1
            samples_processed += 1
            
            if samples_copied % 100 == 0:
                print(f"  Progress: {samples_copied}/{num_samples} samples")
    
    print(f"✓ {lang_code.upper()}: Extracted {samples_copied} samples from {samples_processed} processed")
    return samples_copied

def convert_mp3_to_wav(data_dir='data/wav'):
    """
    Optional: Convert MP3 files to WAV using ffmpeg
    Only run if you have ffmpeg installed
    """
    import subprocess
    
    print("\n" + "="*60)
    print("Converting MP3 to WAV (requires ffmpeg)")
    print("="*60)
    
    data_path = Path(data_dir)
    mp3_files = list(data_path.rglob('*.mp3'))
    
    if not mp3_files:
        print("No MP3 files found to convert")
        return
    
    print(f"Found {len(mp3_files)} MP3 files")
    
    # Check if ffmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  ffmpeg not found. Install with: brew install ffmpeg")
        print("Keeping MP3 files (Whisper can process MP3 directly)")
        return
    
    converted = 0
    for mp3_file in mp3_files:
        wav_file = mp3_file.with_suffix('.wav')
        
        try:
            subprocess.run([
                'ffmpeg', '-i', str(mp3_file),
                '-ar', '16000',  # 16kHz sample rate
                '-ac', '1',       # Mono
                '-y',             # Overwrite
                str(wav_file)
            ], capture_output=True, check=True)
            
            # Remove MP3 after successful conversion
            mp3_file.unlink()
            converted += 1
            
            if converted % 100 == 0:
                print(f"  Converted: {converted}/{len(mp3_files)}")
                
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  Failed to convert {mp3_file.name}: {e}")
    
    print(f"✓ Converted {converted}/{len(mp3_files)} files to WAV")

def main():
    if len(sys.argv) < 2:
        print("="*60)
        print("Common Voice Manual Dataset Processor")
        print("="*60)
        print("\nUsage:")
        print("  python scripts/process_manual_cv.py <cv_directories...>")
        print("\nExample:")
        print("  python scripts/process_manual_cv.py \\")
        print("    ~/Downloads/cv-corpus-13.0-2023-03-09-es/ \\")
        print("    ~/Downloads/cv-corpus-13.0-2023-03-09-fr/ \\")
        print("    ~/Downloads/cv-corpus-13.0-2023-03-09-hu/ \\")
        print("    ~/Downloads/cv-corpus-13.0-2023-03-09-mn/")
        print("\nOr use wildcard:")
        print("  python scripts/process_manual_cv.py ~/Downloads/cv-corpus-*/")
        print("\n" + "="*60)
        return
    
    print("="*60)
    print("Common Voice Manual Dataset Processor")
    print("Extracting 1000 samples per language from test.tsv")
    print("="*60)
    
    # Language code mapping (directory name might contain language code)
    lang_map = {
        'es': 'es',
        'fr': 'fr',
        'hu': 'hu',
        'mn': 'mn',
        'spanish': 'es',
        'french': 'fr',
        'hungarian': 'hu',
        'mongolian': 'mn'
    }
    
    total_samples = 0
    processed_langs = []
    
    for cv_dir in sys.argv[1:]:
        cv_path = Path(cv_dir)
        
        if not cv_path.exists():
            print(f"⚠️  Directory not found: {cv_dir}")
            continue
        
        # Try to detect language from directory name
        dir_name_lower = cv_path.name.lower()
        detected_lang = None
        
        for key, lang_code in lang_map.items():
            if key in dir_name_lower:
                detected_lang = lang_code
                break
        
        if not detected_lang:
            print(f"⚠️  Could not detect language from: {cv_path.name}")
            print(f"    Directory name should contain: es, fr, hu, or mn")
            continue
        
        if detected_lang in processed_langs:
            print(f"⚠️  {detected_lang.upper()} already processed, skipping")
            continue
        
        count = process_language(cv_dir, detected_lang, num_samples=1000)
        if count > 0:
            total_samples += count
            processed_langs.append(detected_lang)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Languages processed: {len(processed_langs)}/4")
    print(f"Total samples extracted: {total_samples}")
    
    if total_samples > 0:
        print("\n✓ Data extraction complete!")
        print(f"\nFiles saved to:")
        print(f"  Audio: data/wav/{{lang}}/")
        print(f"  Text:  data/ref/{{lang}}/")
        
        print(f"\nVerify:")
        print(f"  find data/wav -name '*.mp3' -o -name '*.wav' | wc -l")
        
        # Ask about WAV conversion
        print(f"\nNote: Files are in MP3 format.")
        print(f"Whisper can process MP3 directly, or run conversion:")
        print(f"  python scripts/process_manual_cv.py --convert")
    else:
        print("\n❌ No samples extracted!")
        print("\nTroubleshooting:")
        print("  1. Make sure you extracted the .tar.gz files")
        print("  2. Directory should contain test.tsv and clips/")
        print("  3. Directory name should include language code (es, fr, hu, mn)")
    
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == '--convert':
        convert_mp3_to_wav()
    else:
        main()
