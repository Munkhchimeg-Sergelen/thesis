import json, sys
from jiwer import wer

if len(sys.argv) != 3:
    print("Usage: python src/eval_wer.py <preds.jsonl> <refs.jsonl>")
    sys.exit(1)

preds_fp, refs_fp = sys.argv[1], sys.argv[2]

preds = {json.loads(l)["audio"]: json.loads(l)["text"] for l in open(preds_fp, encoding="utf-8")}
refs  = {json.loads(l)["audio"]: json.loads(l)["ref"]  for l in open(refs_fp,  encoding="utf-8")}

pairs = [(refs[k], preds.get(k,"")) for k in refs]
score = wer([r for r,_ in pairs],[p for _,p in pairs])

print(f"WER: {score:.3f} (lower is better)")
