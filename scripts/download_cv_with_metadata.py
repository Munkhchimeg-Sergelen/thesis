#!/usr/bin/env python3
"""
Download Common Voice with proper metadata tracking
Preserves mapping between renamed files and original transcripts
"""

import os
import csv
from pathlib import Path
from datasets import load_dataset
import soundfile as sf
import json

LANGS = {
    "mn": "mn",
    "hu": "hu", 
    "es": "es",
    "fr": "fr",
}

VERSIONS = [
    "mozilla-foundation/common_voice_17_0",
    "mozilla-foundation/common_voice_13_0",
]

def download_with_metadata(lang, cv_code, num_samples=1000):
    """Download samples and save metadata mapping"""
    
    print(f"\n{'='*60}")
    print(f"Downloading {lang.upper()} with metadata")
    print(f"{'='*60}")
    
    # Create directories
    audio_dir = Path(f"data/wav_new/{lang}")
    ref_dir = Path(f"data/ref_new/{lang}")
    audio_dir.mkdir(parents=True, exist_ok=True)
    ref_dir.mkdir(parents=True, exist_ok=True)
    
    # Try versions
    for version in VERSIONS:
        try:
            print(f"Trying {version}...")
            ds = load_dataset(version, cv_code, split="test", streaming=False)
            print(f"✓ Loaded dataset: {len(ds)} samples")
            
            # Get subset
            samples_to_get = min(num_samples, len(ds))
            ds_subset = ds.select(range(samples_to_get))
            
            print(f"Processing {samples_to_get} samples...")
            
            metadata = []
            count = 0
            
            for i, example in enumerate(ds_subset):
                try:
                    # Get audio data
                    audio_array = example["audio"]["array"]
                    sample_rate = example["audio"]["sampling_rate"]
                    
                    # Get transcript
                    transcript = example.get("sentence", "").strip()
                    
                    # Get original path if available
                    original_path = example.get("path", f"sample_{i}")
                    
                    # Our renamed filename
                    our_filename = f"{lang}{i+1:04d}"
                    
                    # Save audio as MP3 (to match existing files)
                    audio_path = audio_dir / f"{our_filename}.mp3"
                    # Note: sf.write doesn't support MP3, so save as WAV
                    # You'll need to convert or use original MP3s
                    wav_path = audio_dir / f"{our_filename}.wav"
                    sf.write(str(wav_path), audio_array, sample_rate)
                    
                    # Save transcript
                    ref_path = ref_dir / f"{our_filename}.txt"
                    with open(ref_path, 'w', encoding='utf-8') as f:
                        f.write(transcript)
                    
                    # Save metadata
                    metadata.append({
                        'our_filename': our_filename,
                        'original_path': original_path,
                        'transcript': transcript,
                        'index': i,
                    })
                    
                    count += 1
                    if (count % 100) == 0:
                        print(f"  Processed {count}/{samples_to_get}")
                
                except Exception as e:
                    print(f"  Warning: Failed on sample {i}: {e}")
            
            # Save metadata mapping
            metadata_file = Path(f"data/metadata_{lang}.json")
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"\n✓ Downloaded {count} samples")
            print(f"✓ Saved metadata: {metadata_file}")
            print(f"✓ Audio: {audio_dir}/")
            print(f"✓ Transcripts: {ref_dir}/")
            
            return count
            
        except Exception as e:
            print(f"  Failed with {version}: {e}")
            continue
    
    print(f"❌ Could not download {lang}")
    return 0

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', required=True, choices=['mn', 'hu', 'es', 'fr'])
    parser.add_argument('--num-samples', type=int, default=1000)
    
    args = parser.parse_args()
    
    print("="*60)
    print("COMMON VOICE DOWNLOAD WITH METADATA")
    print("="*60)
    
    lang = args.lang
    cv_code = LANGS[lang]
    
    count = download_with_metadata(lang, cv_code, args.num_samples)
    
    if count > 0:
        print("\n" + "="*60)
        print("✅ DOWNLOAD COMPLETE")
        print("="*60)
        print(f"\nNext steps:")
        print(f"1. Replace old audio files:")
        print(f"   mv data/wav/{lang} data/wav/{lang}_old")
        print(f"   mv data/wav_new/{lang} data/wav/{lang}")
        print(f"2. Replace old references:")
        print(f"   mv data/ref/{lang} data/ref/{lang}_old")
        print(f"   mv data/ref_new/{lang} data/ref/{lang}")
        print(f"3. Re-run ASR models on new audio")
        print(f"4. Run WER/CER calculation")
    else:
        print("\n❌ Download failed")

if __name__ == '__main__':
    main()
