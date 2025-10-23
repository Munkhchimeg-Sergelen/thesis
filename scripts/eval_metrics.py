#!/usr/bin/env python3
import argparse, os, csv, json, re
from pathlib import Path
from jiwer import wer, cer, Compose, ToLowerCase, RemovePunctuation, RemoveMultipleSpaces, Strip, RemoveWhiteSpace, RemoveEmptyStrings

def preproc(t: str) -> str:
    if t is None: return ""
    t = t.lower()
    t = re.sub(r"\d+", " ", t)
    t = re.sub(r"[^\w\s]", " ", t, flags=re.UNICODE)
    t = re.sub(r"\s+", " ", t).strip()
    return t

TRANSFORMS = Compose([ToLowerCase(), RemovePunctuation(), RemoveMultipleSpaces(), Strip(),
                      RemoveWhiteSpace(replace_by_space=True), RemoveEmptyStrings()])

def read_text(p):
    try:
        return Path(p).read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hyp-dir", required=True)
    ap.add_argument("--ref-dir", default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    rows = []
    for root, _, files in os.walk(args.hyp_dir):
        for fn in files:
            if not fn.lower().endswith(".txt"): continue
            hyp_file = os.path.join(root, fn)
            base = os.path.splitext(fn)[0]

            # infer lang/mode/system from path parts
            parts = Path(hyp_file).parts
            lang = "unk"; mode = ""; system = ""
            # Expect something like: results/transcripts/<mode>/<system>/<lang>/txt/<file>.txt
            if "transcripts" in parts:
                i = parts.index("transcripts")
                if i+1 < len(parts): mode = parts[i+1]
                if i+2 < len(parts): system = parts[i+2]
                if i+3 < len(parts): lang = parts[i+3]
            # Older layouts fallback
            for p in parts:
                if p in ("mn","hu","fr","es","en","ko"): lang = p

            hyp = read_text(hyp_file)
            has_ref = 0; ref_file = ""
            w = ""; c = ""

            if args.ref_dir:
                ref_candidate = os.path.join(args.ref_dir, lang, base + ".txt")
                if os.path.isfile(ref_candidate):
                    ref = read_text(ref_candidate)
                    # normalized scoring
                    hyp_n = TRANSFORMS(preproc(hyp))
                    ref_n = TRANSFORMS(preproc(ref))
                    w = f"{wer(ref_n, hyp_n):.4f}" if ref_n else ""
                    c = f"{cer(ref_n, hyp_n):.4f}" if ref_n else ""
                    has_ref = 1; ref_file = ref_candidate

            rows.append({
                "hyp_file": hyp_file,
                "lang": lang,
                "mode": mode,
                "system": system,
                "base": base,
                "wer": w,
                "cer": c,
                "has_ref": has_ref,
                "ref_file": ref_file
            })

    Path(os.path.dirname(args.out)).mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else
                            ["hyp_file","lang","mode","system","base","wer","cer","has_ref","ref_file"])
        wr.writeheader()
        wr.writerows(rows)
    print(f"metrics CSV → {args.out}")

if __name__ == "__main__":
    main()
