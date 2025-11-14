#!/usr/bin/env python3
"""
Simple Common Voice downloader - tries multiple dataset versions
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

LANGS = {
    "mn": "mn",  # Mongolian
    "hu": "hu",  # Hungarian
    "fr": "fr",  # French
    "es": "es",  # Spanish
}

# Try different Common Voice versions
VERSIONS_TO_TRY = [
    "mozilla-foundation/common_voice_13_0",
    "mozilla-foundation/common_voice_11_0",
    "mozilla-foundation/common_voice_9_0",
]

def download_language(lang, cv_code, num_samples=1000):
    """Download samples for one language"""
    print(f"\n{'='*50}")
    print(f"Downloading {lang.upper()} ({cv_code})")
    print(f"{'='*50}")
    
    os.makedirs(f"data/wav/{lang}", exist_ok=True)
    os.makedirs(f"data/ref/{lang}", exist_ok=True)
    
    # Try different versions
    for version in VERSIONS_TO_TRY:
        try:
            print(f"Trying {version}...")
            ds = load_dataset(
                version,
                cv_code,
                split="test"
            )
            print(f"✓ Found dataset! Total samples available: {len(ds)}")
            
            # Select subset
            samples_to_get = min(num_samples, len(ds))
            ds = ds.select(range(samples_to_get))
            
            print(f"Downloading {samples_to_get} samples...")
            count = 0
            
            for i, example in enumerate(ds):
                try:
                    audio_array = example["audio"]["array"]
                    sample_rate = example["audio"]["sampling_rate"]
                    text = example.get("sentence", "").strip()
                    
                    filename = f"{lang}{i+1:04d}"
                    
                    # Save audio
                    wav_path = f"data/wav/{lang}/{filename}.wav"
                    sf.write(wav_path, audio_array, sample_rate)
                    
                    # Save reference
                    ref_path = f"data/ref/{lang}/{filename}.txt"
                    with open(ref_path, "w", encoding="utf-8") as f:
                        f.write(text)
                    
                    count += 1
                    if (count % 100) == 0:
                        print(f"  Progress: {count}/{samples_to_get}")
                        
                except Exception as e:
                    print(f"  Warning: Skipped sample {i}: {e}")
                    continue
            
            print(f"✓ {lang.upper()}: Downloaded {count} samples")
            return count
            
        except Exception as e:
            print(f"  ✗ {version} failed: {e}")
            continue
    
    print(f"✗ {lang.upper()}: Could not download from any version")
    return 0

def main():
    print("=" * 50)
    print("Common Voice Downloader (Multi-Version)")
    print("=" * 50)
    print("\nWill try multiple Common Voice versions")
    print(f"Target: ~1000 samples per language")
    print("=" * 50)
    
    total = 0
    successful = 0
    
    for lang, cv_code in LANGS.items():
        count = download_language(lang, cv_code, num_samples=1000)
        if count > 0:
            successful += 1
            total += count
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Languages successful: {successful}/{len(LANGS)}")
    print(f"Total samples: {total}")
    
    if total == 0:
        print("\n❌ ERROR: No data downloaded!")
        print("This might be a Hugging Face access issue.")
        print("Try: huggingface-cli login")
        sys.exit(1)
    
    print("\n✅ Download complete!")
    print(f"Files saved to: data/wav/ and data/ref/")

if __name__ == "__main__":
    main()
