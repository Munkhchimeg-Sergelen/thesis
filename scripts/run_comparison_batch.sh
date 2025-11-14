#!/bin/bash
# Run full system comparison (Whisper vs Wav2Vec2)
# Usage: ./scripts/run_comparison_batch.sh [whisper_model] [device]

set -e

WHISPER_MODEL=${1:-small}
DEVICE=${2:-cpu}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="results/comparison_${TIMESTAMP}"

echo "======================================"
echo "🔬 System Comparison Batch Run"
echo "======================================"
echo "Whisper Model: ${WHISPER_MODEL}"
echo "Device: ${DEVICE}"
echo "Output: ${OUTDIR}"
echo

# Check audio files (both WAV and MP3)
AUDIO_COUNT=$(find data/wav \( -name "*.wav" -o -name "*.mp3" \) 2>/dev/null | wc -l | tr -d ' ')
echo "Found ${AUDIO_COUNT} audio files"
echo

if [ "$AUDIO_COUNT" -lt 5 ]; then
    echo "⚠️  WARNING: Only ${AUDIO_COUNT} files found."
    echo "   For meaningful comparison, download more audio data."
    echo
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Create output directory
mkdir -p "${OUTDIR}"

echo "======================================"
echo "Starting batch comparison..."
echo "======================================"
echo

# Run comparison
python scripts/compare_systems.py \
    --audio data/wav \
    --mode hinted \
    --langs mn hu fr es \
    --whisper-model "${WHISPER_MODEL}" \
    --device "${DEVICE}" \
    --out-csv "${OUTDIR}/system_comparison.csv"

echo
echo "======================================"
echo "✅ Comparison Complete!"
echo "======================================"
echo
echo "Results saved to:"
echo "  ${OUTDIR}/system_comparison.csv"
echo
echo "Next steps:"
echo "  1. Review results: cat ${OUTDIR}/system_comparison.csv"
echo "  2. Generate plots: python scripts/plot_comparison.py --csv ${OUTDIR}/system_comparison.csv"
echo "  3. Document findings: update docs/thesis_materials/05_results_comparison.md"
echo "  4. Commit: ./scripts/document_milestone.sh \"Completed system comparison\""
echo
