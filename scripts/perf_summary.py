#!/usr/bin/env python
import os, glob, json, re, csv

os.makedirs("results/metrics", exist_ok=True)
out = "results/metrics/perf_summary.csv"

lang_re = re.compile(r"/(mn|hu|fr|es)/", re.IGNORECASE)

def to_float(x):
    try:
        if isinstance(x, (list, tuple)) and len(x)==1:
            x = x[0]
        if isinstance(x, str):
            x = x.strip()
            if not x:
                return None
            return float(x)
        try:
            import numpy as np
            if isinstance(x, np.generic):
                return float(x)
            if isinstance(x, np.ndarray) and x.size==1:
                return float(x.reshape(()))
        except Exception:
            pass
        if isinstance(x, (int, float)):
            return float(x)
    except Exception:
        return None
    return None

sums = {}   # lang -> dict of metric sums
counts = {} # lang -> count

for f in glob.glob("results/metrics/perf_*.json"):
    try:
        with open(f, "r", encoding="utf-8", errors="ignore") as fh:
            d = json.load(fh)
    except Exception:
        continue

    audio = d.get("audio")
    if not isinstance(audio, str):
        continue
    m = lang_re.search("/" + audio.replace("\\","/") + "/")
    lang = m.group(1).lower() if m else None
    if not lang:
        continue

    elapsed = to_float(d.get("elapsed_sec"))
    rtf     = to_float(d.get("rtf"))
    cpu     = to_float(d.get("cpu_avg_pct"))
    rss     = to_float(d.get("rss_peak_mb"))

    if lang not in sums:
        sums[lang] = {"elapsed":0.0, "rtf":0.0, "cpu_avg_pct":0.0, "rss_peak_mb":0.0}
        counts[lang] = 0

    # only add if metric is present
    if elapsed is not None: sums[lang]["elapsed"] += elapsed
    if rtf     is not None: sums[lang]["rtf"]     += rtf
    if cpu     is not None: sums[lang]["cpu_avg_pct"] += cpu
    if rss     is not None: sums[lang]["rss_peak_mb"] += rss
    counts[lang] += 1

rows=[]
for lang in sorted(sums.keys()):
    c = max(1, counts[lang])
    agg = {k: (v/c if c else None) for k,v in sums[lang].items()}
    rows.append({
        "lang": lang,
        "elapsed": round(agg["elapsed"], 3),
        "rtf": round(agg["rtf"], 3),
        "cpu_avg_pct": round(agg["cpu_avg_pct"], 3),
        "rss_peak_mb": round(agg["rss_peak_mb"], 3),
    })

with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["lang","elapsed","rtf","cpu_avg_pct","rss_peak_mb"])
    w.writeheader()
    for r in rows:
        w.writerow(r)

print(f"✅ wrote {out}")
for r in rows:
    print(f"{r['lang']:>3}  elapsed={r['elapsed']:<5}  rtf={r['rtf']:<5}  cpu={r['cpu_avg_pct']:<5}  rss_mb={r['rss_peak_mb']:<5}")
