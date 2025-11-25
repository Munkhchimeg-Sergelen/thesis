#!/bin/bash
# Prepare Hungarian audio - first 1000 files

set -e

CV_DIR="$HOME/Downloads/cv-corpus-23.0-2025-09-05"
OUTPUT_DIR="$HOME/thesis-asr/data/wav/hu"
NUM_FILES=1000

echo "======================================"
echo "Preparing Hungarian Audio"
echo "======================================"

mkdir -p "$OUTPUT_DIR"

HU_CLIPS="$CV_DIR/hu/clips"
if [ ! -d "$HU_CLIPS" ]; then
    echo "Error: Hungarian clips not found: $HU_CLIPS"
    exit 1
fi

count=1
for file in "$HU_CLIPS"/*.mp3; do
    if [ $count -gt $NUM_FILES ]; then
        break
    fi
    
    outfile=$(printf "$OUTPUT_DIR/hu%04d.mp3" $count)
    cp "$file" "$outfile"
    
    if [ $((count % 100)) -eq 0 ]; then
        echo "  Copied $count / $NUM_FILES files..."
    fi
    
    ((count++))
done

echo "✓ Completed: $(($count - 1)) Hungarian files"
echo "Total: $(ls $OUTPUT_DIR/*.mp3 | wc -l) files"
