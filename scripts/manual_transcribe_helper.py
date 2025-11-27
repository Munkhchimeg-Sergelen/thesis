#!/usr/bin/env python3
"""
Interactive manual transcription helper
Plays audio and lets you type the transcript
"""

import os
import sys
from pathlib import Path
import subprocess

def play_audio(audio_file):
    """Play audio file using available player"""
    try:
        # Try different audio players
        if sys.platform == 'darwin':  # Mac
            subprocess.run(['afplay', audio_file])
        elif sys.platform == 'linux':
            subprocess.run(['mpg123', '-q', audio_file])
        else:
            print("  ⚠️  Auto-play not available, play manually")
    except:
        print("  ⚠️  Could not play audio automatically")

def transcribe_files(lang, start_idx=1, end_idx=100):
    """Interactive transcription session"""
    audio_dir = Path(f"data/wav/{lang}")
    ref_dir = Path(f"data/ref/{lang}")
    ref_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print(f"MANUAL TRANSCRIPTION: {lang.upper()}")
    print("="*60)
    print(f"Files: {start_idx} to {end_idx}")
    print("\nCommands:")
    print("  [Type transcript] - Save and continue")
    print("  'r' - Replay audio")
    print("  's' - Skip this file")
    print("  'q' - Quit")
    print("="*60)
    
    for i in range(start_idx, end_idx + 1):
        filename = f"{lang}{i:04d}"
        audio_file = audio_dir / f"{filename}.mp3"
        ref_file = ref_dir / f"{filename}.txt"
        
        # Skip if already transcribed
        if ref_file.exists():
            print(f"\n[{i}/{end_idx}] {filename} - Already done ✓")
            continue
        
        if not audio_file.exists():
            print(f"\n[{i}/{end_idx}] {filename} - Audio not found ✗")
            continue
        
        print(f"\n[{i}/{end_idx}] {filename}")
        print("  Playing audio...")
        play_audio(str(audio_file))
        
        while True:
            transcript = input("  Transcript: ").strip()
            
            if transcript.lower() == 'q':
                print("\n✓ Saved progress. Resume with: python manual_transcribe_helper.py --lang {lang} --start {i}")
                return i
            elif transcript.lower() == 's':
                print("  Skipped")
                break
            elif transcript.lower() == 'r':
                print("  Replaying...")
                play_audio(str(audio_file))
                continue
            elif transcript:
                # Save transcript
                with open(ref_file, 'w', encoding='utf-8') as f:
                    f.write(transcript)
                print("  Saved ✓")
                break
            else:
                print("  (Empty - press 'r' to replay, 's' to skip, or type transcript)")
    
    print(f"\n✅ Completed {lang.upper()}!")
    return end_idx

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Manual transcription helper')
    parser.add_argument('--lang', required=True, choices=['mn', 'hu', 'es', 'fr'])
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=100)
    
    args = parser.parse_args()
    
    # Check for audio player
    if sys.platform == 'linux':
        try:
            subprocess.run(['which', 'mpg123'], capture_output=True, check=True)
        except:
            print("⚠️  Warning: mpg123 not found. Install with: sudo apt-get install mpg123")
            print("You'll need to play audio manually.\n")
    
    last_completed = transcribe_files(args.lang, args.start, args.end)
    
    print("\n" + "="*60)
    print("PROGRESS SUMMARY")
    print("="*60)
    
    ref_dir = Path(f"data/ref/{args.lang}")
    completed = len(list(ref_dir.glob("*.txt"))) if ref_dir.exists() else 0
    print(f"{args.lang.upper()}: {completed}/100 files transcribed")

if __name__ == '__main__':
    main()
