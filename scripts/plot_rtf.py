#!/usr/bin/env python
import pandas as pd, matplotlib.pyplot as plt, os
df = pd.read_csv("results/metrics/perf_summary.csv")  # columns: lang, rtf, ...
if not {"lang","rtf"}.issubset(df.columns):
    raise SystemExit("perf_summary.csv missing required columns")
df = df.sort_values("lang")
os.makedirs("docs/figs", exist_ok=True)
plt.bar(df["lang"], df["rtf"])
plt.ylabel("Average Real-Time Factor (CPU)")
plt.title("RTF per language")
plt.tight_layout()
plt.savefig("docs/figs/rtf_by_lang.png", dpi=200)
print("✅ saved docs/figs/rtf_by_lang.png")
