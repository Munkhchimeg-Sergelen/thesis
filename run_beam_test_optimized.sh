#!/bin/bash
# Optimized beam search test - loads model once per language

echo "Starting optimized beam search comparison..."
echo "This will take ~2-3 hours (much faster than old script!)"
echo ""

python scripts/test_beam_batch.py \
    --languages mn hu es fr \
    --model small \
    --beam-sizes 1 5 \
    --device cpu \
    --audio-dir data/wav \
    --output-dir results/beam_comparison

echo ""
echo "✅ Beam comparison complete!"
