#!/usr/bin/env python3
import argparse, os, csv, soundfile as sf
def bucket(d):
    if d < 20: return 10
    if d < 60: return 30
    return 120
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for lang in sorted(os.listdir(args.inp)):
        lang_dir = os.path.join(args.inp, lang)
        if not os.path.isdir(lang_dir): continue
        out_csv = os.path.join(args.out, f"{lang}.csv")
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["file_path","lang","duration_sec","bucket"])
            for root,_,files in os.walk(lang_dir):
                for fn in files:
                    if not fn.lower().endswith((".wav",".flac",".mp3",".m4a",".ogg")): continue
                    p = os.path.join(root, fn)
                    try:
                        info = sf.info(p); dur = float(info.frames)/float(info.samplerate)
                    except Exception: dur = float("nan")
                    w.writerow([p, lang, f"{dur:.2f}", bucket(dur) if dur==dur else ""])
    print("manifests written to", args.out)
if __name__ == "__main__":
    main()
