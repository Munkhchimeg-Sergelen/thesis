#!/usr/bin/env python
import os, glob, json, re
import matplotlib.pyplot as plt

lang_re = re.compile(r"/(mn|hu|fr|es)/", re.IGNORECASE)

sums = {}
counts = {}

for f in glob.glob("results/metrics/perf_*.json"):
    try:
        with open(f, "r", encoding="utf-8", errors="ignore") as fh:
            d = json.load(fh)
        audio = d.get("audio")
        rtf = d.get("rtf")
        if not isinstance(audio, str):
            continue
        m = lang_re.search("/" + audio.replace("\\","/") + "/")
        lang = m.group(1).lower() if m else None
        # coerce rtf to float if possible
        if isinstance(rtf, (list, tuple)) and len(rtf)==1:
            rtf = rtf[0]
        if isinstance(rtf, str):
            rtf = float(rtf.strip())
        if not isinstance(rtf, (int, float)):
            continue
        if lang:
            sums[lang] = sums.get(lang, 0.0) + float(rtf)
            counts[lang] = counts.get(lang, 0) + 1
    except Exception:
        continue

langs = sorted(sums.keys())
vals = [sums[L]/counts[L] for L in langs] if langs else []

os.makedirs("docs/figs", exist_ok=True)
if not langs:
    print("No usable perf JSONs found for plotting.")
else:
    plt.bar(langs, vals)
    plt.ylabel("Average Real-Time Factor (CPU)")
    plt.title("RTF per language")
    plt.tight_layout()
    out = "docs/figs/rtf_by_lang.png"
    plt.savefig(out, dpi=200)
    print("✅ saved", out)
