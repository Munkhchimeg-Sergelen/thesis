#!/usr/bin/env python3
import argparse, os, json, time, whisper

def transcribe(model, wav_path, language, task="transcribe"):
    import time, soundfile as sf
    # measure audio duration
    try:
        info = sf.info(wav_path); audio_sec = float(info.frames)/float(info.samplerate)
    except Exception:
        audio_sec = None
    t0 = time.time()
    result = model.transcribe(wav_path, language=language, task=task)
    dt = time.time() - t0
    result["_timing"] = {"latency_sec": result.get("_timing",{}).get("latency_sec", dt), "audio_sec": result.get("_timing",{}).get("audio_sec"), "rtf": result.get("_timing",{}).get("rtf"), "audio_sec": audio_sec, "rtf": (audio_sec/dt) if (audio_sec and dt>0) else None}
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["lid2asr","hinted"], required=True)
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="small")
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    model = whisper.load_model(args.model, device=args.device)

    # LID cache
    lid_dir = "results/logs/lid"
    lid_cache = {}
    if os.path.isdir(lid_dir):
        for fn in os.listdir(lid_dir):
            if fn.endswith(".json"):
                with open(os.path.join(lid_dir, fn), "r", encoding="utf-8") as f:
                    j = json.load(f); lid_cache[j["file"]] = j

    for root,_,files in os.walk(args.inp):
        parts = root.replace("\\","/").split("/")
        lang_hint = parts[-1] if parts and parts[-1] in {"mn","hu","fr","es"} else None

        for fn in files:
            if not fn.lower().endswith((".wav",".flac",".mp3",".m4a",".ogg")): continue
            p = os.path.join(root, fn)

            if args.mode == "hinted":
                language = lang_hint
                if language is None:
                    print(f"skip (no lang folder): {p}")
                    continue
            else:  # lid2asr
                if p in lid_cache:
                    language = lid_cache[p]["pred_lang"]
                else:
                    print(f"no LID for {p}; run make test_lid first"); continue

            t0 = time.time()
            result = transcribe(model, p, language=language)
            dt = time.time() - t0

            base = os.path.splitext(os.path.basename(p))[0]
            out_txt_dir = os.path.join(args.out, language or "unk", "txt")
            out_js_dir  = os.path.join(args.out, language or "unk", "json")
            os.makedirs(out_txt_dir, exist_ok=True)
            os.makedirs(out_js_dir,  exist_ok=True)

            with open(os.path.join(out_txt_dir, base + ".txt"), "w", encoding="utf-8") as f:
                f.write(result.get("text","").strip())

            side = {
                "file": p, "language_used": language, "segments": result.get("segments",[]),
                "avg_logprob": result.get("avg_logprob"), "compression_ratio": result.get("compression_ratio"),
                "no_speech_prob": result.get("no_speech_prob"), "model": args.model,
                "device": args.device, "latency_sec": result.get("_timing",{}).get("latency_sec", dt), "audio_sec": result.get("_timing",{}).get("audio_sec"), "rtf": result.get("_timing",{}).get("rtf")
            }
            with open(os.path.join(out_js_dir, base + ".json"), "w", encoding="utf-8") as f:
                json.dump(side, f, ensure_ascii=False, indent=2)

    print("ASR outputs →", args.out)

if __name__ == "__main__":
    main()
