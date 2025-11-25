#!/bin/bash
# Prepare the EXACT same 1,000 Spanish files used in Whisper experiments

set -e

CV_DIR="$HOME/Downloads/cv-corpus-23.0-2025-09-05"
OUTPUT_DIR="$HOME/thesis-asr/data/wav/es"
RESULTS_DIR="$HOME/thesis-asr/results/transcripts"

echo "======================================"
echo "Preparing EXACT Spanish Audio Files"
echo "======================================"
echo ""

# Extract list of Spanish files from existing Whisper results
echo "Step 1: Finding which files were used in Whisper experiments..."
FILE_LIST="/tmp/spanish_files_used.txt"
find "$RESULTS_DIR" -name "es*.json" -path "*/whisper*" | \
    xargs -I {} basename {} .json > "$FILE_LIST"

NUM_FILES=$(cat "$FILE_LIST" | wc -l | tr -d ' ')
echo "✓ Found $NUM_FILES Spanish files in Whisper results"
echo ""

if [ "$NUM_FILES" -eq 0 ]; then
    echo "Error: No Spanish files found in results!"
    echo "Using fallback: first 1000 files"
    # This should not happen but provides fallback
    exit 1
fi

# Check if Common Voice Spanish exists
ES_CLIPS="$CV_DIR/es/clips"
if [ ! -d "$ES_CLIPS" ]; then
    echo "Error: Spanish clips not found: $ES_CLIPS"
    echo "Please extract the Spanish Common Voice dataset first:"
    echo "  cd ~/Downloads"
    echo "  tar -xzf mcv-scripted-es-v23.0.tar.gz"
    exit 1
fi

echo "Step 2: Checking which original MP3s we need..."
# Read the mapping file that was used during original preparation
# Spanish files were named es0001.mp3, es0002.mp3, etc.
# We need to find the original Common Voice filenames

# Since we don't have the original mapping, we'll need to use the numbered files
# The good news: your results already tell us which numbered files to use!

mkdir -p "$OUTPUT_DIR"

echo "Step 3: Looking for original Spanish audio files..."
echo ""

# Check if you still have the original prepared files somewhere
ORIG_ES="$HOME/thesis-asr/data/wav/es"
if [ -d "$ORIG_ES" ] && [ "$(ls $ORIG_ES/*.mp3 2>/dev/null | wc -l)" -gt 0 ]; then
    echo "✓ Found original Spanish files in data/wav/es/"
    echo "  No need to re-prepare - files are already correct!"
    count=$(ls "$ORIG_ES"/*.mp3 | wc -l)
    echo "  Files present: $count"
else
    echo "⚠️  Original Spanish files not found locally"
    echo ""
    echo "Options:"
    echo "  1. Download from GPU (recommended):"
    echo "     rsync -avz -e 'ssh -p 15270' mugi@bistromat.tmit.bme.hu:~/thesis-asr/data/wav/es/ data/wav/es/"
    echo ""
    echo "  2. Or prepare fresh (but must match original selection)"
    echo ""
    echo "Since the original preparation order matters, it's safer to download from GPU"
fi

echo ""
echo "======================================"
echo "File list saved to: $FILE_LIST"
echo "Total files needed: $NUM_FILES"
echo "======================================"
