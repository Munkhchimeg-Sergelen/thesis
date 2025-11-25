#!/bin/bash
# Prepare Mongolian audio - first 1000 files

set -e

CV_DIR="$HOME/Downloads/cv-corpus-23.0-2025-09-05"
OUTPUT_DIR="$HOME/thesis-asr/data/wav/mn"
NUM_FILES=1000

echo "======================================"
echo "Preparing Mongolian Audio"
echo "======================================"

mkdir -p "$OUTPUT_DIR"

MN_CLIPS="$CV_DIR/mn/clips"
if [ ! -d "$MN_CLIPS" ]; then
    echo "Error: Mongolian clips not found: $MN_CLIPS"
    exit 1
fi

count=1
for file in "$MN_CLIPS"/*.mp3; do
    if [ $count -gt $NUM_FILES ]; then
        break
    fi
    
    outfile=$(printf "$OUTPUT_DIR/mn%04d.mp3" $count)
    cp "$file" "$outfile"
    
    if [ $((count % 100)) -eq 0 ]; then
        echo "  Copied $count / $NUM_FILES files..."
    fi
    
    ((count++))
done

echo "✓ Completed: $(($count - 1)) Mongolian files"
echo "Total: $(ls $OUTPUT_DIR/*.mp3 | wc -l) files"
