#!/usr/bin/env python3
"""
Match audio files to Common Voice references using audio duration
Finds correct references for existing audio files without re-running ASR
"""

import csv
import json
from pathlib import Path
import librosa
import argparse

def get_audio_duration(audio_file):
    """Get audio duration in seconds"""
    try:
        duration = librosa.get_duration(path=str(audio_file))
        return round(duration, 3)  # Round to milliseconds
    except Exception as e:
        print(f"Error reading {audio_file}: {e}")
        return None

def match_by_duration(lang, tsv_file, audio_dir, cv_clips_dir, output_dir):
    """Match audio files using duration"""
    
    print(f"\n{'='*60}")
    print(f"Duration-based matching for {lang.upper()}")
    print(f"{'='*60}")
    
    # Load TSV with paths and transcripts
    print(f"Loading TSV: {tsv_file}")
    cv_data = {}
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            path = row.get('path', '')
            sentence = row.get('sentence', '').strip()
            if path and sentence:
                cv_data[path] = sentence
    
    print(f"✓ Loaded {len(cv_data)} CV entries")
    
    # Get durations of CV clips
    print(f"Reading CV clip durations from {cv_clips_dir}...")
    cv_durations = {}
    cv_clips_path = Path(cv_clips_dir)
    
    if not cv_clips_path.exists():
        print(f"❌ CV clips directory not found: {cv_clips_dir}")
        return 0
    
    clip_files = list(cv_clips_path.glob("*.mp3"))
    print(f"Found {len(clip_files)} CV clip files")
    
    for i, clip_file in enumerate(clip_files):
        duration = get_audio_duration(clip_file)
        if duration:
            cv_durations[clip_file.name] = duration
        
        if (i + 1) % 1000 == 0:
            print(f"  Processed {i+1} CV clips...")
    
    print(f"✓ Got durations for {len(cv_durations)} CV clips")
    
    # Match our audio files
    print(f"\nMatching our audio files from {audio_dir}...")
    audio_path = Path(audio_dir)
    our_files = sorted(audio_path.glob("*.mp3"))
    
    matches = []
    matched_count = 0
    
    for our_file in our_files:
        our_duration = get_audio_duration(our_file)
        if not our_duration:
            continue
        
        # Find CV clip with same duration (within 10ms tolerance)
        best_match = None
        best_diff = float('inf')
        
        for cv_filename, cv_duration in cv_durations.items():
            diff = abs(our_duration - cv_duration)
            if diff < 0.01 and diff < best_diff:  # Within 10ms
                best_diff = diff
                best_match = cv_filename
        
        if best_match and best_match in cv_data:
            reference = cv_data[best_match]
            
            # Save reference
            ref_file = Path(output_dir) / f"{our_file.stem}.txt"
            ref_file.parent.mkdir(parents=True, exist_ok=True)
            with open(ref_file, 'w', encoding='utf-8') as f:
                f.write(reference)
            
            matches.append({
                'our_file': our_file.name,
                'cv_file': best_match,
                'duration': our_duration,
                'diff_ms': best_diff * 1000,
                'reference': reference
            })
            matched_count += 1
            
            if matched_count % 100 == 0:
                print(f"  Matched {matched_count} files...")
        else:
            print(f"⚠️  No match for {our_file.name} (duration: {our_duration:.3f}s)")
    
    print(f"\n✓ Matched {matched_count}/{len(our_files)} files")
    
    # Save matching report
    report_file = Path(f"data/duration_match_report_{lang}.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved report: {report_file}")
    
    return matched_count

def main():
    parser = argparse.ArgumentParser(description='Match audio by duration')
    parser.add_argument('--lang', required=True, choices=['mn', 'hu', 'es', 'fr'])
    parser.add_argument('--tsv-file', required=True)
    parser.add_argument('--audio-dir', required=True, help='Our audio directory (e.g., data/wav/es)')
    parser.add_argument('--cv-clips-dir', required=True, help='CV clips directory (e.g., cv-corpus-*/es/clips)')
    parser.add_argument('--output-dir', required=True, help='Output directory for references')
    
    args = parser.parse_args()
    
    matched = match_by_duration(
        args.lang,
        args.tsv_file,
        args.audio_dir,
        args.cv_clips_dir,
        args.output_dir
    )
    
    print("\n" + "="*60)
    if matched > 950:
        print("✅ EXCELLENT - Almost perfect matching!")
    elif matched > 900:
        print("✅ GOOD - Sufficient for analysis")
    elif matched > 800:
        print("⚠️  PARTIAL - Some files unmatched")
    else:
        print("❌ POOR - Matching failed")
    print("="*60)

if __name__ == '__main__':
    main()
