#!/usr/bin/env python3
"""
Wav2Vec2-XLSR-53 Language-Specific ASR Evaluation Wrapper
Matches the interface of run_whisper.py for fair comparison
"""

import argparse
import time
import json
import torch
import torchaudio
from pathlib import Path
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Language-specific models
# MN & HU use base multilingual XLSR-53 (supports 53 languages)
LANG_MODELS = {
    'mn': 'facebook/wav2vec2-large-xlsr-53',  # Multilingual (includes Mongolian)
    'hu': 'facebook/wav2vec2-large-xlsr-53',  # Multilingual (includes Hungarian)
    'es': 'facebook/wav2vec2-large-xlsr-53-spanish',
    'fr': 'facebook/wav2vec2-large-xlsr-53-french',
}

class Wav2Vec2ASR:
    def __init__(self, language: str, device: str = 'cuda'):
        """Initialize Wav2Vec2 for a specific language"""
        if language not in LANG_MODELS:
            raise ValueError(f"Language '{language}' not supported. Available: {list(LANG_MODELS.keys())}")
        
        self.language = language
        self.device = device
        self.model_id = LANG_MODELS[language]
        
        print(f"[Wav2Vec2] Loading {self.model_id} on {device}...")
        self.processor = Wav2Vec2Processor.from_pretrained(self.model_id)
        self.model = Wav2Vec2ForCTC.from_pretrained(
            self.model_id,
            use_safetensors=True
        ).to(device)
        self.model.eval()  # Set to evaluation mode
        
    def transcribe(self, audio_path: str):
        """Transcribe audio file"""
        # Load audio
        audio, sr = torchaudio.load(audio_path)
        
        # Resample to 16kHz if needed
        if sr != 16000:
            audio = torchaudio.functional.resample(audio, sr, 16000)
        
        # Get audio duration
        duration_sec = audio.shape[1] / 16000
        
        # Process audio
        inputs = self.processor(
            audio.squeeze().cpu().numpy(),
            sampling_rate=16000,
            return_tensors='pt'
        )
        
        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Inference with timing
        start_time = time.perf_counter()
        
        with torch.no_grad():
            logits = self.model(**inputs).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)[0]
        
        end_time = time.perf_counter()
        processing_time = end_time - start_time
        
        # Compute RTF
        rtf = processing_time / duration_sec if duration_sec > 0 else 0
        
        return {
            'text': transcription,
            'language': self.language,
            'duration_sec': duration_sec,
            'processing_time_sec': processing_time,
            'rtf': rtf,
            'model': self.model_id.split('/')[-1],  # Short name
            'device': self.device
        }


def main():
    parser = argparse.ArgumentParser(description='Wav2Vec2-XLSR-53 ASR Evaluation')
    parser.add_argument('--infile', required=True, help='Input audio file (WAV)')
    parser.add_argument('--hint-lang', required=True, choices=['mn', 'hu', 'es', 'fr'],
                      help='Target language (MN, HU use multilingual model; ES, FR use specialized models)')
    parser.add_argument('--device', default='cuda', choices=['cuda', 'cpu'],
                      help='Device to use for inference')
    parser.add_argument('--save-json', action='store_true',
                      help='Save results as JSON')
    parser.add_argument('--outdir', default='results/transcripts/hinted/wav2vec2',
                      help='Output directory')
    
    args = parser.parse_args()
    
    # Initialize model
    asr = Wav2Vec2ASR(language=args.hint_lang, device=args.device)
    
    # Transcribe
    result = asr.transcribe(args.infile)
    
    # Prepare output
    input_path = Path(args.infile)
    lang = args.hint_lang
    outdir = Path(args.outdir) / lang
    outdir.mkdir(parents=True, exist_ok=True)
    
    # Output filename (same stem as input)
    out_stem = input_path.stem
    txt_file = outdir / f"{out_stem}.txt"
    json_file = outdir / f"{out_stem}.json"
    
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
            'device': result['device'],
            'system': 'wav2vec2',
            'mode': 'hinted'
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result_json, f, indent=2, ensure_ascii=False)
        
        print(f"Wrote: {json_file}")


if __name__ == '__main__':
    main()
