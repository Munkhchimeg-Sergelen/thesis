#!/usr/bin/env python3
import argparse, os, json, time
from faster_whisper import WhisperModel

LANGS = {"mn","hu","fr","es"}

def lang_hint_from_path(p):
    parts = p.replace("\\","/").split("/")
    for pr in parts:
        if pr in LANGS: return pr
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["hinted"], default="hinted")
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="tiny")
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    compute_type = "int8" if args.device=="cpu" else "float16"
    model = WhisperModel(args.model, device=args.device, compute_type=compute_type)

    for root,_,files in os.walk(args.inp):
        for fn in files:
            if not fn.lower().endswith((".wav",".flac",".mp3",".m4a",".ogg")): continue
            p = os.path.join(root, fn)
            lang = lang_hint_from_path(p)
            if not lang: continue

            t0 = time.time()
            segments, info = model.transcribe(p, language=lang, task="transcribe")
            text = "".join(s.text for s in segments).strip()
            dt = time.time()-t0

            base = os.path.splitext(os.path.basename(p))[0]
            out_txt_dir = os.path.join(args.out, lang, "txt")
            out_js_dir  = os.path.join(args.out, lang, "json")
            os.makedirs(out_txt_dir, exist_ok=True); os.makedirs(out_js_dir, exist_ok=True)
            with open(os.path.join(out_txt_dir, base + ".txt"), "w", encoding="utf-8") as f:
                f.write(text)
            side = {
                "file": p, "language_used": lang,
                "segments": [{"start": s.start, "end": s.end, "text": s.text} for s in model.transcribe(p, language=lang, task="transcribe")[0]],
                "model": args.model, "device": args.device, "latency_sec": dt
            }
            with open(os.path.join(out_js_dir, base + ".json"), "w", encoding="utf-8") as f:
                json.dump(side, f, ensure_ascii=False, indent=2)
    print("ASR outputs →", args.out)
if __name__ == "__main__":
    main()
