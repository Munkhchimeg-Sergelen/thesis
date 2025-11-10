PY=python
MODEL ?= tiny
DEVICE ?= cpu
OUT=results

# ===== Whisper ASR =====
run_whisper_hinted:
	$(PY) scripts/run_whisper.py --mode hinted --model $(MODEL) --device $(DEVICE) --infile $(FILE) --hint-lang $(LANG) --outdir $(OUT)/transcripts

run_whisper_lid:
	$(PY) scripts/run_whisper.py --mode lid2asr --model $(MODEL) --device $(DEVICE) --infile $(FILE) --outdir $(OUT)/transcripts

# ===== Wav2Vec2 ASR (Second System) =====
run_wav2vec2_hinted:
	$(PY) scripts/asr_wav2vec2.py --mode hinted --device $(DEVICE) --infile $(FILE) --hint-lang $(LANG) --outdir $(OUT)/transcripts --save-json

run_wav2vec2_lid:
	$(PY) scripts/asr_wav2vec2.py --mode lid2asr --device $(DEVICE) --infile $(FILE) --outdir $(OUT)/transcripts --save-json

# ===== Language ID =====
lid:
	$(PY) scripts/lid_from_whisper.py --model $(MODEL) --device $(DEVICE) --infile $(FILE)

# ===== Evaluation =====
eval:
	$(PY) scripts/eval_metrics.py --refs $(REFS) --hyps_dir $(HYPDIR) --out_csv $(OUT)/metrics/wer_cer_$$(date +%s).csv

perf:
	$(PY) scripts/measure_perf.py --cmd "$(CMD)" --audio $(FILE) --out $(OUT)/metrics/perf_$$(date +%s).json
