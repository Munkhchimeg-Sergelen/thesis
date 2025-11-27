#!/usr/bin/env python3
"""
Optimized OmniLingual batch processing
Loads model ONCE per language, processes all files
"""

import argparse
import time
import json
from pathlib import Path
from omnilingual_asr.models.inference.pipeline import ASRInferencePipeline
import librosa

# Language code mapping
LANG_MAP = {
    'mn': 'khk_Cyrl',
    'hu': 'hun_Latn',
    'es': 'spa_Latn',
    'fr': 'fra_Latn',
}

def process_model_language(model_card, lang, audio_dir, output_dir):
    """Process all files for one model and language"""
    
    lang_code = LANG_MAP[lang]
    audio_files = sorted(Path(audio_dir).glob(f"{lang}/*.mp3"))
    
    if not audio_files:
        print(f"❌ No audio files found for {lang}")
        return
    
    print(f"\n--- Processing {lang.upper()} with {model_card} ---")
    print(f"Files to process: {len(audio_files)}")
    
    # Load model ONCE
    print(f"Loading {model_card}...")
    pipeline = ASRInferencePipeline(model_card=model_card)
    print("✓ Model loaded\n")
    
    # Prepare output directory
    outdir = Path(output_dir) / model_card / lang
    outdir.mkdir(parents=True, exist_ok=True)
    
    # Process all files
    total_time = 0
    for i, audio_file in enumerate(audio_files, 1):
        # Load audio
        audio, sr = librosa.load(str(audio_file), sr=16000, mono=True)
        duration_sec = len(audio) / 16000
        
        # Check duration
        if duration_sec > 40:
            print(f"⚠️  Skipping {audio_file.name} (duration {duration_sec:.1f}s > 40s limit)")
            continue
        
        # Prepare audio dict
        audio_data = {
            "waveform": audio,
            "sample_rate": sr
        }
        
        # Transcribe with timing
        t0 = time.time()
        transcriptions = pipeline.transcribe(
            [audio_data],
            lang=[lang_code],
            batch_size=1
        )
        processing_time = time.time() - t0
        total_time += processing_time
        
        transcription = transcriptions[0] if transcriptions else ""
        rtf = processing_time / duration_sec if duration_sec > 0 else 0
        
        # Save results
        base_name = audio_file.stem
        txt_file = outdir / f"{base_name}.txt"
        json_file = outdir / f"{base_name}.json"
        
        # Save transcript
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(transcription)
        
        # Save JSON
        result_json = {
            'file': str(audio_file),
            'transcript': transcription,
            'language_used': lang_code,
            'duration_sec': duration_sec,
            'processing_time_sec': processing_time,
            'rtf': rtf,
            'model': model_card,
            'system': 'omnilingual',
            'mode': 'hinted'
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result_json, f, indent=2, ensure_ascii=False)
        
        # Progress updates
        if i % 100 == 0:
            avg = total_time / i
            print(f"  Processed {i}/{len(audio_files)} files (avg: {avg:.3f}s per file)")
    
    avg_time = total_time / len(audio_files)
    print(f"✅ {lang.upper()} completed: {len(audio_files)} files")
    print(f"   Total time: {total_time:.2f}s, Average: {avg_time:.3f}s per file\n")


def main():
    parser = argparse.ArgumentParser(description='Optimized OmniLingual Batch Processing')
    parser.add_argument('--models', nargs='+', 
                      default=['omniASR_CTC_300M', 'omniASR_CTC_1B', 'omniASR_LLM_1B'],
                      help='Models to process')
    parser.add_argument('--languages', nargs='+', default=['mn', 'hu', 'es', 'fr'],
                      help='Languages to process')
    parser.add_argument('--audio-dir', default='data/wav',
                      help='Directory containing audio files')
    parser.add_argument('--output-dir', default='results/transcripts/hinted/omnilingual',
                      help='Output directory')
    
    args = parser.parse_args()
    
    start_time = time.time()
    
    print("="*60)
    print("OPTIMIZED OMNILINGUAL ASR BATCH PROCESSING")
    print("="*60)
    print(f"Models: {', '.join(args.models)}")
    print(f"Languages: {', '.join(args.languages)}")
    print(f"Estimated time: ~12-18 hours")
    print("="*60)
    
    for model in args.models:
        print(f"\n{'='*60}")
        print(f"MODEL: {model}")
        print(f"{'='*60}")
        
        for lang in args.languages:
            process_model_language(
                model_card=model,
                lang=lang,
                audio_dir=args.audio_dir,
                output_dir=args.output_dir
            )
    
    total_time = time.time() - start_time
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    
    print("\n" + "="*60)
    print("✅ ALL MODELS & LANGUAGES COMPLETE!")
    print("="*60)
    print(f"Total time: {hours}h {minutes}m")
    
    # Print summary
    for model in args.models:
        print(f"\n{model}:")
        for lang in args.languages:
            result_dir = Path(args.output_dir) / model / lang
            count = len(list(result_dir.glob("*.json"))) if result_dir.exists() else 0
            print(f"  {lang}: {count} files")


if __name__ == '__main__':
    main()
