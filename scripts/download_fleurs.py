#!/usr/bin/env python3
"""
Download FLEURS dataset as alternative to Common Voice
Smaller, cleaner, better structured
"""

from datasets import load_dataset
import soundfile as sf
import os

LANGS = {
    "es": "es_419",  # Spanish (Latin America)
    "fr": "fr_fr",   # French
    "hu": "hu_hu",   # Hungarian
}

# Check if Mongolian is available
AVAILABLE_LANGS = [
    "es_419", "fr_fr", "hu_hu",  # Confirmed available
    # Mongolian variants to try:
    "mn_mn", "mon", "mongolian"
]

def check_fleurs_languages():
    """Check what languages are available"""
    print("="*60)
    print("FLEURS Dataset Language Check")
    print("="*60)
    
    try:
        # Load dataset info
        from datasets import get_dataset_config_names
        configs = get_dataset_config_names("google/fleurs")
        
        print(f"\nTotal languages available: {len(configs)}")
        
        # Check our needed languages
        needed = ["Spanish", "French", "Hungarian", "Mongolian"]
        codes = ["es_419", "fr_fr", "hu_hu", "mn_mn"]
        
        print("\nChecking our languages:")
        for name, code in zip(needed, codes):
            if code in configs:
                print(f"  ✅ {name} ({code}) - Available!")
            else:
                # Try to find it
                matches = [c for c in configs if name.lower()[:2] in c.lower()]
                if matches:
                    print(f"  ⚠️  {name} - Found as: {matches}")
                else:
                    print(f"  ❌ {name} ({code}) - Not found")
        
        print(f"\nAll available language codes:")
        for i, config in enumerate(sorted(configs), 1):
            print(f"  {i}. {config}")
            
    except Exception as e:
        print(f"Error: {e}")

def download_fleurs_language(lang_code, num_samples=1000):
    """Download samples from FLEURS"""
    print(f"\n{'='*60}")
    print(f"Downloading FLEURS: {lang_code}")
    print(f"{'='*60}")
    
    try:
        # Load test split
        ds = load_dataset("google/fleurs", lang_code, split="test", streaming=True)
        
        lang_short = lang_code.split('_')[0]
        os.makedirs(f"data/wav/{lang_short}", exist_ok=True)
        os.makedirs(f"data/ref/{lang_short}", exist_ok=True)
        
        count = 0
        for i, example in enumerate(ds):
            if count >= num_samples:
                break
            
            try:
                audio = example["audio"]["array"]
                sr = example["audio"]["sampling_rate"]
                text = example["transcription"].strip()
                
                if len(audio) < 1000 or not text:
                    continue
                
                filename = f"{lang_short}{count+1:04d}"
                
                # Save audio
                wav_path = f"data/wav/{lang_short}/{filename}.wav"
                sf.write(wav_path, audio, sr)
                
                # Save text
                ref_path = f"data/ref/{lang_short}/{filename}.txt"
                with open(ref_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                count += 1
                
                if count % 50 == 0:
                    print(f"  Progress: {count}/{num_samples}")
                    
            except Exception as e:
                print(f"  Warning: Skipped sample: {e}")
                continue
        
        print(f"  ✅ Downloaded {count} samples")
        return count
        
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return 0

def main():
    print("="*60)
    print("FLEURS Dataset Downloader")
    print("Alternative to Common Voice - Smaller & Cleaner")
    print("="*60)
    
    # First, check what's available
    check_fleurs_languages()
    
    print("\n" + "="*60)
    print("Would you like to proceed with download? (y/n)")
    response = input().strip().lower()
    
    if response == 'y':
        total = 0
        for lang_code in ["es_419", "fr_fr", "hu_hu"]:
            count = download_fleurs_language(lang_code, num_samples=1000)
            total += count
        
        print("\n" + "="*60)
        print(f"Total samples downloaded: {total}")
        print("="*60)

if __name__ == "__main__":
    main()
