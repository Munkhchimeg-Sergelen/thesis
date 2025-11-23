#!/usr/bin/env python
import argparse, os, json, time, pathlib, re
from faster_whisper import WhisperModel

LANG_RE = re.compile(r"/(mn|hu|fr|es)/", re.IGNORECASE)
def guess_lang_from_path(path):
    m = LANG_RE.search("/" + path.replace("\\","/") + "/")
    return (m.group(1).lower() if m else None)

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="tiny")
ap.add_argument("--mode", choices=["hinted","lid2asr"], required=True)
ap.add_argument("--infile", required=True)
ap.add_argument("--hint-lang", help="Required if mode=hinted")
ap.add_argument("--device", default="cpu", help='"cpu", "cuda", or "auto"')
ap.add_argument("--outdir", default="results/transcripts")
args = ap.parse_args()

if args.device == "cpu":
    os.environ["CT2_FORCE_CPU"] = "1"

pathlib.Path(args.outdir).mkdir(parents=True, exist_ok=True)
model = WhisperModel(args.model, device=args.device)

language = None
lid_meta = {}
t0 = time.time()

if args.mode == "hinted":
    assert args.hint_lang, "--hint-lang is required for hinted mode"
    language = args.hint_lang
else:
    tried = []
    # LID attempt 1: VAD on
    try:
        tried.append("vad_filter=True")
        segments, info = model.transcribe(args.infile, task="transcribe", without_timestamps=True, vad_filter=True)
        language = getattr(info, "language", None)
        lid_meta = {"lid_language": language, "lid_prob": getattr(info, "language_probability", None), "tried": tried}
    except Exception:
        language = None
    # LID attempt 2: VAD off
    if not language:
        try:
            tried.append("vad_filter=False")
            segments, info = model.transcribe(args.infile, task="transcribe", without_timestamps=True, vad_filter=False)
            language = getattr(info, "language", None)
            lid_meta = {"lid_language": language, "lid_prob": getattr(info, "language_probability", None), "tried": tried}
        except Exception:
            language = None
    # Fallbacks: low-confidence or unknown
    # threshold for low confidence
    lid_prob = (lid_meta.get("lid_prob") if isinstance(lid_meta, dict) else None)
    folder_lang = guess_lang_from_path(args.infile)
    if (lid_prob is not None and lid_prob < 0.60 and folder_lang):
        language = folder_lang
        lid_meta = {**lid_meta, "fallback": "folder_on_low_conf"}
    if not language:
        language = guess_lang_from_path(args.infile)
        lid_meta = {"lid_language": language, "lid_prob": None, "tried": tried + ["fallback:folder"]}

# Final ASR pass
segments, info = model.transcribe(args.infile, task="transcribe", language=language, vad_filter=True)
text = "".join(s.text for s in segments)

# Get audio duration
duration_sec = getattr(info, "duration", None)

stem = os.path.splitext(os.path.basename(args.infile))[0]
sysname = f"whisper-{args.model}"
# Include model size in path to prevent overwriting
outbase = os.path.join(args.outdir, f"{args.mode}/whisper-{args.model}/{(language or 'unk')}")
os.makedirs(outbase, exist_ok=True)

with open(os.path.join(outbase, f"{stem}.txt"), "w", encoding="utf-8") as f:
    f.write(text.strip()+"\n")

elapsed = round(time.time()-t0, 3)
sidecar = {
  "file": args.infile, "system": sysname, "mode": args.mode,
  "language_used": language, "avg_logprob": getattr(info, "avg_logprob", None),
  "elapsed_sec": elapsed,
  "duration_sec": duration_sec,
  "rtf": round(elapsed / duration_sec, 4) if duration_sec else None,
  "device": args.device
}
sidecar.update(lid_meta)
with open(os.path.join(outbase, f"{stem}.json"), "w", encoding="utf-8") as f:
    json.dump(sidecar, f, ensure_ascii=False, indent=2)

print(f"Wrote: {outbase}/{stem}.txt")
