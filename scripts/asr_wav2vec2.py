#!/usr/bin/env python3
"""
Wav2Vec2-XLS-R multilingual ASR wrapper
Supports: MN, HU, FR, ES via facebook/wav2vec2-xls-r-300m model
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import torch
import soundfile as sf
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor


# Language-specific fine-tuned models
LANG_MODELS = {
    "mn": "bayartsogt/wav2vec2-large-xlsr-mongolian",
    "hu": "jonatasgrosman/wav2vec2-large-xlsr-53-hungarian",
    "fr": "jonatasgrosman/wav2vec2-large-xlsr-53-french",
    "es": "jonatasgrosman/wav2vec2-large-xlsr-53-spanish",
}

# Language codes mapping
LANG_MAP = {
    "mn": "mongolian",  # Mongolian
    "hu": "hungarian",  # Hungarian  
    "fr": "french",     # French
    "es": "spanish",    # Spanish
}


class Wav2Vec2ASR:
    """Wav2Vec2-XLS-R ASR wrapper with language-specific models"""
    
    def __init__(self, language="hu", device="cpu"):
        self.device = device
        self.language = language
        
        # Get language-specific model
        if language not in LANG_MODELS:
            raise ValueError(f"Language '{language}' not supported. Available: {list(LANG_MODELS.keys())}")
        
        self.model_name = LANG_MODELS[language]
        
        print(f"[Wav2Vec2] Loading {self.model_name} ({language}) on {device}...", file=sys.stderr)
        self.processor = Wav2Vec2Processor.from_pretrained(self.model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(self.model_name).to(device)
        self.model.eval()
        print("[Wav2Vec2] Model loaded.", file=sys.stderr)
    
    def load_audio(self, audio_path, target_sr=16000):
        """Load and resample audio to 16kHz mono"""
        import librosa
        # Load audio with librosa (handles MP3 and resampling)
        waveform, _ = librosa.load(audio_path, sr=target_sr, mono=True)
        return waveform
    
    def transcribe(self, audio_path, language=None):
        """
        Transcribe audio file
        
        Args:
            audio_path: Path to audio file
            language: Language code (ignored for base model, kept for API compatibility)
        
        Returns:
            dict with 'text', 'language_used', 'duration_sec', 'elapsed_sec'
        """
        start_time = time.time()
        
        # Load audio
        audio = self.load_audio(audio_path)
        duration_sec = len(audio) / 16000.0
        
        # Process with model
        with torch.no_grad():
            inputs = self.processor(
                audio, 
                sampling_rate=16000, 
                return_tensors="pt",
                padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Forward pass
            logits = self.model(**inputs).logits
            
            # Decode
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)[0]
        
        elapsed_sec = time.time() - start_time
        
        return {
            "text": transcription.strip(),
            "language_used": language or "multi",  # Base model is multilingual
            "duration_sec": duration_sec,
            "elapsed_sec": elapsed_sec,
            "rtf": elapsed_sec / duration_sec if duration_sec > 0 else 0.0,
            "model": self.model_name,
        }


def main():
    parser = argparse.ArgumentParser(description="Wav2Vec2-XLS-R ASR with language-specific models")
    parser.add_argument("--mode", choices=["hinted", "lid2asr"], default="hinted",
                        help="Inference mode (hinted=language provided, lid2asr=auto-detect)")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"],
                        help="Device (cpu/cuda)")
    parser.add_argument("--infile", required=True, help="Input audio file")
    parser.add_argument("--hint-lang", help="Language hint (for hinted mode): mn/hu/fr/es")
    parser.add_argument("--outdir", default="results/transcripts",
                        help="Output directory for transcripts")
    parser.add_argument("--save-json", action="store_true",
                        help="Save detailed JSON output")
    args = parser.parse_args()
    
    # Determine language FIRST (needed to load correct model)
    language = None
    if args.mode == "hinted":
        if not args.hint_lang:
            print("[ERROR] --hint-lang required for hinted mode", file=sys.stderr)
            sys.exit(1)
        language = args.hint_lang.lower()
    elif args.mode == "lid2asr":
        # Wav2Vec2 needs language-specific models, so infer from filename
        filename = Path(args.infile).name.lower()
        for code in ["mn", "hu", "fr", "es"]:
            if code in filename:
                language = code
                break
        if not language:
            print("[ERROR] Could not infer language from filename for LID mode", file=sys.stderr)
            sys.exit(1)
        print(f"[Wav2Vec2] LID mode: inferred language '{language}' from filename", 
              file=sys.stderr)
    
    # Initialize language-specific model
    asr = Wav2Vec2ASR(language=language, device=args.device)
    
    # Transcribe
    print(f"[Wav2Vec2] Transcribing: {args.infile}", file=sys.stderr)
    result = asr.transcribe(args.infile, language=language)
    
    # Print main output
    print(result["text"])
    
    # Save detailed output if requested
    if args.save_json or args.outdir:
        os.makedirs(args.outdir, exist_ok=True)
        
        # Determine output filename
        audio_name = Path(args.infile).stem
        if args.mode == "hinted":
            mode_dir = f"{args.outdir}/hinted/wav2vec2"
        else:
            mode_dir = f"{args.outdir}/lid2asr/wav2vec2"
        
        lang = language or "multi"
        full_outdir = f"{mode_dir}/{lang}"
        os.makedirs(full_outdir, exist_ok=True)
        
        # Save text
        txt_path = f"{full_outdir}/{audio_name}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        # Save JSON
        json_path = f"{full_outdir}/{audio_name}.json"
        result["audio_file"] = args.infile
        result["mode"] = args.mode
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"[Wav2Vec2] Saved: {txt_path}", file=sys.stderr)
        print(f"[Wav2Vec2] Saved: {json_path}", file=sys.stderr)
    
    # Print summary to stderr
    print(f"[Wav2Vec2] Duration: {result['duration_sec']:.2f}s, "
          f"Elapsed: {result['elapsed_sec']:.2f}s, "
          f"RTF: {result['rtf']:.3f}", file=sys.stderr)


if __name__ == "__main__":
    main()
