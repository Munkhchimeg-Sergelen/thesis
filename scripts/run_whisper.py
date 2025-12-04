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
ap.add_argument("--device", default="cuda", help='"cpu", "cuda", or "auto"')
ap.add_argument("--outdir", default="results/transcripts")
args = ap.parse_args()

pathlib.Path(args.outdir).mkdir(parents=True, exist_ok=True)
model = WhisperModel(
    args.model,
    device="cuda",
    compute_type="float16",
    download_root="models"
)

language = None
lid_meta = {}
t0 = time.time()

if args.mode == "hinted":
    if not args.hint_lang:
        language = guess_lang_from_path(args.infile)
        if not language:
            raise ValueError("No language hint provided and couldn't guess from path")
    else:
        language = args.hint_lang.lower()
else:  # lid2asr mode
    segments, info = model.transcribe(
        args.infile,
        task="lang_id",
        beam_size=1
    )
    language = info.language
    lid_meta = {
        "detected_language": language,
        "language_probability": info.language_probability
    }

segments, info = model.transcribe(
    args.infile,
    language=language,
    beam_size=1
)

text = "".join(s.text for s in segments)
duration = time.time() - t0

outfile = os.path.splitext(os.path.basename(args.infile))[0]
outdir = os.path.join(args.outdir, args.mode, args.model, language)
pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

with open(os.path.join(outdir, outfile + ".txt"), "w", encoding="utf-8") as f:
    f.write(text.strip())

meta = {
    "model": args.model,
    "mode": args.mode,
    "language": language,
    "duration_sec": duration,
    **lid_meta
}

with open(os.path.join(outdir, outfile + ".json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)