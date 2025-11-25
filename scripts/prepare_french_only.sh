#!/bin/bash
# Prepare French audio files only

set -e

# Configuration
CV_DIR="$HOME/Downloads/cv-corpus-23.0-2025-09-05/fr"
OUTPUT_DIR="$HOME/thesis-asr/data/wav/fr"
NUM_FILES=1000

echo "======================================"
echo "Preparing French Audio Files"
echo "======================================"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Process French
echo "Processing French files..."
FR_CLIPS="$CV_DIR/clips"

if [ ! -d "$FR_CLIPS" ]; then
    echo "Error: French clips directory not found: $FR_CLIPS"
    exit 1
fi

count=1
for file in "$FR_CLIPS"/*.mp3; do
    if [ $count -gt $NUM_FILES ]; then
        break
    fi
    
    # Copy and rename
    outfile=$(printf "$OUTPUT_DIR/fr%04d.mp3" $count)
    cp "$file" "$outfile"
    
    if [ $((count % 100)) -eq 0 ]; then
        echo "  Copied $count / $NUM_FILES French files..."
    fi
    
    ((count++))
done

echo "✓ Completed: $(($count - 1)) French files"
echo ""

# Verify count
echo "======================================"
echo "Verification:"
echo "======================================"
FR_COUNT=$(ls "$OUTPUT_DIR"/*.mp3 2>/dev/null | wc -l | tr -d ' ')
echo "French files: $FR_COUNT / $NUM_FILES"
echo ""

if [ "$FR_COUNT" -eq "$NUM_FILES" ]; then
    echo "✅ French files prepared successfully!"
else
    echo "⚠️  Warning: French file count mismatch!"
fi
