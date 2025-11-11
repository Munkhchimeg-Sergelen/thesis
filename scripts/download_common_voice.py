#!/usr/bin/env python3
"""
Download audio samples from Common Voice for thesis evaluation
Works with Mozilla Common Voice 17.0 (latest at time of writing)
"""
import os
import sys

try:
    from datasets import load_dataset
    import soundfile as sf
except ImportError:
    print("ERROR: Missing dependencies")
    print("Run: pip install datasets soundfile")
    sys.exit(1)

# Common Voice language codes
LANGS = {
    "mn": "mn",      # Mongolian
    "hu": "hu",      # Hungarian
    "fr": "fr",      # French
    "es": "es",      # Spanish
}

def slug(text, max_len=40):
    """Create safe filename from text"""
    import re
    if not text:
        return "sample"
    safe = re.sub(r'[^a-zA-Z0-9_-]+', '_', str(text))
    return safe[:max_len]

def download_language(lang, cv_code, num_samples=15):
    """Download samples for one language"""
    print(f"\n{'='*50}")
    print(f"Downloading {lang.upper()} ({cv_code})")
    print(f"{'='*50}")
    
    # Create directories
    os.makedirs(f"data/wav/{lang}", exist_ok=True)
    os.makedirs(f"data/ref/{lang}", exist_ok=True)
    
    try:
        # Load dataset (streaming to avoid downloading everything)
        print(f"Loading Common Voice dataset for {lang}...")
        ds = load_dataset(
            "mozilla-foundation/common_voice_17_0",
            cv_code,
            split=f"test[:{num_samples}]",
            streaming=False
        )
        
        print(f"Processing {num_samples} samples...")
        count = 0
        
        for i, example in enumerate(ds):
            # Get audio
            audio_array = example["audio"]["array"]
            sample_rate = example["audio"]["sampling_rate"]
            
            # Get text
            text = example.get("sentence", "").strip()
            
            # Create filename
            client_id = slug(example.get("client_id", f"sample{i}"))
            filename = f"{lang}{i+1:02d}_{client_id}"
            
            # Save audio
            wav_path = f"data/wav/{lang}/{filename}.wav"
            sf.write(wav_path, audio_array, sample_rate)
            
            # Save reference
            ref_path = f"data/ref/{lang}/{filename}.txt"
            with open(ref_path, "w", encoding="utf-8") as f:
                f.write(text)
            
            count += 1
            print(f"  [{count}/{num_samples}] {filename}.wav ({len(text)} chars)")
        
        print(f"✓ {lang.upper()}: Downloaded {count} samples")
        return count
    
    except Exception as e:
        print(f"✗ {lang.upper()}: Failed - {e}")
        return 0

def main():
    print("=" * 50)
    print("Common Voice Downloader for Thesis")
    print("=" * 50)
    print("\nThis will download ~15 audio samples per language")
    print("Languages: Mongolian (MN), Hungarian (HU), French (FR), Spanish (ES)")
    print("\nEstimated download: ~50-100 MB")
    print("\nNote: First run may take longer as datasets cache.")
    print("=" * 50)
    print("\nStarting download...")
    print()
    
    total = 0
    successful = 0
    
    for lang, cv_code in LANGS.items():
        count = download_language(lang, cv_code, num_samples=15)
        if count > 0:
            successful += 1
            total += count
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Languages successful: {successful}/{len(LANGS)}")
    print(f"Total samples: {total}")
    print("\nAudio saved to: data/wav/{lang}/")
    print("References saved to: data/ref/{lang}/")
    
    if total == 0:
        print("\n⚠️  ERROR: No data downloaded!")
        print("Check internet connection and try again.")
        sys.exit(1)
    
    print("\n✅ Ready for evaluation!")
    print("\nNext steps:")
    print("  1. Verify files: ls data/wav/*/*.wav | wc -l")
    print("  2. Run comparison: ./scripts/run_comparison_batch.sh")

if __name__ == "__main__":
    main()
