#!/usr/bin/env python
import pandas as pd, matplotlib.pyplot as plt, os, sys
csv_path = sys.argv[1] if len(sys.argv) > 1 else "results/metrics/lid_accuracy.csv"
df = pd.read_csv(csv_path)
# expect columns: lang, acc (0..1)
if not {"lang","acc"}.issubset(df.columns):
    # some versions named it slightly differently; try to coerce
    cols = {c.lower().replace(" ", ""): c for c in df.columns}
    df = df.rename(columns={cols.get("lang","lang"): "lang",
                            cols.get("acc","acc"): "acc"})
df = df[["lang","acc"]].dropna().sort_values("lang")
os.makedirs("docs/figs", exist_ok=True)
plt.bar(df["lang"], df["acc"])
plt.ylim(0,1)
plt.ylabel("LID accuracy")
plt.title("LID accuracy by language")
plt.tight_layout()
plt.savefig("docs/figs/lid_acc_by_lang.png", dpi=200)
print("✅ saved docs/figs/lid_acc_by_lang.png")
