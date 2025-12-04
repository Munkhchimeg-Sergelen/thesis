#!/usr/bin/env python3
"""
Download FLEURS dataset as alternative to Common Voice
Smaller, cleaner, better structured
"""

from datasets import load_dataset, Audio
import torch
import torchaudio
import os
import numpy as np

def check_fleurs_languages():
    """Check what languages are available"""
    print("="*60)
    print("FLEURS Dataset Language Check")
    print("="*60)
    
    try:
        # Load a small subset to verify
        ds = load_dataset("google/fleurs", "es_419", split="test", streaming=True)
        sample = next(iter(ds))
        print(f"\nDataset verified!")
        print(f"Features: {list(sample.keys())}")
        print(f"\nAudio format: {sample['audio']}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def download_fleurs_language(lang_code, num_samples=1000):
    """Download samples from FLEURS"""
    print(f"\n{'='*60}")
    print(f"Downloading FLEURS: {lang_code}")
    print(f"{'='*60}")
    
    try:
        # Load dataset
        ds = load_dataset("google/fleurs", lang_code, split="test", streaming=True)
        ds = ds.cast_column("audio", Audio(sampling_rate=16000))
        
        lang_short = lang_code.split('_')[0]
        os.makedirs(f"data/wav/{lang_short}", exist_ok=True)
        os.makedirs(f"data/ref/{lang_short}", exist_ok=True)
        
        count = 0
        for i, example in enumerate(ds):
            if count >= num_samples:
                break
                
            try:
                # Get audio array
                audio = example["audio"]["array"]
                sr = example["audio"]["sampling_rate"]
                text = example["transcription"].strip()
                
                if len(audio) < 1000 or not text:
                    continue
                    
                # Save audio
                filename = f"{lang_short}{count+1:04d}"
                wav_path = f"data/wav/{lang_short}/{filename}.wav"
                torchaudio.save(wav_path, torch.from_numpy(audio).reshape(1, -1), sr)
                
                # Save transcript
                ref_path = f"data/ref/{lang_short}/{filename}.txt"
                with open(ref_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                    
                count += 1
                if count % 10 == 0:
                    print(f"Progress: {count}/{num_samples}")
                    
            except Exception as e:
                print(f"Error processing sample {i}: {e}")
                continue
                
        print(f"✓ Downloaded {count} samples")
        return count
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return 0

def main():
    print("="*60)
    print("FLEURS Dataset Downloader")
    print("Alternative to Common Voice - Smaller & Cleaner")
    print("="*60)
    
    # First, check what's available
    if not check_fleurs_languages():
        print("Failed to check FLEURS dataset. Exiting.")
        return
    
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
