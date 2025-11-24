#!/bin/bash
# Prepare Common Voice audio files for ES+FR experiments
# Takes first 1000 files and renames to our naming convention

set -e

# Configuration
CV_DIR="$HOME/Downloads"
OUTPUT_DIR="$HOME/thesis-asr/data/wav"
NUM_FILES=1000

echo "======================================"
echo "Preparing ES+FR Audio Files"
echo "======================================"
echo ""

# Create output directories
mkdir -p "$OUTPUT_DIR/es"
mkdir -p "$OUTPUT_DIR/fr"

# Process Spanish
echo "Processing Spanish files..."
ES_DIR="$CV_DIR/cv-corpus-23.0-2025-09-05/es"
if [ ! -d "$ES_DIR" ]; then
    echo "Error: Spanish directory not found: $ES_DIR"
    echo "Please extract mcv-scripted-es-v23.0.tar.gz first"
    exit 1
fi

ES_CLIPS="$ES_DIR/clips"
if [ ! -d "$ES_CLIPS" ]; then
    echo "Error: Spanish clips directory not found: $ES_CLIPS"
    exit 1
fi

count=1
for file in "$ES_CLIPS"/*.mp3; do
    if [ $count -gt $NUM_FILES ]; then
        break
    fi
    
    # Copy and rename
    outfile=$(printf "$OUTPUT_DIR/es/es%04d.mp3" $count)
    cp "$file" "$outfile"
    
    if [ $((count % 100)) -eq 0 ]; then
        echo "  Copied $count / $NUM_FILES Spanish files..."
    fi
    
    ((count++))
done
echo "✓ Completed: $(($count - 1)) Spanish files"
echo ""

# Process French (if available)
echo "Processing French files..."
FR_DIR="$CV_DIR/cv-corpus-23.0-2025-09-05/fr"
if [ ! -d "$FR_DIR" ]; then
    echo "⚠️  French directory not found - skipping for now"
    echo "Download and extract mcv-scripted-fr-v23.0.tar.gz, then run again"
else
    FR_CLIPS="$FR_DIR/clips"
    if [ ! -d "$FR_CLIPS" ]; then
        echo "Error: French clips directory not found: $FR_CLIPS"
    else
        count=1
        for file in "$FR_CLIPS"/*.mp3; do
            if [ $count -gt $NUM_FILES ]; then
                break
            fi
            
            # Copy and rename
            outfile=$(printf "$OUTPUT_DIR/fr/fr%04d.mp3" $count)
            cp "$file" "$outfile"
            
            if [ $((count % 100)) -eq 0 ]; then
                echo "  Copied $count / $NUM_FILES French files..."
            fi
            
            ((count++))
        done
        echo "✓ Completed: $(($count - 1)) French files"
    fi
fi
echo ""

# Verify counts
echo "======================================"
echo "Verification:"
echo "======================================"
ES_COUNT=$(ls "$OUTPUT_DIR/es"/*.mp3 2>/dev/null | wc -l | tr -d ' ')
FR_COUNT=$(ls "$OUTPUT_DIR/fr"/*.mp3 2>/dev/null | wc -l | tr -d ' ')
echo "Spanish files: $ES_COUNT / $NUM_FILES"
echo "French files: $FR_COUNT / $NUM_FILES"
echo ""

if [ "$ES_COUNT" -eq "$NUM_FILES" ]; then
    echo "✅ Spanish files prepared successfully!"
else
    echo "⚠️  Warning: Spanish file count mismatch!"
fi

if [ "$FR_COUNT" -eq "$NUM_FILES" ]; then
    echo "✅ French files prepared successfully!"
elif [ "$FR_COUNT" -eq 0 ]; then
    echo "ℹ️  French not processed yet - download and run again"
else
    echo "⚠️  Warning: French file count mismatch!"
fi
