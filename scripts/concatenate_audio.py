#!/usr/bin/env python3
"""
Create long-form audio samples by concatenating Common Voice clips.
Used to test long-form drift in ASR systems.
"""

import soundfile as sf
import numpy as np
from pathlib import Path
import random
import json
import torchaudio

def convert_mp3_to_wav(mp3_file):
    """Convert MP3 to WAV format"""
    wav_file = mp3_file.with_suffix('.wav')
    if wav_file.exists():
        return wav_file
        
    # Convert using torchaudio
    try:
        audio, sr = torchaudio.load(mp3_file)
        torchaudio.save(wav_file, audio, sr)
        return wav_file
    except Exception as e:
        print(f"Error converting {mp3_file}: {e}")
        return None

def concatenate_audio_files(input_files, output_path, target_duration=120):
    """
    Concatenate audio files until reaching target duration (in seconds)
    Returns the concatenated audio and combined transcript
    """
    combined_audio = []
    combined_transcript = []
    total_duration = 0
    files_used = []
    
    for audio_file in input_files:
        # Convert MP3 to WAV if needed
        if audio_file.suffix.lower() == '.mp3':
            wav_file = convert_mp3_to_wav(audio_file)
            if wav_file is None:
                continue
            audio_file = wav_file
            
        # Read audio
        audio, sr = sf.read(audio_file)
        duration = len(audio) / sr
        
        # Read corresponding transcript
        # Get transcript path
        wav_dir = Path("data/wav")
        ref_dir = Path("results/transcripts/hinted/whisper")
        transcript_file = ref_dir / audio_file.parent.name / f"{audio_file.stem}.txt"
        if not transcript_file.exists():
            print(f"Warning: No transcript found at {transcript_file}")
            continue
            
        with open(transcript_file, 'r') as f:
            transcript = f.read().strip()
            
        combined_audio.append(audio)
        combined_transcript.append(transcript)
        files_used.append(audio_file.name)
        
        total_duration += duration
        if total_duration >= target_duration:
            break
    
    # Check if we have any valid files
    if not combined_audio:
        print("No valid files with transcripts found")
        return None
        
    # Concatenate audio
    final_audio = np.concatenate(combined_audio)
    
    # Save audio
    sf.write(output_path, final_audio, sr)
    
    # Save metadata
    metadata = {
        "duration_seconds": total_duration,
        "num_segments": len(files_used),
        "source_files": files_used,
        "transcripts": combined_transcript
    }
    
    return metadata

def create_long_form_samples(wav_dir="data/wav", out_dir="data/long_form", 
                           durations=[120, 180, 240], samples_per_duration=3):
    """
    Create long-form samples for each language by concatenating shorter clips
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    
    for lang in ['mn', 'hu', 'es', 'fr']:
        print(f"\nProcessing {lang.upper()}...")
        lang_dir = Path(wav_dir) / lang
        
        if not lang_dir.exists():
            print(f"❌ No data found for {lang}")
            continue
            
        # Get all wav files
        wav_files = list(lang_dir.glob("*.wav"))
        if not wav_files:
            print(f"❌ No WAV files found in {lang_dir}")
            continue
            
        print(f"Found {len(wav_files)} source files")
        
        # Create samples for each duration
        for duration in durations:
            print(f"\nCreating {samples_per_duration} samples of {duration}s...")
            
            for i in range(samples_per_duration):
                # Randomly shuffle files for each sample
                random.shuffle(wav_files)
                
                out_name = f"{lang}_long_{duration}s_{i+1}"
                out_path = out_dir / f"{out_name}.wav"
                
                metadata = concatenate_audio_files(
                    wav_files, 
                    out_path,
                    target_duration=duration
                )
                
                if metadata is None:
                    print(f"❌ Failed to create {out_name}")
                    continue
                
                # Save metadata
                with open(out_dir / f"{out_name}.json", 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"✓ Created {out_name}")

def main():
    print("="*60)
    print("Long-form Audio Creator")
    print("Creates extended audio samples by concatenating Common Voice clips")
    print("="*60)
    
    create_long_form_samples()

if __name__ == "__main__":
    main()
