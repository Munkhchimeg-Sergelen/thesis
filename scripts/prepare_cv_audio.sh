#!/bin/bash
# Prepare Common Voice audio files for ASR experiments
# Takes first 1000 files and renames to our naming convention

set -e

# Configuration
CV_DIR="$HOME/Downloads/cv-corpus-23.0-2025-09-05"
OUTPUT_DIR="$HOME/thesis-asr/data/wav"
NUM_FILES=1000

echo "======================================"
echo "Preparing Common Voice Audio Files"
echo "======================================"
echo ""

# Create output directories
mkdir -p "$OUTPUT_DIR/hu"
mkdir -p "$OUTPUT_DIR/mn"

# Process Hungarian
echo "Processing Hungarian files..."
HU_CLIPS="$CV_DIR/hu/clips"
if [ ! -d "$HU_CLIPS" ]; then
    echo "Error: Hungarian clips directory not found: $HU_CLIPS"
    exit 1
fi

count=1
for file in "$HU_CLIPS"/*.mp3; do
    if [ $count -gt $NUM_FILES ]; then
        break
    fi
    
    # Copy and rename
    outfile=$(printf "$OUTPUT_DIR/hu/hu%04d.mp3" $count)
    cp "$file" "$outfile"
    
    if [ $((count % 100)) -eq 0 ]; then
        echo "  Copied $count / $NUM_FILES Hungarian files..."
    fi
    
    ((count++))
done
echo "✓ Completed: $(($count - 1)) Hungarian files"
echo ""

# Process Mongolian
echo "Processing Mongolian files..."
MN_CLIPS="$CV_DIR/mn/clips"
if [ ! -d "$MN_CLIPS" ]; then
    echo "Error: Mongolian clips directory not found: $MN_CLIPS"
    exit 1
fi

count=1
for file in "$MN_CLIPS"/*.mp3; do
    if [ $count -gt $NUM_FILES ]; then
        break
    fi
    
    # Copy and rename
    outfile=$(printf "$OUTPUT_DIR/mn/mn%04d.mp3" $count)
    cp "$file" "$outfile"
    
    if [ $((count % 100)) -eq 0 ]; then
        echo "  Copied $count / $NUM_FILES Mongolian files..."
    fi
    
    ((count++))
done
echo "✓ Completed: $(($count - 1)) Mongolian files"
echo ""

# Verify counts
echo "======================================"
echo "Verification:"
echo "======================================"
HU_COUNT=$(ls "$OUTPUT_DIR/hu"/*.mp3 2>/dev/null | wc -l | tr -d ' ')
MN_COUNT=$(ls "$OUTPUT_DIR/mn"/*.mp3 2>/dev/null | wc -l | tr -d ' ')
echo "Hungarian files: $HU_COUNT / $NUM_FILES"
echo "Mongolian files: $MN_COUNT / $NUM_FILES"
echo ""

if [ "$HU_COUNT" -eq "$NUM_FILES" ] && [ "$MN_COUNT" -eq "$NUM_FILES" ]; then
    echo "✅ All files prepared successfully!"
else
    echo "⚠️  Warning: File count mismatch!"
fi
