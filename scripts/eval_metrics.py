#!/usr/bin/env python3
import argparse, os, csv
def read_transcripts(hyp_dir):
    outs=[]
    for root,_,files in os.walk(hyp_dir):
        for fn in files:
            if fn.endswith(".txt"):
                p=os.path.join(root,fn)
                with open(p,"r",encoding="utf-8") as f: txt=f.read().strip()
                parts=root.replace("\\","/").split("/")
                lang="unk"
                for l in ("mn","hu","fr","es"):
                    if l in parts: lang=l
                outs.append((p,lang,txt))
    return outs
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--hyp-dir", required=True)
    ap.add_argument("--out", required=True)
    args=ap.parse_args()
    hyps=read_transcripts(args.hyp_dir)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out,"w",newline="",encoding="utf-8") as f:
        from csv import writer; w=writer(f); w.writerow(["file","lang","wer","cer","notes"])
        for p,lang,_ in hyps: w.writerow([p,lang,"","","no_ref_yet"])
    print("metrics CSV →", args.out)
if __name__=="__main__": main()
