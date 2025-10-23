#!/usr/bin/env python3
import argparse, os, json, time, whisper, csv
from collections import defaultdict

LANGS = {"mn","hu","fr","es"}
AUDIO_EXTS = (".wav",".flac",".mp3",".m4a",".ogg")

def lang_from_path(p):
    parts = p.replace("\\","/").split("/")
    for t in parts:
        if t in LANGS: return t
    return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="data/wav")
    ap.add_argument("--out", default="results/transcripts/sweep/whisper")
    ap.add_argument("--model", default="tiny")
    ap.add_argument("--limit-per-lang", type=int, default=5, help="how many files per language")
    args=ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    model=whisper.load_model(args.model, device="cpu")
    grid=[{"beam_size":1, "temperature":0.0, "best_of":1, "tag":"b1_t0_bo1"},
          {"beam_size":5, "temperature":0.0, "best_of":1, "tag":"b5_t0_bo1"},
          {"beam_size":1, "temperature":0.2, "best_of":3, "tag":"b1_t02_bo3"}]

    picked=defaultdict(list)
    for root,_,files in os.walk(args.inp):
        for fn in sorted(files):
            if not fn.lower().endswith(AUDIO_EXTS): continue
            p=os.path.join(root,fn)
            lang=lang_from_path(p)
            if not lang: continue
            if len(picked[lang]) < args.limit_per_lang:
                picked[lang].append(p)

    rows=[]
    for lang, paths in picked.items():
        for path in paths:
            base=os.path.splitext(os.path.basename(path))[0]
            for cfg in grid:
                t0=time.time()
                out=model.transcribe(path, language=lang, task="transcribe",
                                     beam_size=cfg["beam_size"],
                                     temperature=cfg["temperature"],
                                     best_of=cfg["best_of"],
                                     fp16=False)
                dt=time.time()-t0
                text=(out.get("text") or "").strip()
                info={k:out.get(k) for k in ("avg_logprob","compression_ratio","no_speech_prob")}

                tag=cfg["tag"]
                out_txt_dir=os.path.join(args.out, tag, lang, "txt")
                out_js_dir =os.path.join(args.out, tag, lang, "json")
                os.makedirs(out_txt_dir, exist_ok=True)
                os.makedirs(out_js_dir,  exist_ok=True)
                with open(os.path.join(out_txt_dir, base+".txt"),"w",encoding="utf-8") as f: f.write(text)
                side={"file":path,"lang":lang,"cfg":cfg,"latency_sec":dt}|(info or {})
                with open(os.path.join(out_js_dir, base+".json"),"w",encoding="utf-8") as f: json.dump(side,f,ensure_ascii=False,indent=2)
                rows.append([path,lang,tag,dt,info.get("avg_logprob"),info.get("no_speech_prob")])

    os.makedirs("results/metrics", exist_ok=True)
    with open("results/metrics/sweep_index.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["file","lang","tag","latency_sec","avg_logprob","no_speech_prob"]); w.writerows(rows)
    print("sweep outputs →", args.out)
    print("sweep index   → results/metrics/sweep_index.csv")
if __name__=="__main__":
    main()
