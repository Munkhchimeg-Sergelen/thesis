PY=python
MODEL ?= tiny
DEVICE ?= cpu
OUT=results

run_whisper_hinted:
	$(PY) scripts/run_whisper.py --mode hinted --model $(MODEL) --device $(DEVICE) --infile $(FILE) --hint-lang $(LANG) --outdir $(OUT)/transcripts

run_whisper_lid:
	$(PY) scripts/run_whisper.py --mode lid2asr --model $(MODEL) --device $(DEVICE) --infile $(FILE) --outdir $(OUT)/transcripts

lid:
	$(PY) scripts/lid_from_whisper.py --model $(MODEL) --device $(DEVICE) --infile $(FILE)

eval:
	$(PY) scripts/eval_metrics.py --refs $(REFS) --hyps_dir $(HYPDIR) --out_csv $(OUT)/metrics/wer_cer_$$(date +%s).csv

perf:
	$(PY) scripts/measure_perf.py --cmd "$(CMD)" --audio $(FILE) --out $(OUT)/metrics/perf_$$(date +%s).json
