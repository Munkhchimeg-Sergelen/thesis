# Metrics schema
- **WER/CER**: lower-case, remove digits & punctuation, collapse spaces (see `scripts/eval_metrics.py`).
- **Latency (sec)** & **RTF**: from `run_summary.csv` (latency / audio_sec).
- **LID**: accuracy + confusion (per-lang, per-bucket), threshold-free (argmax).
- **Hardware context**: CPU model, RAM; on GPU: CUDA, driver, VRAM.
- **Bucket**: 10/30/120s (from manifests).
