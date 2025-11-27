#!/bin/bash
# Run Wav2Vec2 on Hungarian audio files
echo "Processing Hungarian with Wav2Vec2..."
count=0
for file in data/wav/hu/*.mp3; do
    python scripts/run_wav2vec2.py \
        --infile "$file" \
        --hint-lang hu \
        --device cpu \
        --save-json \
        --outdir results/transcripts/hinted/wav2vec2
    
    count=$((count + 1))
    if [ $((count % 100)) -eq 0 ]; then
        echo "Processed $count files..."
    fi
done
echo "✅ Completed $count files"
