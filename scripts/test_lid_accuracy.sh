#!/bin/bash
# Test Language Identification (LID) accuracy
# Run models without language hints to test auto-detection

set -e

LANGS="mn hu es fr"
NUM_SAMPLES=100  # Test on 100 samples per language
RESULTS_DIR="results_lid_test"

echo "============================================================"
echo "LANGUAGE IDENTIFICATION (LID) ACCURACY TEST"
echo "============================================================"
echo "Testing $NUM_SAMPLES samples per language"
echo "Models: Whisper-small (supports LID)"
echo ""

# Activate environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate omni

cd ~/thesis-asr
mkdir -p $RESULTS_DIR

# Test Whisper LID
echo ""
echo "============================================================"
echo "TESTING WHISPER LID (lid2asr mode)"
echo "============================================================"

for lang in $LANGS; do
    echo ""
    echo "=== Testing LID for $lang ==="
    mkdir -p $RESULTS_DIR/whisper-small/$lang
    
    # Get first NUM_SAMPLES files
    count=0
    for audio_file in data/wav/$lang/*.mp3; do
        [ -e "$audio_file" ] || continue
        
        # Run without language hint (LID mode)
        python scripts/run_whisper.py \
            --mode lid2asr \
            --model small \
            --device cpu \
            --infile "$audio_file" \
            --outdir $RESULTS_DIR/whisper-small/$lang
        
        count=$((count + 1))
        if [ $count -ge $NUM_SAMPLES ]; then
            break
        fi
    done
    
    echo "✓ Tested $count files for $lang"
done

echo ""
echo "============================================================"
echo "✅ LID TESTING COMPLETE"
echo "============================================================"
echo ""
echo "Next: Run python scripts/analyze_lid_accuracy.py"
