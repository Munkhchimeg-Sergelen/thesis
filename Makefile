.PHONY: test_lid run_whisper_small_all metrics perf manifests

PY=python
DATA=data/wav
OUT=results
WHMODEL=tiny  # change to tiny/small/base as you wish
DEVICE=cpu     # set to cuda on the GPU server

test_lid:
	$(PY) scripts/lid_from_whisper.py --in $(DATA) --model $(WHMODEL) --head-sec 8 --device $(DEVICE) --out $(OUT)/logs/lid

run_whisper_small_all:
	$(PY) scripts/asr_whisper.py --mode lid2asr --in $(DATA) --model $(WHMODEL) --device $(DEVICE) --out $(OUT)/transcripts/lid2asr/whisper
	$(PY) scripts/asr_whisper.py --mode hinted  --in $(DATA) --model $(WHMODEL) --device $(DEVICE) --out $(OUT)/transcripts/hinted/whisper

manifests:
	$(PY) scripts/make_manifest.py --in $(DATA) --out results/manifests

metrics:

summary:
	$(PY) scripts/run_summary.py --out $(OUT)/metrics/run_summary.csv
	$(PY) scripts/eval_metrics.py --hyp-dir $(OUT)/transcripts --out $(OUT)/metrics/wer_cer.csv

perf:
	$(PY) scripts/measure_perf.py --in $(DATA) --system whisper-$(WHMODEL) --device $(DEVICE) --out $(OUT)/metrics/perf.csv

most:
	$(PY) scripts/assemble_most.py

metrics_with_ref:
	PYTHONUTF8=1 $(PY) scripts/eval_metrics.py --hyp-dir $(OUT)/transcripts --ref-dir data/ref --out $(OUT)/metrics/wer_cer_with_ref.csv

run_faster_whisper:
	$(PY) scripts/asr_faster_whisper.py --mode hinted --in $(DATA) --model tiny --device $(DEVICE) --out $(OUT)/transcripts/hinted/faster_whisper

run_whisper_tiny_cuda:
	$(PY) scripts/asr_whisper.py --mode hinted  --in $(DATA) --model tiny --device cuda --out $(OUT)/transcripts/hinted/whisper
	$(PY) scripts/asr_whisper.py --mode lid2asr --in $(DATA) --model tiny --device cuda --out $(OUT)/transcripts/lid2asr/whisper
	$(PY) scripts/eval_metrics.py --hyp-dir $(OUT)/transcripts --ref-dir data/ref --out $(OUT)/metrics/wer_cer_with_ref_cuda.csv

run_whisper_tiny_cuda:
	$(PY) scripts/asr_whisper.py --mode hinted  --in $(DATA) --model tiny --device cuda --out $(OUT)/transcripts/hinted/whisper_tiny_cuda
	$(PY) scripts/asr_whisper.py --mode lid2asr --in $(DATA) --model tiny --device cuda --out $(OUT)/transcripts/lid2asr/whisper_tiny_cuda

run_whisper_base_cuda:
	$(PY) scripts/asr_whisper.py --mode hinted  --in $(DATA) --model base --device cuda --out $(OUT)/transcripts/hinted/whisper_base_cuda
	$(PY) scripts/asr_whisper.py --mode lid2asr --in $(DATA) --model base --device cuda --out $(OUT)/transcripts/lid2asr/whisper_base_cuda

score_cuda:
	$(PY) scripts/eval_metrics.py --hyp-dir $(OUT)/transcripts --ref-dir data/ref --out $(OUT)/metrics/wer_cer_with_ref_cuda.csv
