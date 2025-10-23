#!/usr/bin/env python
import pandas as pd, glob, os
os.makedirs("results/metrics", exist_ok=True)

wer_csvs = glob.glob("results/metrics/wer_cer_*.csv")
perf_jsons = glob.glob("results/metrics/perf_*.json")

dfs = [pd.read_csv(f) for f in wer_csvs]
wer_df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

perfs = []
for j in perf_jsons:
    import json
    data = json.load(open(j))
    perfs.append({"file": data.get("audio"), **{k:v for k,v in data.items() if k not in ["cmd","audio"]}})
perf_df = pd.DataFrame(perfs)

if not wer_df.empty and not perf_df.empty:
    merged = pd.merge(wer_df, perf_df, on="file", how="outer")
    out = "results/metrics/run_summary_combined.csv"
    merged.to_csv(out, index=False)
    print(f"✅ wrote {out} ({len(merged)} rows)")
else:
    print("⚠️ missing data: wer_df or perf_df empty")
