#!/usr/bin/env python3
import csv, glob, json, os, re
from collections import OrderedDict

OUT = "results/metrics/run_summary_combined.csv"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# --- collect perf metrics from JSON (by file) ---
perf_by_file = {}
for f in sorted(glob.glob("results/metrics/perf_*.json")):
    try:
        with open(f, "r", encoding="utf-8", errors="ignore") as fh:
            d = json.load(fh)
        audio = d.get("audio")
        if not isinstance(audio, str): 
            continue
        # flatten/clean
        def num(x):
            try:
                if isinstance(x, (list, tuple)) and len(x)==1: x=x[0]
                if isinstance(x, str): x=x.strip()
                return float(x)
            except Exception:
                return None
        perf_by_file[audio] = {
            "elapsed": num(d.get("elapsed_sec")),
            "rtf":     num(d.get("rtf")),
            "cpu_avg_pct": num(d.get("cpu_avg_pct")),
            "rss_peak_mb": num(d.get("rss_peak_mb")),
        }
    except Exception:
        continue

# --- helper: pull canonical header from arbitrary row keys ---
def norm_keys(row):
    # normalize keys: lowercase, remove spaces/underscores
    nk = {}
    for k in row.keys():
        if k is None: 
            continue
        kk = str(k).lower().replace(" ", "").replace("_", "")
        nk[kk] = k
    return nk

# --- collect WER/CER rows and merge perf columns ---
rows = []
lang_re = re.compile(r"/(mn|hu|fr|es)/", re.IGNORECASE)
for csv_path in sorted(glob.glob("results/metrics/wer_cer*.csv")):
    try:
        with open(csv_path, "r", encoding="utf-8", errors="ignore") as fh:
            r = csv.DictReader(fh)
            for row in r:
                if not row: 
                    continue
                nk = norm_keys(row)
                k_file  = nk.get("file") or nk.get("audio") or nk.get("path")
                if not k_file or not row.get(k_file):
                    continue
                file_path = row[k_file]
                # fix weird encodings/trailing junk
                file_path = str(file_path).strip()

                # identify lang from path
                m = lang_re.search("/" + file_path.replace("\\","/") + "/")
                lang = m.group(1).lower() if m else ""

                # optional fields
                k_mode  = nk.get("mode")   or nk.get("decodemode") or nk.get("pipeline")
                k_model = nk.get("model")  or nk.get("asrmodel")
                k_wer   = nk.get("wer")
                k_cer   = nk.get("cer")

                def tofloat(v):
                    try:
                        if isinstance(v, (list,tuple)) and len(v)==1: v=v[0]
                        v = str(v).strip()
                        if v == "": return None
                        return float(v)
                    except Exception:
                        return None

                merged = OrderedDict()
                merged["file"] = file_path
                merged["lang"] = lang
                if k_mode:  merged["mode"]  = row.get(k_mode, "")
                if k_model: merged["model"] = row.get(k_model, "")
                merged["wer"] = tofloat(row.get(k_wer)) if k_wer else None
                merged["cer"] = tofloat(row.get(k_cer)) if k_cer else None

                # attach perf if we have it
                p = perf_by_file.get(file_path)
                if p:
                    merged["elapsed"]     = p.get("elapsed")
                    merged["rtf"]         = p.get("rtf")
                    merged["cpu_avg_pct"] = p.get("cpu_avg_pct")
                    merged["rss_peak_mb"] = p.get("rss_peak_mb")
                else:
                    merged["elapsed"] = merged["rtf"] = merged["cpu_avg_pct"] = merged["rss_peak_mb"] = None

                rows.append(merged)
    except Exception:
        continue

# If no WER/CER CSVs, at least dump perf as rows
if not rows and perf_by_file:
    for file_path, p in perf_by_file.items():
        m = lang_re.search("/" + file_path.replace("\\","/") + "/")
        lang = m.group(1).lower() if m else ""
        rows.append(OrderedDict({
            "file": file_path,
            "lang": lang,
            "mode": "",
            "model": "",
            "wer": None,
            "cer": None,
            "elapsed": p.get("elapsed"),
            "rtf": p.get("rtf"),
            "cpu_avg_pct": p.get("cpu_avg_pct"),
            "rss_peak_mb": p.get("rss_peak_mb"),
        }))

# stable header order
header = ["file","lang","mode","model","wer","cer","elapsed","rtf","cpu_avg_pct","rss_peak_mb"]

# write clean CSV via stdlib
with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=header)
    w.writeheader()
    for row in rows:
        # ensure only known keys in output
        w.writerow({k: row.get(k, "") for k in header})

print(f"✅ wrote {OUT} ({len(rows)} rows)")
