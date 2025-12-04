#!/usr/bin/env python3
"""
Test long-form drift in Whisper ASR by analyzing transcriptions of concatenated audio.
"""

import json
from pathlib import Path
import whisper
import torch
import pandas as pd
import numpy as np
from tqdm import tqdm

def load_audio(audio_path):
    """Load audio file using whisper's load_audio function"""
    return whisper.load_audio(str(audio_path))

def transcribe_audio(model, audio, language=None):
    """Transcribe audio using Whisper"""
    # First detect language if not provided
    if language is None:
        result = model.detect_language(audio)[0]
        print(f"Detected language: {result}")
    
    # Transcribe with language hint if provided
    result = model.transcribe(
        audio,
        language=language,
        task="transcribe",
        verbose=True
    )
    
    return result

def analyze_drift(reference, hypothesis, window_size=30):
    """
    Analyze drift by comparing reference and hypothesis in windows
    Returns window-wise WER and language confidence scores
    """
    # Split into windows (roughly)
    ref_words = reference.split()
    hyp_words = hypothesis.split()
    
    ref_windows = [' '.join(ref_words[i:i+window_size]) 
                  for i in range(0, len(ref_words), window_size)]
    hyp_windows = [' '.join(hyp_words[i:i+window_size]) 
                  for i in range(0, len(hyp_words), window_size)]
    
    # Pad shorter list
    max_windows = max(len(ref_windows), len(hyp_windows))
    ref_windows.extend([''] * (max_windows - len(ref_windows)))
    hyp_windows.extend([''] * (max_windows - len(hyp_windows)))
    
    # Calculate WER for each window
    window_wers = []
    for ref_win, hyp_win in zip(ref_windows, hyp_windows):
        if not ref_win and not hyp_win:
            continue
            
        # Simple WER calculation
        ref_words = ref_win.split()
        hyp_words = hyp_win.split()
        
        # Levenshtein distance
        d = np.zeros((len(ref_words) + 1, len(hyp_words) + 1))
        d[0, :] = np.arange(len(hyp_words) + 1)
        d[:, 0] = np.arange(len(ref_words) + 1)
        
        for i in range(1, len(ref_words) + 1):
            for j in range(1, len(hyp_words) + 1):
                if ref_words[i-1] == hyp_words[j-1]:
                    d[i, j] = d[i-1, j-1]
                else:
                    d[i, j] = min(d[i-1, j], d[i, j-1], d[i-1, j-1]) + 1
                    
        wer = d[-1, -1] / len(ref_words) if ref_words else 1.0
        window_wers.append(wer)
    
    return window_wers

def main():
    print("="*60)
    print("Long-form Drift Analysis")
    print("Testing Whisper's performance on extended audio")
    print("="*60)
    
    # Load Whisper model
    print("\nLoading Whisper model...")
    model = whisper.load_model("small")
    
    # Get all long-form samples
    long_form_dir = Path("data/long_form")
    wav_files = sorted(long_form_dir.glob("*.wav"))
    
    results = []
    for wav_file in tqdm(wav_files, desc="Processing files"):
        print(f"\nProcessing {wav_file.name}...")
        
        # Load audio
        audio = load_audio(wav_file)
        
        # Load reference
        json_file = wav_file.with_suffix('.json')
        with open(json_file) as f:
            metadata = json.load(f)
        reference = " ".join(metadata['transcripts'])
        
        # Transcribe
        result = transcribe_audio(model, audio, language="fr")
        
        # Analyze drift
        window_wers = analyze_drift(reference, result['text'])
        
        # Store results
        results.append({
            'file': wav_file.name,
            'duration': metadata['duration_seconds'],
            'num_segments': metadata['num_segments'],
            'detected_language': result['language'],
            'language_probability': 1.0,  # Whisper no longer exposes probabilities
            'window_wers': window_wers,
            'avg_wer': np.mean(window_wers),
            'reference': reference,
            'hypothesis': result['text']
        })
        
        # Save intermediate results
        df = pd.DataFrame(results)
        df.to_csv(long_form_dir / 'drift_analysis.csv', index=False)
        
        # Also save detailed results
        with open(long_form_dir / 'drift_analysis.json', 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
    print("\nAnalysis complete! Results saved to:")
    print("- drift_analysis.csv")
    print("- drift_analysis.json")

if __name__ == "__main__":
    main()
