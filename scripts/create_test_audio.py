#!/usr/bin/env python3
"""Generate simple test audio files for quick testing"""
import numpy as np
import soundfile as sf
import os

def generate_tone(duration_sec=3.0, freq=440.0, sr=16000):
    """Generate a simple sine wave tone"""
    t = np.linspace(0, duration_sec, int(sr * duration_sec))
    audio = 0.3 * np.sin(2 * np.pi * freq * t)
    return audio, sr

def main():
    os.makedirs("data/wav/test", exist_ok=True)
    os.makedirs("data/ref/test", exist_ok=True)
    
    # Create simple test files
    langs = ["mn", "hu", "fr", "es"]
    for lang in langs:
        os.makedirs(f"data/wav/{lang}", exist_ok=True)
        os.makedirs(f"data/ref/{lang}", exist_ok=True)
        
        # Generate a test tone
        audio, sr = generate_tone(duration_sec=5.0, freq=440 + langs.index(lang) * 50)
        
        # Save
        wav_path = f"data/wav/{lang}/{lang}_test.wav"
        sf.write(wav_path, audio, sr)
        
        # Create empty reference
        ref_path = f"data/ref/{lang}/{lang}_test.txt"
        with open(ref_path, "w", encoding="utf-8") as f:
            f.write(f"test audio for {lang}")
        
        print(f"Created: {wav_path}")
    
    print("✓ Test audio files created")

if __name__ == "__main__":
    main()
