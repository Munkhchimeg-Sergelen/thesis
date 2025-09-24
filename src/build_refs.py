import json, os, sys

preds_fp = "experiments/whisper_tiny/preds.jsonl"
refs_fp  = "experiments/refs.jsonl"

print("Opening:", preds_fp)
pairs = []
with open(preds_fp, encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        audio = item["audio"]
        print("\nAUDIO:", audio)
        print("MODEL:", item["text"])
        ref = input("Your exact reference text (leave blank to skip): ").strip()
        if ref:
            pairs.append({"audio": audio, "ref": ref})

os.makedirs("experiments", exist_ok=True)
with open(refs_fp, "w", encoding="utf-8") as w:
    for p in pairs:
        w.write(json.dumps(p, ensure_ascii=False)+"\n")

print("\nWrote ->", refs_fp)
