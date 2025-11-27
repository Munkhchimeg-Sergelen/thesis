#!/usr/bin/env python3
"""
Optimized beam search comparison - loads model ONCE
Processes all files with the same model instance
"""

import argparse
import time
from pathlib import Path
from faster_whisper import WhisperModel
import json

def process_language(lang_code, model_name, beam_sizes, device, audio_dir, output_dir):
    """Process all files for a language with both beam sizes"""
    
    audio_files = sorted(Path(audio_dir).glob(f"{lang_code}/*.mp3"))
    if not audio_files:
        print(f"❌ No audio files found for {lang_code}")
        return
    
    print(f"\n{'='*50}")
    print(f"Processing {lang_code.upper()} - {len(audio_files)} files")
    print(f"{'='*50}")
    
    # Load model ONCE
    print(f"Loading Whisper {model_name} model on {device}...")
    model = WhisperModel(model_name, device=device)
    print("✓ Model loaded\n")
    
    for beam_size in beam_sizes:
        mode_name = "greedy" if beam_size == 1 else f"beam{beam_size}"
        print(f"\n--- Testing beam_size={beam_size} ({mode_name}) ---")
        
        output_file = Path(output_dir) / f"{lang_code}_beam{beam_size}.txt"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        results = []
        total_time = 0
        
        for i, audio_file in enumerate(audio_files, 1):
            start = time.time()
            
            # Transcribe with specified beam size
            segments, info = model.transcribe(
                str(audio_file),
                language=lang_code,
                beam_size=beam_size,
                vad_filter=False
            )
            
            # Consume segments (needed for timing)
            _ = list(segments)
            
            elapsed = time.time() - start
            total_time += elapsed
            
            results.append({
                'file': audio_file.name,
                'time': elapsed
            })
            
            # Progress updates
            if i % 100 == 0:
                avg = total_time / i
                print(f"  Processed {i}/{len(audio_files)} files... (avg: {avg:.3f}s per file)")
        
        # Save results
        with open(output_file, 'w') as f:
            for r in results:
                f.write(f"{r['file']},{r['time']:.6f}\n")
            
            # Summary line
            avg_time = total_time / len(results)
            f.write(f"SUMMARY,{len(results)},{total_time:.6f},{avg_time:.6f}\n")
        
        print(f"✓ Completed {len(results)} files")
        print(f"  Total time: {total_time:.2f}s")
        print(f"  Average: {avg_time:.3f}s per file")
        print(f"  Saved: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Optimized Beam Search Comparison')
    parser.add_argument('--languages', nargs='+', default=['mn', 'hu', 'es', 'fr'],
                      help='Language codes to process')
    parser.add_argument('--model', default='small', help='Whisper model size')
    parser.add_argument('--beam-sizes', nargs='+', type=int, default=[1, 5],
                      help='Beam sizes to test')
    parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'],
                      help='Device for inference')
    parser.add_argument('--audio-dir', default='data/wav',
                      help='Directory containing audio files')
    parser.add_argument('--output-dir', default='results/beam_comparison',
                      help='Output directory for results')
    
    args = parser.parse_args()
    
    start_time = time.time()
    
    print("="*60)
    print("OPTIMIZED BEAM SEARCH COMPARISON")
    print("="*60)
    print(f"Languages: {', '.join(args.languages)}")
    print(f"Model: {args.model}")
    print(f"Beam sizes: {args.beam_sizes}")
    print(f"Device: {args.device}")
    print(f"Estimated time: ~2-3 hours (loads model once per language)")
    print("="*60)
    
    for lang in args.languages:
        process_language(
            lang_code=lang,
            model_name=args.model,
            beam_sizes=args.beam_sizes,
            device=args.device,
            audio_dir=args.audio_dir,
            output_dir=args.output_dir
        )
    
    total_time = time.time() - start_time
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    
    print("\n" + "="*60)
    print("✅ ALL LANGUAGES COMPLETE!")
    print("="*60)
    print(f"Total time: {hours}h {minutes}m")
    print(f"Results saved in: {args.output_dir}/")
    
    # Print summary
    for lang in args.languages:
        for beam in args.beam_sizes:
            result_file = Path(args.output_dir) / f"{lang}_beam{beam}.txt"
            if result_file.exists():
                with open(result_file) as f:
                    summary = [line for line in f if line.startswith('SUMMARY')]
                    if summary:
                        parts = summary[0].strip().split(',')
                        print(f"  {lang} beam={beam}: {parts[1]} files, avg={float(parts[3]):.3f}s")


if __name__ == '__main__':
    main()
