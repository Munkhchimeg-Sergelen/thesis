#!/usr/bin/env python
import json, argparse, time, os, tempfile, subprocess, shlex, re
from faster_whisper import WhisperModel

LANG_RE = re.compile(r"/(mn|hu|fr|es)/", re.IGNORECASE)

def trim_head(infile, head_sec):
    if head_sec is None or head_sec <= 0:
        return infile, None
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav"); tmp.close()
    cmd = f"ffmpeg -y -hide_banner -loglevel error -t {head_sec} -i {shlex.quote(infile)} -ac 1 -ar 16000 {shlex.quote(tmp.name)}"
    subprocess.check_call(cmd, shell=True)
    return tmp.name, tmp.name

def guess_lang_from_path(path):
    m = LANG_RE.search("/" + path.replace("\\","/") + "/")
    return (m.group(1).lower() if m else None)

parser = argparse.ArgumentParser()
parser.add_argument("--model", default="tiny")
parser.add_argument("--head-sec", type=float, default=10.0, help="Use only first N seconds (ffmpeg trim).")
parser.add_argument("--infile", required=True)
parser.add_argument("--device", default="cpu", help='"cpu", "cuda", or "auto"')
args = parser.parse_args()

if args.device == "cpu":
    os.environ["CT2_FORCE_CPU"] = "1"

t0 = time.time()
model = WhisperModel(args.model, device=args.device)

use_path, tmp_to_rm = trim_head(args.infile, args.head_sec)
language = None; lang_prob = None; tried = []

try:
    # 1) attempt with VAD
    tried.append("vad_filter=True")
    segments, info = model.transcribe(use_path, task="transcribe", language=None, without_timestamps=True, vad_filter=True)
    language = getattr(info, "language", None)
    lang_prob = getattr(info, "language_probability", None)
except Exception:
    language = None

if not language:
    try:
        # 2) retry without VAD
        tried.append("vad_filter=False")
        segments, info = model.transcribe(use_path, task="transcribe", language=None, without_timestamps=True, vad_filter=False)
        language = getattr(info, "language", None)
        lang_prob = getattr(info, "language_probability", None)
    except Exception:
        language = None

# 3) fallback to folder hint if still unknown
if not language:
    language = guess_lang_from_path(args.infile)
    lang_prob = None

out = {
    "file": args.infile,
    "language": language,
    "language_prob": lang_prob,
    "model": args.model,
    "head_sec": args.head_sec,
    "device": args.device,
    "tried": tried,
    "elapsed_sec": round(time.time() - t0, 3),
}
print(json.dumps(out, ensure_ascii=False))

if tmp_to_rm and os.path.exists(tmp_to_rm):
    try: os.remove(tmp_to_rm)
    except OSError: pass
