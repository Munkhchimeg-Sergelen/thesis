#!/usr/bin/env bash
set -euo pipefail

MODEL="${MODEL:-tiny}"
DEVICE="${DEVICE:-cpu}"
LANGS="${LANGS:-hu fr es mn}"

export CT2_FORCE_CPU=1

for L in $LANGS; do
  DIR="data/wav/$L"
  [ -d "$DIR" ] || { echo "skip $L (no $DIR)"; continue; }
  echo "=== $L ==="
  for f in "$DIR"/*.wav; do
    [ -e "$f" ] || continue
    echo "hinted → $f"
    python scripts/run_whisper.py --mode hinted --model "$MODEL" --device "$DEVICE" --infile "$f" --hint-lang "$L"
    echo "lid2asr → $f"
    python scripts/run_whisper.py --mode lid2asr --model "$MODEL" --device "$DEVICE" --infile "$f"
  done
done
