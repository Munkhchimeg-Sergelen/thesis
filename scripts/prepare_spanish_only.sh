#!/bin/bash
# Prepare Spanish audio only

set -e

CV_DIR="$HOME/Downloads/cv-corpus-23.0-2025-09-05"
OUTPUT_DIR="$HOME/thesis-asr/data/wav/es"
NUM_FILES=1000

echo "======================================"
echo "Preparing Spanish Audio"
echo "======================================"
echo ""

mkdir -p "$OUTPUT_DIR"

ES_CLIPS="$CV_DIR/es/clips"
if [ ! -d "$ES_CLIPS" ]; then
    echo "Error: Spanish clips not found: $ES_CLIPS"
    exit 1
fi

count=1
for file in "$ES_CLIPS"/*.mp3; do
    if [ $count -gt $NUM_FILES ]; then
        break
    fi
    
    outfile=$(printf "$OUTPUT_DIR/es%04d.mp3" $count)
    cp "$file" "$outfile"
    
    if [ $((count % 100)) -eq 0 ]; then
        echo "  Copied $count / $NUM_FILES files..."
    fi
    
    ((count++))
done

echo "✓ Completed: $(($count - 1)) Spanish files"
echo ""

ES_COUNT=$(ls "$OUTPUT_DIR"/*.mp3 2>/dev/null | wc -l | tr -d ' ')
echo "Spanish files: $ES_COUNT / $NUM_FILES"

if [ "$ES_COUNT" -eq "$NUM_FILES" ]; then
    echo "✅ Spanish files prepared successfully!"
else
    echo "⚠️ Warning: File count mismatch!"
fi
