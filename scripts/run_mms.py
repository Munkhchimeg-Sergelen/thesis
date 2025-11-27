#!/usr/bin/env python3
"""
MMS (Massively Multilingual Speech) ASR Evaluation
Supports 1100+ languages including MN, HU, ES, FR
"""

import argparse
import time
import json
import torch
import librosa
from pathlib import Path
from transformers import Wav2Vec2ForCTC, AutoProcessor

# MMS model supports 1100+ languages
MODEL_ID = 'facebook/mms-1b-all'

# Language code mapping (MMS uses ISO 639-3)
LANG_MAP = {
    'mn': 'mon',  # Mongolian
    'hu': 'hun',  # Hungarian
    'es': 'spa',  # Spanish
    'fr': 'fra',  # French
}

class MMS_ASR:
    def __init__(self, language: str, device: str = 'cuda'):
        """Initialize MMS for a specific language"""
        if language not in LANG_MAP:
            raise ValueError(f"Language '{language}' not supported. Available: {list(LANG_MAP.keys())}")
        
        self.language = language
        self.lang_code = LANG_MAP[language]
        self.device = device
        self.model_id = MODEL_ID
        
        print(f"[MMS] Loading {self.model_id} for {language} ({self.lang_code}) on {device}...")
        self.processor = AutoProcessor.from_pretrained(self.model_id)
        self.model = Wav2Vec2ForCTC.from_pretrained(self.model_id).to(device)
        self.model.eval()
        
        # Set target language
        self.processor.tokenizer.set_target_lang(self.lang_code)
        self.model.load_adapter(self.lang_code)
        
    def transcribe(self, audio_path: str):
        """Transcribe audio file"""
        # Load audio with librosa (more compatible)
        audio, sr = librosa.load(audio_path, sr=16000, mono=True)
        
        # Get audio duration
        duration_sec = len(audio) / 16000
        
        # Process audio
        t0 = time.time()
        inputs = self.processor(audio, sampling_rate=16000, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Inference
        with torch.no_grad():
            outputs = self.model(**inputs).logits
        
        # Decode
        predicted_ids = torch.argmax(outputs, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]
        
        processing_time = time.time() - t0
        rtf = processing_time / duration_sec if duration_sec > 0 else 0
        
        return {
            'text': transcription,
            'language': self.lang_code,
            'duration_sec': duration_sec,
            'processing_time_sec': processing_time,
            'rtf': rtf,
            'model': self.model_id.split('/')[-1],
            'device': self.device
        }


def main():
    parser = argparse.ArgumentParser(description='MMS ASR Evaluation')
    parser.add_argument('--infile', required=True, help='Input audio file')
    parser.add_argument('--hint-lang', required=True, choices=['mn', 'hu', 'es', 'fr'],
                      help='Target language')
    parser.add_argument('--device', default='cuda', choices=['cuda', 'cpu'],
                      help='Device to use for inference')
    parser.add_argument('--save-json', action='store_true',
                      help='Save results as JSON')
    parser.add_argument('--outdir', default='results/transcripts/hinted/mms',
                      help='Output directory')
    
    args = parser.parse_args()
    
    # Initialize model
    asr = MMS_ASR(args.hint_lang, args.device)
    
    # Process audio
    input_path = Path(args.infile)
    result = asr.transcribe(str(input_path))
    
    # Prepare output paths
    outdir = Path(args.outdir) / args.hint_lang
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
            'device': result['device'],
            'system': 'mms',
            'mode': 'hinted'
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result_json, f, indent=2, ensure_ascii=False)
        
        print(f"Wrote: {json_file}")


if __name__ == '__main__':
    main()
