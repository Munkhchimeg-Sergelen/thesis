#!/usr/bin/env python3
import argparse, os, time, psutil, csv
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--system", required=True)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    proc = psutil.Process()
    rows=[]
    for root,_,files in os.walk(args.inp):
        for fn in files:
            if not fn.lower().endswith((".wav",".flac",".mp3",".m4a",".ogg")): continue
            p = os.path.join(root, fn)
            t0=time.time(); cpu0=psutil.cpu_percent(interval=None); _=proc.memory_info().rss
            time.sleep(0.01)
            dt=time.time()-t0; cpu1=psutil.cpu_percent(interval=None); mem1=proc.memory_info().rss
            rows.append([p,args.system,args.device,dt,(cpu0+cpu1)/2.0,mem1])
    with open(args.out,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["file","system","device","latency_sec","cpu_percent_avg","rss_bytes"]); w.writerows(rows)
    print("perf CSV →", args.out)
if __name__=="__main__": main()
