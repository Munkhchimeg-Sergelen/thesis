#!/usr/bin/env python
import pandas as pd, glob, os, json, math

def as_float(x):
    # coerce lists/tuples/arrays/strings to float where possible
    try:
        # unwrap 1-length containers
        if isinstance(x, (list, tuple)) and len(x)==1:
            x = x[0]
        # strings like "0.94" -> 0.94
        if isinstance(x, str):
            x = x.strip()
            if x == "": return None
            return float(x)
        # numpy scalars
        try:
            import numpy as np
            if isinstance(x, (np.generic,)):
                return float(x)  # type: ignore
        except Exception:
            pass
        # plain numbers
        if isinstance(x, (int, float)):
            return float(x)
    except Exception:
        return None
    return None

def as_str(x):
    return str(x) if isinstance(x, str) else None

files = sorted(glob.glob("results/metrics/perf_*.json"))
rows=[]; bad=[]

for f in files:
    try:
        d = json.load(open(f, encoding="utf-8"))
        if not isinstance(d, dict):
            raise ValueError("json root is not an object")
        row = {
            "file": as_str(d.get("audio")),
            "elapsed": as_float(d.get("elapsed_sec")),
            "rtf": as_float(d.get("rtf")),
            "cpu_avg_pct": as_float(d.get("cpu_avg_pct")),
            "rss_peak_mb": as_float(d.get("rss_peak_mb")),
        }
        # minimal sanity: need file path and an rtf
        if not row["file"] or row["rtf"] is None:
            raise ValueError("missing file or rtf")
        rows.append(row)
    except Exception as e:
        bad.append((f, str(e)))

if bad:
    print("⚠️ Skipped {} perf JSONs due to format issues:".format(len(bad)))
    for f, msg in bad[:5]:
        print(" -", f, "→", msg)
    if len(bad) > 5:
        print("   ...")

if not rows:
    print("no valid perf files")
    raise SystemExit(0)

df = pd.DataFrame(rows)

# derive language from file path
df["lang"] = df["file"].str.extract(r"/(mn|hu|fr|es)/", expand=False)

# aggregate means per language
summary = (df.dropna(subset=["lang"])
             .groupby("lang")[["elapsed","rtf","cpu_avg_pct","rss_peak_mb"]]
             .mean()
             .reset_index()
             .round(3))

os.makedirs("results/metrics", exist_ok=True)
out = "results/metrics/perf_summary.csv"
summary.to_csv(out, index=False)
print(f"✅ wrote {out}")
print(summary.to_string(index=False))
