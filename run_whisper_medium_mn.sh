#!/bin/bash
set -e

echo "======================================================================"
echo "🚀 WHISPER-MEDIUM MONGOLIAN EXPERIMENT"
echo "======================================================================"
echo ""
echo "Model: Whisper-medium (769M params)"
echo "Language: Mongolian (mn)"
echo "Mode: Language-hinted"
echo "Device: GPU (cuda)"
echo ""
echo "======================================================================"

DATADIR="data/wav/mn"
DEVICE="cuda"
OUTDIR="results/transcripts/hinted/whisper-medium"
MODEL="medium"

# Count files
total=$(ls -1 ${DATADIR}/*.wav 2>/dev/null | wc -l)
echo "Total files: $total"
echo ""

completed=0

# Run all Mongolian files
for wavfile in ${DATADIR}/*.wav; do
    if [ -f "$wavfile" ]; then
        basename=$(basename "$wavfile")
        completed=$((completed + 1))
        
        echo "[$completed/$total] Processing: $basename"
        
        python scripts/run_whisper.py \
            --model "$MODEL" \
            --mode hinted \
            --infile "$wavfile" \
            --hint-lang mn \
            --device "$DEVICE" \
            --outdir "$OUTDIR"
        
        echo "✅ Completed $basename"
        echo ""
    fi
done

echo ""
echo "======================================================================"
echo "📊 WHISPER-MEDIUM MONGOLIAN COMPLETE!"
echo "======================================================================"
echo "Results: $OUTDIR/mn/"
