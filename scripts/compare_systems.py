#!/usr/bin/env python3
"""
Compare Whisper vs Wav2Vec2 ASR systems
Runs both on same audio, outputs comparison table
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
import pandas as pd


def run_whisper(audio_path, mode, language=None, model="tiny", device="cpu"):
    """Run Whisper ASR"""
    cmd = [
        "python", "scripts/run_whisper.py",
        "--mode", mode,
        "--model", model,
        "--device", device,
        "--infile", audio_path,
        "--outdir", "results/transcripts"
    ]
    
    if mode == "hinted" and language:
        cmd.extend(["--hint-lang", language])
    
    print(f"[Whisper] Running: {' '.join(cmd)}", file=sys.stderr)
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start
    
    if result.returncode != 0:
        print(f"[Whisper] ERROR: {result.stderr}", file=sys.stderr)
        return None
    
    return {
        "system": "whisper",
        "text": result.stdout.strip(),
        "elapsed": elapsed,
        "stderr": result.stderr
    }


def run_wav2vec2(audio_path, mode, language=None, device="cpu"):
    """Run Wav2Vec2 ASR"""
    cmd = [
        "python", "scripts/asr_wav2vec2.py",
        "--mode", mode,
        "--device", device,
        "--infile", audio_path,
        "--outdir", "results/transcripts",
        "--save-json"
    ]
    
    if mode == "hinted" and language:
        cmd.extend(["--hint-lang", language])
    
    print(f"[Wav2Vec2] Running: {' '.join(cmd)}", file=sys.stderr)
    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start
    
    if result.returncode != 0:
        print(f"[Wav2Vec2] ERROR: {result.stderr}", file=sys.stderr)
        return None
    
    return {
        "system": "wav2vec2",
        "text": result.stdout.strip(),
        "elapsed": elapsed,
        "stderr": result.stderr
    }


def compare_single(audio_path, mode, language=None, whisper_model="tiny", device="cpu"):
    """Compare both systems on single audio file"""
    print(f"\n{'='*60}")
    print(f"Audio: {audio_path}")
    print(f"Mode: {mode}, Language: {language or 'auto'}")
    print(f"{'='*60}\n")
    
    # Run both systems
    whisper_result = run_whisper(audio_path, mode, language, whisper_model, device)
    wav2vec2_result = run_wav2vec2(audio_path, mode, language, device)
    
    # Print comparison
    if whisper_result:
        print(f"\n[WHISPER] ({whisper_result['elapsed']:.2f}s)")
        print(f"  {whisper_result['text']}")
    
    if wav2vec2_result:
        print(f"\n[WAV2VEC2] ({wav2vec2_result['elapsed']:.2f}s)")
        print(f"  {wav2vec2_result['text']}")
    
    print(f"\n{'='*60}\n")
    
    return {
        "audio": str(audio_path),
        "mode": mode,
        "language": language,
        "whisper_text": whisper_result["text"] if whisper_result else None,
        "whisper_time": whisper_result["elapsed"] if whisper_result else None,
        "wav2vec2_text": wav2vec2_result["text"] if wav2vec2_result else None,
        "wav2vec2_time": wav2vec2_result["elapsed"] if wav2vec2_result else None,
    }


def compare_batch(audio_dir, mode, languages=None, whisper_model="tiny", device="cpu"):
    """Compare systems on multiple audio files"""
    audio_dir = Path(audio_dir)
    results = []
    
    # Find all wav files
    wav_files = list(audio_dir.rglob("*.wav"))
    
    if not wav_files:
        print(f"[ERROR] No .wav files found in {audio_dir}", file=sys.stderr)
        return []
    
    print(f"[INFO] Found {len(wav_files)} audio files", file=sys.stderr)
    
    for wav_file in sorted(wav_files):
        # Infer language from path
        lang = None
        if languages:
            for l in languages:
                if l in str(wav_file).lower():
                    lang = l
                    break
        
        # Compare
        result = compare_single(
            wav_file, 
            mode=mode,
            language=lang,
            whisper_model=whisper_model,
            device=device
        )
        results.append(result)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Compare Whisper vs Wav2Vec2")
    parser.add_argument("--audio", help="Single audio file or directory")
    parser.add_argument("--mode", default="hinted", choices=["hinted", "lid2asr"])
    parser.add_argument("--lang", help="Language code (for hinted mode)")
    parser.add_argument("--langs", nargs="+", help="Language codes (for batch mode)")
    parser.add_argument("--whisper-model", default="tiny", help="Whisper model size")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    parser.add_argument("--out-csv", help="Output CSV path for batch results")
    args = parser.parse_args()
    
    if not args.audio:
        print("[ERROR] --audio required", file=sys.stderr)
        sys.exit(1)
    
    audio_path = Path(args.audio)
    
    # Single file or batch?
    if audio_path.is_file():
        compare_single(
            audio_path,
            mode=args.mode,
            language=args.lang,
            whisper_model=args.whisper_model,
            device=args.device
        )
    elif audio_path.is_dir():
        results = compare_batch(
            audio_path,
            mode=args.mode,
            languages=args.langs or ["mn", "hu", "fr", "es"],
            whisper_model=args.whisper_model,
            device=args.device
        )
        
        # Save to CSV if requested
        if args.out_csv and results:
            df = pd.DataFrame(results)
            df.to_csv(args.out_csv, index=False)
            print(f"\n[INFO] Results saved to: {args.out_csv}", file=sys.stderr)
            
            # Print summary
            print(f"\n{'='*60}")
            print("SUMMARY")
            print(f"{'='*60}")
            print(f"Total files: {len(results)}")
            print(f"Whisper avg time: {df['whisper_time'].mean():.2f}s")
            print(f"Wav2Vec2 avg time: {df['wav2vec2_time'].mean():.2f}s")
    else:
        print(f"[ERROR] {audio_path} not found", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
