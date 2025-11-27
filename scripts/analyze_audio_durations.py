#!/usr/bin/env python3
"""
Analyze audio file durations and group results by length buckets
"""

import json
import librosa
from pathlib import Path
import pandas as pd
import argparse

def get_duration(audio_file):
    """Get audio duration in seconds"""
    try:
        duration = librosa.get_duration(path=str(audio_file))
        return duration
    except Exception as e:
        print(f"Error reading {audio_file}: {e}")
        return None

def analyze_durations(audio_dir, results_dir, output_file):
    """Analyze audio durations and correlate with performance"""
    
    print("="*60)
    print("AUDIO DURATION ANALYSIS")
    print("="*60)
    
    # Define duration buckets (in seconds)
    buckets = [
        (0, 5, "short"),      # 0-5s
        (5, 10, "medium"),    # 5-10s
        (10, 30, "long"),     # 10-30s
        (30, float('inf'), "very_long")  # 30s+
    ]
    
    data = []
    
    # Process all audio files
    audio_path = Path(audio_dir)
    for lang_dir in sorted(audio_path.iterdir()):
        if not lang_dir.is_dir():
            continue
        
        lang = lang_dir.name
        print(f"\nProcessing {lang.upper()}...")
        
        for audio_file in sorted(lang_dir.glob("*.mp3")):
            file_id = audio_file.stem
            
            # Get duration
            duration = get_duration(audio_file)
            if duration is None:
                continue
            
            # Determine bucket
            bucket_name = "unknown"
            for min_dur, max_dur, name in buckets:
                if min_dur <= duration < max_dur:
                    bucket_name = name
                    break
            
            # Try to get performance metrics from results
            results_path = Path(results_dir)
            models = ['whisper-small', 'omniASR_CTC_300M', 'omniASR_CTC_1B', 'omniASR_LLM_1B']
            
            for model in models:
                # Find JSON file
                if 'whisper' in model:
                    json_path = results_path / "transcripts" / "hinted" / model / lang / f"{file_id}.json"
                else:
                    # OmniLingual path might be nested
                    json_path = results_path / "transcripts" / "hinted" / "omnilingual" / model / lang / f"{file_id}.json"
                    # Check nested path
                    if not json_path.exists():
                        json_path = results_path / "transcripts" / "hinted" / "omnilingual" / model / lang / model / lang / f"{file_id}.json"
                
                if json_path.exists():
                    try:
                        with open(json_path) as f:
                            result = json.load(f)
                        
                        data.append({
                            'file_id': file_id,
                            'language': lang,
                            'model': model,
                            'duration_sec': duration,
                            'bucket': bucket_name,
                            'processing_time': result.get('processing_time_sec', result.get('elapsed_sec', None)),
                            'rtf': result.get('rtf', None)
                        })
                    except Exception as e:
                        print(f"  Warning: Could not read {json_path}: {e}")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    if df.empty:
        print("\n⚠️  No data found. Make sure results are available.")
        return
    
    print(f"\n✓ Collected {len(df)} data points")
    
    # Analysis by duration bucket
    print("\n" + "="*60)
    print("DURATION BUCKET ANALYSIS")
    print("="*60)
    
    bucket_stats = df.groupby(['bucket', 'model', 'language']).agg({
        'duration_sec': ['count', 'mean', 'std'],
        'rtf': ['mean', 'std']
    }).round(3)
    
    print(bucket_stats)
    
    # Save detailed results
    df.to_csv(output_file, index=False)
    print(f"\n✓ Saved detailed analysis: {output_file}")
    
    # Summary statistics
    summary_file = output_file.replace('.csv', '_summary.csv')
    bucket_stats.to_csv(summary_file)
    print(f"✓ Saved summary: {summary_file}")
    
    # Overall duration distribution
    print("\n" + "="*60)
    print("OVERALL DURATION DISTRIBUTION")
    print("="*60)
    
    duration_dist = df.groupby('language')['duration_sec'].describe()
    print(duration_dist)
    
    duration_dist.to_csv(output_file.replace('.csv', '_distribution.csv'))
    print(f"✓ Saved distribution: {output_file.replace('.csv', '_distribution.csv')}")

def main():
    parser = argparse.ArgumentParser(description='Analyze audio durations and performance')
    parser.add_argument('--audio-dir', default='data/wav',
                        help='Directory with audio files')
    parser.add_argument('--results-dir', default='results',
                        help='Directory with results')
    parser.add_argument('--output', default='results/duration_analysis.csv',
                        help='Output CSV file')
    
    args = parser.parse_args()
    
    analyze_durations(args.audio_dir, args.results_dir, args.output)
    
    print("\n" + "="*60)
    print("✅ DURATION ANALYSIS COMPLETE")
    print("="*60)

if __name__ == '__main__':
    main()
