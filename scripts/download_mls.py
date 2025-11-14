#!/usr/bin/env python3
"""
Download from Multilingual LibriSpeech - smaller, cleaner alternative
"""

from datasets import load_dataset
import soundfile as sf
import os

def download_mls_language(lang, num_samples=1000):
    """
    Download MLS samples
    Languages: spanish, french, german, dutch, polish, portuguese, italian
    """
    print(f"\n{'='*60}")
    print(f"Downloading MLS: {lang}")
    print(f"{'='*60}")
    
    try:
        # Load test split with streaming
        print("Loading dataset...")
        ds = load_dataset(
            "facebook/multilingual_librispeech",
            lang,
            split="test",
            streaming=True
        )
        
        os.makedirs(f"data/wav/{lang[:2]}", exist_ok=True)
        os.makedirs(f"data/ref/{lang[:2]}", exist_ok=True)
        
        count = 0
        print(f"Processing up to {num_samples} samples...")
        
        for i, example in enumerate(ds):
            if count >= num_samples:
                break
            
            try:
                audio = example["audio"]["array"]
                sr = example["audio"]["sampling_rate"]
                text = example["transcript"].strip()
                
                if len(audio) < 1000 or not text:
                    continue
                
                lang_code = lang[:2]
                filename = f"{lang_code}{count+1:04d}"
                
                # Save audio
                wav_path = f"data/wav/{lang_code}/{filename}.wav"
                sf.write(wav_path, audio, sr)
                
                # Save text
                ref_path = f"data/ref/{lang_code}/{filename}.txt"
                with open(ref_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                count += 1
                
                if count % 100 == 0:
                    print(f"  Progress: {count}/{num_samples}")
                    
            except Exception as e:
                continue
        
        print(f"✅ {lang}: Downloaded {count} samples")
        return count
        
    except Exception as e:
        print(f"❌ {lang}: Failed - {e}")
        return 0

def main():
    print("="*60)
    print("Multilingual LibriSpeech Downloader")
    print("Smaller alternative to Common Voice")
    print("="*60)
    print("\nThis will download Spanish and French from MLS")
    print("Using streaming mode - no huge downloads!")
    print("Estimated time: 30-60 minutes")
    print("\nPress Ctrl+C to cancel, or wait 5 seconds...")
    
    import time
    time.sleep(5)
    
    total = 0
    
    # Download Spanish
    count = download_mls_language("spanish", num_samples=1000)
    total += count
    
    # Download French  
    count = download_mls_language("french", num_samples=1000)
    total += count
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total samples downloaded: {total}")
    print("\nFiles saved to:")
    print("  data/wav/es/ and data/wav/fr/")
    print("  data/ref/es/ and data/ref/fr/")
    print("="*60)

if __name__ == "__main__":
    main()
