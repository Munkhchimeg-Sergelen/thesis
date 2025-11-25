#!/bin/bash
# Batch process French audio with Wav2Vec2

set -e

echo "======================================"
echo "Wav2Vec2 French Processing"
echo "======================================"
echo ""

# Count files
TOTAL=$(ls data/wav/fr/*.mp3 | wc -l | tr -d ' ')
echo "Total files to process: $TOTAL"
echo ""

count=0
for file in data/wav/fr/*.mp3; do
    python scripts/run_wav2vec2.py \
        --infile "$file" \
        --hint-lang fr \
        --device cpu \
        --save-json \
        --outdir results/transcripts/hinted/wav2vec2
    
    count=$((count + 1))
    
    if [ $((count % 50)) -eq 0 ]; then
        echo "Processed $count / $TOTAL files..."
    fi
done

echo ""
echo "======================================"
echo "✅ Completed $count French files"
echo "======================================"
