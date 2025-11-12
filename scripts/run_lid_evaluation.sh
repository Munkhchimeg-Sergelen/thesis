#!/bin/bash
set -e

echo "======================================================================"
echo "🔍 LID→ASR EVALUATION - Automatic Language Detection"
echo "======================================================================"
echo ""
echo "Mode: LID→ASR (language detected from audio)"
echo "Systems: Whisper (tiny/base/small)"
echo "Languages: ES, FR, HU, MN (will be auto-detected)"
echo ""
echo "======================================================================"
echo ""

# Configuration
DATADIR="data/wav"
DEVICE="cpu"
OUTDIR="results/transcripts"

total=0
completed=0

# Count total files
for lang in es fr hu mn; do
    count=$(ls -1 ${DATADIR}/${lang}/*.wav 2>/dev/null | wc -l)
    total=$((total + count * 3))  # 3 models
done

echo "Total experiments: $total"
echo ""

# Function to run a single experiment
run_experiment() {
    local model=$1
    local lang=$2
    local wavfile=$3
    local basename=$(basename "$wavfile")
    
    completed=$((completed + 1))
    echo ""
    echo "[$completed] Whisper-$model LID $basename"
    echo "----------------------------------------------------------------------"
    
    python scripts/run_whisper.py \
        --model "$model" \
        --mode lid2asr \
        --infile "$wavfile" \
        --device "$DEVICE" \
        --outdir "$OUTDIR"
    
    echo "✅ Completed [$completed/$total]"
}

echo ""
echo "======================================================================"
echo "WHISPER LID→ASR EVALUATION"
echo "======================================================================"
echo ""

# Run all experiments
for model in tiny base small; do
    for lang in es fr hu mn; do
        for wavfile in ${DATADIR}/${lang}/*.wav; do
            if [ -f "$wavfile" ]; then
                run_experiment "$model" "$lang" "$wavfile"
            fi
        done
    done
done

echo ""
echo "======================================================================"
echo "📊 LID EVALUATION COMPLETE!"
echo "======================================================================"
echo ""
echo "Total experiments: $total"
echo "Completed: $completed"
echo ""
echo "Results saved to: results/transcripts/lid2asr/"
echo ""
echo "Next steps:"
echo "  1. python scripts/compare_lid_vs_hinted.py"
echo "  2. python scripts/analyze_lid_accuracy.py"
echo ""
echo "======================================================================"
