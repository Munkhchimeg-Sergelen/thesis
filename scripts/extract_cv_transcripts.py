#!/usr/bin/env python3
"""
Extract reference transcripts from Common Voice dataset
Matches existing audio files by index
"""

import os
from datasets import load_dataset

LANGS = {
    "mn": "mn",  # Mongolian
    "hu": "hu",  # Hungarian
    "fr": "fr",  # French
    "es": "es",  # Spanish
}

VERSIONS = [
    "mozilla-foundation/common_voice_13_0",
    "mozilla-foundation/common_voice_11_0",
    "mozilla-foundation/common_voice_16_1",
]

def extract_transcripts(lang, cv_code, num_samples=1000):
    """Extract transcripts for existing audio files"""
    print(f"\n{'='*60}")
    print(f"Extracting transcripts for {lang.upper()}")
    print(f"{'='*60}")
    
    ref_dir = f"data/ref/{lang}"
    os.makedirs(ref_dir, exist_ok=True)
    
    # Try versions
    for version in VERSIONS:
        try:
            print(f"Trying {version}...")
            ds = load_dataset(version, cv_code, split="test", streaming=False)
            print(f"✓ Loaded dataset: {len(ds)} samples")
            
            # Get the samples we need
            samples_to_get = min(num_samples, len(ds))
            ds_subset = ds.select(range(samples_to_get))
            
            print(f"Extracting {samples_to_get} transcripts...")
            
            for i, example in enumerate(ds_subset):
                text = example.get("sentence", "").strip()
                
                # Save individual file (matches audio filename pattern)
                filename = f"{lang}{i+1:04d}.txt"
                ref_path = os.path.join(ref_dir, filename)
                
                with open(ref_path, "w", encoding="utf-8") as f:
                    f.write(text)
                
                if (i+1) % 100 == 0:
                    print(f"  Progress: {i+1}/{samples_to_get}")
            
            print(f"✓ Saved {samples_to_get} transcripts to {ref_dir}/")
            return True
            
        except Exception as e:
            print(f"  Failed with {version}: {e}")
            continue
    
    print(f"❌ Could not load dataset for {lang}")
    return False

def main():
    print("="*60)
    print("COMMON VOICE TRANSCRIPT EXTRACTION")
    print("="*60)
    
    for lang, cv_code in LANGS.items():
        success = extract_transcripts(lang, cv_code, num_samples=1012)
        if not success:
            print(f"⚠️  Warning: Failed to extract transcripts for {lang}")
    
    print("\n" + "="*60)
    print("✅ Transcript extraction complete!")
    print("="*60)
    
    # Verify
    print("\nVerifying extracted transcripts:")
    for lang in LANGS.keys():
        ref_dir = f"data/ref/{lang}"
        txt_files = len([f for f in os.listdir(ref_dir) if f.endswith('.txt') and not f.endswith('_test.txt')])
        print(f"  {lang}: {txt_files} transcript files")

if __name__ == "__main__":
    main()
