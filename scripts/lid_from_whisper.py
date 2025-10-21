#!/usr/bin/env python3
import argparse, json, os, time
import whisper
from whisper.audio import load_audio, pad_or_trim, log_mel_spectrogram

def detect_lang(model, wav_path, head_sec):
    audio = load_audio(wav_path)
    sr = 16000
    n = min(len(audio), int(head_sec*sr))
    head = pad_or_trim(audio[:n])
    mel = log_mel_spectrogram(head).to(model.device)
    _, probs = model.detect_language(mel)
    lang, prob = max(probs.items(), key=lambda kv: kv[1])
    return lang, float(prob), {k: float(v) for k,v in probs.items()}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="small")
    ap.add_argument("--head-sec", type=float, default=8.0)
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    model = whisper.load_model(args.model, device=args.device)

    for root,_,files in os.walk(args.inp):
        for fn in files:
            if not fn.lower().endswith((".wav",".flac",".mp3",".m4a",".ogg")): continue
            p = os.path.join(root, fn)
            t0 = time.time()
            lang, conf, dist = detect_lang(model, p, args.head_sec)
            dt = time.time() - t0
            outj = {
                "file": p, "head_sec": args.head_sec, "pred_lang": lang,
                "confidence": conf, "probs": dist, "model": args.model,
                "device": args.device, "latency_sec": dt
            }
            base = os.path.splitext(os.path.basename(p))[0]
            with open(os.path.join(args.out, base + ".json"), "w", encoding="utf-8") as f:
                json.dump(outj, f, ensure_ascii=False, indent=2)
    print("LID logs →", args.out)

if __name__ == "__main__":
    main()
