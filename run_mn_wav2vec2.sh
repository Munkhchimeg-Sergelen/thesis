#!/bin/bash
# Run Wav2Vec2 on Mongolian audio files
echo "Processing Mongolian with Wav2Vec2..."
count=0
for file in data/wav/mn/*.mp3; do
    python scripts/run_wav2vec2.py \
        --infile "$file" \
        --hint-lang mn \
        --device cpu \
        --save-json \
        --outdir results/transcripts/hinted/wav2vec2
    
    count=$((count + 1))
    if [ $((count % 100)) -eq 0 ]; then
        echo "Processed $count files..."
    fi
done
echo "✅ Completed $count files"
