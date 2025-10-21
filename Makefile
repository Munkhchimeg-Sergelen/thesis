.PHONY: test_lid run_whisper_small_all metrics perf manifests

PY=python
DATA=data/wav
OUT=results
WHMODEL=small  # change to tiny/small/base as you wish
DEVICE=cpu     # set to cuda on the GPU server

test_lid:
	$(PY) scripts/lid_from_whisper.py --in $(DATA) --model $(WHMODEL) --head-sec 8 --device $(DEVICE) --out $(OUT)/logs/lid

run_whisper_small_all:
	$(PY) scripts/asr_whisper.py --mode lid2asr --in $(DATA) --model $(WHMODEL) --device $(DEVICE) --out $(OUT)/transcripts/lid2asr/whisper
	$(PY) scripts/asr_whisper.py --mode hinted  --in $(DATA) --model $(WHMODEL) --device $(DEVICE) --out $(OUT)/transcripts/hinted/whisper

manifests:
	$(PY) scripts/make_manifest.py --in $(DATA) --out results/manifests

metrics:
	$(PY) scripts/eval_metrics.py --hyp-dir $(OUT)/transcripts --out $(OUT)/metrics/wer_cer.csv

perf:
	$(PY) scripts/measure_perf.py --in $(DATA) --system whisper-$(WHMODEL) --device $(DEVICE) --out $(OUT)/metrics/perf.csv
