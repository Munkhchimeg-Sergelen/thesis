#!/usr/bin/env python3
import csv, os, collections

IN = "results/metrics/run_summary.csv"
OUT1 = "results/metrics/lid_accuracy.csv"
OUT2 = "results/metrics/lid_confusion.csv"

LANGS = ["mn","hu","fr","es"]

def main():
    os.makedirs("results/metrics", exist_ok=True)
    tot = 0; correct = 0
    by_lang = collections.Counter()
    by_lang_ok = collections.Counter()
    by_bucket = collections.Counter()
    by_bucket_ok = collections.Counter()
    conf = {g:{p:0 for p in LANGS+["en","ko","unk"]} for g in LANGS+["unk"]}

    with open(IN, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            # use only files where we know ground-truth language from path
            g = row["path_lang"]
            p = row.get("lid_pred","unk") or "unk"
            b = row.get("bucket","") or ""
            if g not in LANGS and g != "unk":  # ignore 'en' and others for LID evaluation
                continue
            tot += 1
            by_lang[g]+=1
            by_bucket[b]+=1
            ok = (g == p)
            if ok:
                correct += 1; by_lang_ok[g]+=1; by_bucket_ok[b]+=1
            conf[g][p] = conf.get(g, {}).get(p, 0) + 1

    # write accuracy tables
    with open(OUT1, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["scope","key","n","acc"])
        w.writerow(["overall","all",tot, f"{(correct/tot):.4f}" if tot else ""])
        for g in LANGS+["unk"]:
            n = by_lang[g]; ok = by_lang_ok[g]
            w.writerow(["per_lang", g, n, f"{(ok/n):.4f}" if n else ""])
        for b in sorted(by_bucket):
            n = by_bucket[b]; ok = by_bucket_ok[b]
            w.writerow(["per_bucket", b, n, f"{(ok/n):.4f}" if n else ""])

    # write confusion matrix
    cols = LANGS+["en","ko","unk"]
    with open(OUT2, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["gold\\pred"] + cols)
        for g in LANGS+["unk"]:
            w.writerow([g] + [conf.get(g,{}).get(p,0) for p in cols])

    print("LID accuracy →", OUT1)
    print("LID confusion →", OUT2)

if __name__ == "__main__":
    main()
