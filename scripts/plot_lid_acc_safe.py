#!/usr/bin/env python
import csv, sys, os
import matplotlib.pyplot as plt

csv_path = sys.argv[1] if len(sys.argv) > 1 else "results/metrics/lid_accuracy.csv"

langs, accs = [], []
with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
    r = csv.DictReader(f)
    # try common headers; fall back to case/space-insensitive keys
    for row in r:
        keys = {k.lower().replace(" ", ""): k for k in row.keys()}
        k_lang = keys.get("lang") or keys.get("language") or "lang"
        k_acc  = keys.get("acc") or keys.get("accuracy") or "acc"
        lang = row.get(k_lang)
        acc = row.get(k_acc)
        if not lang or acc is None:
            continue
        try:
            acc_val = float(str(acc).strip())
        except Exception:
            continue
        langs.append(lang)
        accs.append(acc_val)

if not langs:
    print("No usable rows found in", csv_path)
else:
    os.makedirs("docs/figs", exist_ok=True)
    # sort by language code for stable order
    pairs = sorted(zip(langs, accs), key=lambda x: x[0])
    langs, accs = zip(*pairs)
    import matplotlib.pyplot as plt
    plt.bar(langs, accs)
    plt.ylim(0,1)
    plt.ylabel("LID accuracy")
    plt.title("LID accuracy by language")
    plt.tight_layout()
    out = "docs/figs/lid_acc_by_lang.png"
    plt.savefig(out, dpi=200)
    print("✅ saved", out)
