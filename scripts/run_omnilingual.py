#!/usr/bin/env python3
"""
OmniLingual ASR Evaluation
Successor to Wav2Vec2, supports 1600+ languages
"""

import argparse
import time
import json
import torch
from pathlib import Path
from omnilingual_asr.models.inference.pipeline import ASRInferencePipeline

# Language code mapping for OmniLingual (uses ISO 639-3 + script)
LANG_MAP = {
    'mn': 'khk_Cyrl',  # Mongolian (Khalkha, Cyrillic script)
    'hu': 'hun_Latn',  # Hungarian (Latin script)
    'es': 'spa_Latn',  # Spanish (Latin script)
    'fr': 'fra_Latn',  # French (Latin script)
}

class OmniLingualASR:
    def __init__(self, model_card: str, language: str):
        """
        Initialize OmniLingual ASR
        
        Args:
            model_card: Model to use (e.g., 'omniASR_W2V_300M', 'omniASR_W2V_1B', 'omniASR_LLM_1B')
            language: Target language code (mn, hu, es, fr)
        """
        if language not in LANG_MAP:
            raise ValueError(f"Language '{language}' not supported. Available: {list(LANG_MAP.keys())}")
        
        self.language = language
        self.lang_code = LANG_MAP[language]
        self.model_card = model_card
        
        print(f"[OmniLingual] Loading {model_card} for {language} ({self.lang_code})...")
        self.pipeline = ASRInferencePipeline(model_card=model_card)
        print("✓ Model loaded")
        
    def transcribe(self, audio_path: str):
        """Transcribe audio file"""
        import librosa
        
        # Load audio
        audio, sr = librosa.load(audio_path, sr=16000, mono=True)
        
        # Get duration
        duration_sec = len(audio) / 16000
        
        # Check duration (OmniLingual has 40s limit)
        if duration_sec > 40:
            raise ValueError(f"Audio duration ({duration_sec:.1f}s) exceeds 40s limit")
        
        # Prepare audio dict for pipeline
        audio_data = {
            "waveform": audio,
            "sample_rate": sr
        }
        
        # Transcribe with timing
        t0 = time.time()
        transcriptions = self.pipeline.transcribe(
            [audio_data],
            lang=[self.lang_code],
            batch_size=1
        )
        processing_time = time.time() - t0
        
        # Get transcript
        transcription = transcriptions[0] if transcriptions else ""
        
        # Calculate RTF
        rtf = processing_time / duration_sec if duration_sec > 0 else 0
        
        return {
            'text': transcription,
            'language': self.lang_code,
            'duration_sec': duration_sec,
            'processing_time_sec': processing_time,
            'rtf': rtf,
            'model': self.model_card,
        }


def main():
    parser = argparse.ArgumentParser(description='OmniLingual ASR Evaluation')
    parser.add_argument('--infile', required=True, help='Input audio file')
    parser.add_argument('--hint-lang', required=True, choices=['mn', 'hu', 'es', 'fr'],
                      help='Target language')
    parser.add_argument('--model', default='omniASR_CTC_300M',
                      choices=['omniASR_CTC_300M', 'omniASR_CTC_1B', 'omniASR_CTC_3B',
                               'omniASR_LLM_300M', 'omniASR_LLM_1B', 'omniASR_LLM_3B'],
                      help='OmniLingual model to use')
    parser.add_argument('--save-json', action='store_true',
                      help='Save results as JSON')
    parser.add_argument('--outdir', default='results/transcripts/hinted/omnilingual',
                      help='Output directory')
    
    args = parser.parse_args()
    
    # Initialize model
    asr = OmniLingualASR(args.model, args.hint_lang)
    
    # Process audio
    input_path = Path(args.infile)
    result = asr.transcribe(str(input_path))
    
    # Prepare output paths
    outdir = Path(args.outdir) / args.model / args.hint_lang
    outdir.mkdir(parents=True, exist_ok=True)
    
    base_name = input_path.stem
    txt_file = outdir / f"{base_name}.txt"
    json_file = outdir / f"{base_name}.json"
    
    # Save transcript
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(result['text'])
    
    print(f"Wrote: {txt_file}")
    
    # Save JSON if requested
    if args.save_json:
        result_json = {
            'file': str(input_path),
            'transcript': result['text'],
            'language_used': result['language'],
            'duration_sec': result['duration_sec'],
            'processing_time_sec': result['processing_time_sec'],
            'rtf': result['rtf'],
            'model': result['model'],
            'system': 'omnilingual',
            'mode': 'hinted'
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result_json, f, indent=2, ensure_ascii=False)
        
        print(f"Wrote: {json_file}")


if __name__ == '__main__':
    main()
