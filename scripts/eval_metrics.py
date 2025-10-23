#!/usr/bin/env python
import argparse, csv, os
from jiwer import wer, cer

ap = argparse.ArgumentParser()
ap.add_argument("--refs", required=True, help="CSV with columns: file,ref")
ap.add_argument("--hyps_dir", required=True, help="Folder with .txt transcripts")
ap.add_argument("--out_csv", default="results/metrics/wer_cer_run.csv")
args = ap.parse_args()

rows = []
with open(args.refs, encoding="utf-8") as f:
    for line in f:
        if not line.strip(): continue
        file, ref = line.rstrip("\n").split(",", 1)
        stem = os.path.splitext(os.path.basename(file))[0]
        hyp_path = None
        for root,_,_files in os.walk(args.hyps_dir):
            cand = os.path.join(root, f"{stem}.txt")
            if os.path.exists(cand):
                hyp_path = cand; break
        if not hyp_path: continue
        hyp = open(hyp_path, encoding="utf-8").read().strip()
        rows.append({"file": file, "wer": wer(ref, hyp), "cer": cer(ref, hyp)})

os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)
with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["file","wer","cer"])
    w.writeheader(); w.writerows(rows)
print(f"Wrote {args.out_csv} ({len(rows)} rows)")
