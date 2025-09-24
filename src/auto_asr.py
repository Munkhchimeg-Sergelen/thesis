import os, sys, json, glob, shlex, subprocess
from pathlib import Path
from transformers import pipeline

ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "data" / "wav"
OUT_DIR = ROOT / "experiments" / "whisper_tiny"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FP = OUT_DIR / "preds.jsonl"

MODEL_ID = os.environ.get("ASR_MODEL", "openai/whisper-tiny")

def ensure_wav16k(file_path: Path) -> Path:
    file_path = file_path.resolve()
    out = file_path.with_suffix("").with_name(file_path.stem + "_16k.wav")
    cmd = f'ffmpeg -y -i {shlex.quote(str(file_path))} -ar 16000 -ac 1 {shlex.quote(str(out))}'
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out

def main():
    files = []
    for ext in ("*.m4a","*.mp3","*.wav"):
        files.extend(glob.glob(str(IN_DIR / ext)))
    files = sorted(set(files))
    if not files:
        print(f"No audio found in {IN_DIR}")
        sys.exit(0)

    print(f"Found {len(files)} file(s). Preparing WAVs…")
    wavs = [ensure_wav16k(Path(f)) for f in files]

    print(f"Loading ASR model: {MODEL_ID}")
    asr = pipeline("automatic-speech-recognition", model=MODEL_ID, device=-1)

    with open(OUT_FP, "w", encoding="utf-8") as w:
        for wp in wavs:
            try:
                text = asr(str(wp))["text"]
            except Exception as e:
                text = f"<<ERROR {e}>>"
            w.write(json.dumps({"audio": str(wp), "text": text}, ensure_ascii=False) + "\n")
            print(f"✓ {wp}")

    print(f"\nWrote predictions → {OUT_FP}")

if __name__ == "__main__":
    main()
