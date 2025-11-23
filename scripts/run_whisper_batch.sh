#!/bin/bash
# Batch run Whisper on file list
# Usage: ./run_whisper_batch.sh <file_list>

set -e

FILE_LIST="${1:-whisper_rerun_files.txt}"

echo "Starting Whisper batch processing..."
echo "File list: $FILE_LIST"
echo "Total files: $(wc -l < "$FILE_LIST")"
echo ""

count=0
while IFS= read -r audio_file; do
    # Extract language from path (data/wav/LANG/file.mp3)
    lang=$(echo "$audio_file" | sed -E 's|.*/([a-z]{2})/[^/]+$|\1|')
    
    # Process
    python scripts/run_whisper.py \
        --mode hinted \
        --model small \
        --device cpu \
        --infile "$audio_file" \
        --outdir results/transcripts \
        --hint-lang "$lang"
    
    count=$((count + 1))
    if [ $((count % 50)) -eq 0 ]; then
        echo "Processed $count files..."
    fi
done < "$FILE_LIST"

echo ""
echo "✅ Completed $count files"
