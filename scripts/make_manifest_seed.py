#!/usr/bin/env python
import sys, glob, os, csv
langs = sys.argv[1:] or ["hu","fr","es","mn"]
os.makedirs("results/manifests", exist_ok=True)
for L in langs:
    rows=[]
    for p in sorted(glob.glob(f"data/wav/{L}/*.wav")):
        rows.append({"file":p,"ref":""})
    out=f"results/manifests/{L}_refs_seed.csv"
    with open(out,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["file","ref"]); w.writeheader(); w.writerows(rows)
    print(f"Wrote {out} ({len(rows)} rows)")
