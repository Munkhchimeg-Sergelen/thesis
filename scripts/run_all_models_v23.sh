#!/bin/bash
# Run all ASR models on v23.0 dataset
# This will take ~10-12 hours total

set -e

LANGS="mn hu es fr"
RESULTS_DIR="results_v23"

echo "============================================================"
echo "RUNNING ALL MODELS ON V23.0 DATASET"
echo "============================================================"
echo "Languages: $LANGS"
echo "Output: $RESULTS_DIR"
echo ""

# Activate environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate omni

cd ~/thesis-asr

# Create results directory
mkdir -p $RESULTS_DIR

echo ""
echo "============================================================"
echo "PHASE 1: WHISPER-SMALL (4 languages × ~45 min = 3 hours)"
echo "============================================================"

for lang in $LANGS; do
    echo ""
    echo "=== Running Whisper on $lang ==="
    mkdir -p $RESULTS_DIR/transcripts
    
    count=0
    for audio_file in data/wav/$lang/*.mp3; do
        [ -e "$audio_file" ] || continue
        python scripts/run_whisper.py \
            --mode hinted \
            --model small \
            --device cpu \
            --infile "$audio_file" \
            --hint-lang $lang \
            --outdir $RESULTS_DIR/transcripts
        count=$((count + 1))
        if [ $((count % 100)) -eq 0 ]; then
            echo "  Processed $count files..."
        fi
    done
    echo "✓ Whisper $lang complete ($count files)"
done

echo ""
echo "============================================================"
echo "PHASE 2: OMNILINGUAL CTC 300M (4 languages × ~5 min = 20 min)"
echo "============================================================"

for lang in $LANGS; do
    echo ""
    echo "=== Running OmniASR CTC 300M on $lang ==="
    mkdir -p $RESULTS_DIR/transcripts/hinted/omnilingual/omniASR_CTC_300M/$lang
    
    count=0
    for audio_file in data/wav/$lang/*.mp3; do
        [ -e "$audio_file" ] || continue
        python scripts/run_omnilingual.py \
            --infile "$audio_file" \
            --hint-lang $lang \
            --model omniASR_CTC_300M \
            --save-json \
            --outdir $RESULTS_DIR/transcripts/hinted/omnilingual/omniASR_CTC_300M/$lang
        count=$((count + 1))
        if [ $((count % 100)) -eq 0 ]; then
            echo "  Processed $count files..."
        fi
    done
    echo "✓ OmniASR CTC 300M $lang complete ($count files)"
done

echo ""
echo "============================================================"
echo "PHASE 3: OMNILINGUAL CTC 1B (4 languages × ~10 min = 40 min)"
echo "============================================================"

for lang in $LANGS; do
    echo ""
    echo "=== Running OmniASR CTC 1B on $lang ==="
    mkdir -p $RESULTS_DIR/transcripts/hinted/omnilingual/omniASR_CTC_1B/$lang
    
    count=0
    for audio_file in data/wav/$lang/*.mp3; do
        [ -e "$audio_file" ] || continue
        python scripts/run_omnilingual.py \
            --infile "$audio_file" \
            --hint-lang $lang \
            --model omniASR_CTC_1B \
            --save-json \
            --outdir $RESULTS_DIR/transcripts/hinted/omnilingual/omniASR_CTC_1B/$lang
        count=$((count + 1))
        if [ $((count % 100)) -eq 0 ]; then
            echo "  Processed $count files..."
        fi
    done
    echo "✓ OmniASR CTC 1B $lang complete ($count files)"
done

echo ""
echo "============================================================"
echo "PHASE 4: OMNILINGUAL LLM 1B (4 languages × ~30 min = 2 hours)"
echo "============================================================"

for lang in $LANGS; do
    echo ""
    echo "=== Running OmniASR LLM 1B on $lang ==="
    mkdir -p $RESULTS_DIR/transcripts/hinted/omnilingual/omniASR_LLM_1B/$lang
    
    count=0
    for audio_file in data/wav/$lang/*.mp3; do
        [ -e "$audio_file" ] || continue
        python scripts/run_omnilingual.py \
            --infile "$audio_file" \
            --hint-lang $lang \
            --model omniASR_LLM_1B \
            --save-json \
            --outdir $RESULTS_DIR/transcripts/hinted/omnilingual/omniASR_LLM_1B/$lang
        count=$((count + 1))
        if [ $((count % 100)) -eq 0 ]; then
            echo "  Processed $count files..."
        fi
    done
    echo "✓ OmniASR LLM 1B $lang complete ($count files)"
done

echo ""
echo "============================================================"
echo "✅ ALL MODELS COMPLETE!"
echo "============================================================"
echo "Total transcriptions: 16,000 (4 models × 4 languages × 1000 files)"
echo "Results saved to: $RESULTS_DIR/"
echo ""
echo "Next steps:"
echo "1. Move results: mv $RESULTS_DIR results"
echo "2. Update WER/CER script to use results/ directory"
echo "3. Calculate WER/CER: python scripts/calculate_wer_cer.py"
echo "4. Generate plots: python scripts/plot_wer_speed_analysis.py"
echo ""
echo "Finished at: $(date)"
