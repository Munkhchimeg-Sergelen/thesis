#!/usr/bin/env python
import argparse, json, time, os, psutil, wave, contextlib
from subprocess import Popen, PIPE

ap = argparse.ArgumentParser()
ap.add_argument("--cmd", required=True, help="Command to run the ASR (quoted)")
ap.add_argument("--audio", required=True, help="Path to the audio file used")
ap.add_argument("--out", default="results/metrics/perf_run.json")
args = ap.parse_args()

def dur_sec(wav):
    with contextlib.closing(wave.open(wav,'r')) as wf:
        return wf.getnframes()/float(wf.getframerate())

start = time.time()
p = Popen(args.cmd, shell=True, stdout=PIPE, stderr=PIPE)
cpu_samples = []
rss_samples = []
try:
    ps = psutil.Process(p.pid)
except psutil.Error:
    ps = None

while p.poll() is None and ps:
    try:
        cpu_samples.append(ps.cpu_percent(interval=0.2))
        rss_samples.append(ps.memory_info().rss)
    except psutil.Error:
        break

stdout, stderr = p.communicate()
elapsed = time.time() - start
audio_dur = dur_sec(args.audio)
rtf = elapsed / max(audio_dur, 1e-6)

out = {
  "cmd": args.cmd,
  "audio": args.audio,
  "elapsed_sec": round(elapsed,3),
  "audio_sec": round(audio_dur,3),
  "rtf": round(rtf,3),
  "cpu_avg_pct": round(sum(cpu_samples)/len(cpu_samples),1) if cpu_samples else None,
  "rss_peak_mb": round(max(rss_samples)/1e6,1) if rss_samples else None,
  "stderr_tail": stderr.decode("utf-8")[-400:]
}
os.makedirs(os.path.dirname(args.out), exist_ok=True)
open(args.out,"w",encoding="utf-8").write(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))


# --- GPU VRAM logging hook (activates on CUDA) ---
try:
    import torch
    import pynvml
    if torch.cuda.is_available():
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        print(f"GPU VRAM used: {info.used/1e6:.1f} MB / {info.total/1e6:.1f} MB total")
except Exception as e:
    pass
