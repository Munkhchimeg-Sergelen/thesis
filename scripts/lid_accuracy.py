#!/usr/bin/env python
import glob, json, os, csv, re, time
import statistics as stats

LANG_RE = re.compile(r"/(mn|hu|fr|es)/", re.IGNORECASE)

def folder_lang(path):
    m = LANG_RE.search("/" + path.replace("\\","/") + "/")
    return (m.group(1).lower() if m else None)

files = sorted(glob.glob("results/transcripts/lid2asr/whisper/*/*.json"))
rows = []
for j in files:
    d = json.load(open(j, encoding="utf-8"))
    # derive paths/fields
    hyp_txt = j.replace(".json",".txt")
    file_in = d.get("file") or ""
    true_lang = folder_lang(file_in) or folder_lang(j)  # prefer data path; fallback to results path
    lid_lang = d.get("lid_language")   # from LID stage
    lid_prob = d.get("lid_prob")
    used_lang = d.get("language_used") # language used for transcription (may be fallback)
    fallback = d.get("fallback") or ("folder_on_low_conf" if isinstance(d.get("tried"), list) and "fallback:folder" in d.get("tried") else None)

    rows.append({
        "file": file_in,
        "true_lang": true_lang,
        "lid_lang": lid_lang,
        "lid_prob": lid_prob,
        "used_lang": used_lang,
        "fallback": fallback,
        "hyp_file": hyp_txt
    })

# write per-file table
os.makedirs("results/metrics", exist_ok=True)
ts = int(time.time())
per_file_csv = f"results/metrics/lid_per_file_{ts}.csv"
with open(per_file_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["file","true_lang","lid_lang","lid_prob","used_lang","fallback","hyp_file"])
    w.writeheader(); w.writerows(rows)
print(f"✅ wrote {per_file_csv} ({len(rows)} rows)")

# aggregate by true_lang
by_lang = {}
for r in rows:
    tl = r["true_lang"]
    if not tl: continue
    by_lang.setdefault(tl, {"n":0,"correct":0,"lowconf":0,"probs":[]})
    by_lang[tl]["n"] += 1
    if r["lid_lang"] == tl: by_lang[tl]["correct"] += 1
    if r["lid_prob"] is not None and r["lid_prob"] < 0.60: by_lang[tl]["lowconf"] += 1
    if isinstance(r["lid_prob"], (int,float)): by_lang[tl]["probs"].append(r["lid_prob"])

agg_csv = f"results/metrics/lid_accuracy_{ts}.csv"
with open(agg_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["lang","n","correct","acc","low_conf(<0.60)","median_prob"])
    w.writeheader()
    for lang, s in sorted(by_lang.items()):
        acc = (s["correct"]/s["n"]) if s["n"] else 0
        med = (stats.median(s["probs"]) if s["probs"] else "")
        w.writerow({"lang":lang,"n":s["n"],"correct":s["correct"],"acc":round(acc,3),"low_conf(<0.60)":s["lowconf"],"median_prob":med})
print(f"✅ wrote {agg_csv}")
