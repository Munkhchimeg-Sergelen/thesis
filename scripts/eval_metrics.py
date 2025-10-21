#!/usr/bin/env python3
import argparse, os, csv
from jiwer import wer, cer
LANGS={"mn","hu","fr","es"}
def lang_of_path(p):
    for pr in p.replace("\\","/").split("/"):
        if pr in LANGS: return pr
    return "unk"
def read_hypotheses(hyp_dir):
    outs=[]
    for root,_,files in os.walk(hyp_dir):
        for fn in files:
            if fn.endswith(".txt"):
                p=os.path.join(root,fn)
                with open(p,"r",encoding="utf-8") as f: txt=f.read().strip()
                outs.append((p,lang_of_path(p),fn.rsplit(".",1)[0],txt))
    return outs
def read_reference(ref_dir, lang, base):
    rp=os.path.join(ref_dir,lang,base+".txt")
    if os.path.exists(rp):
        with open(rp,"r",encoding="utf-8") as f: return f.read().strip(), rp
    return None,None
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--hyp-dir",required=True)
    ap.add_argument("--ref-dir",required=False)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    os.makedirs(os.path.dirname(args.out),exist_ok=True)
    hyps=read_hypotheses(args.hyp_dir)
    with open(args.out,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["hyp_file","lang","mode","system","base","wer","cer","has_ref","ref_file"])
        for hyp_file,lang,base,hyp in hyps:
            parts=hyp_file.replace("\\","/").split("/")
            mode=parts[parts.index("transcripts")+1] if "transcripts" in parts else "unk"
            system=parts[parts.index("transcripts")+2] if "transcripts" in parts else "unk"
            ref_text,ref_file=(None,None)
            if args.ref_dir: ref_text,ref_file=read_reference(args.ref_dir,lang,base)
            if ref_text:
                w.writerow([hyp_file,lang,mode,system,base,f"{wer(ref_text,hyp):.4f}",f"{cer(ref_text,hyp):.4f}",1,ref_file])
            else:
                w.writerow([hyp_file,lang,mode,system,base,"","",0,""])
    print("metrics CSV →",args.out)
if __name__=="__main__": main()
