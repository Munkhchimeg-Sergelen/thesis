#!/bin/bash
#
# MASTER EVALUATION SCRIPT
# Runs complete ASR evaluation with both systems on all languages
#
# Usage: ./scripts/run_full_evaluation.sh
# Run this AFTER you transfer real audio files tonight!
#

set -e  # Exit on error

echo "======================================================================"
echo "🎯 FULL ASR EVALUATION - Both Systems, All Languages"
echo "======================================================================"
echo ""
echo "Systems: Whisper (tiny/base/small) + Wav2Vec2 (ES/FR only)"
echo "Languages: ES, FR, HU, MN"
echo "Mode: Language-hinted (oracle)"
echo "Device: GPU (CUDA)"
echo ""
echo "======================================================================"
echo ""

# Activate conda environment
source ~/miniforge/bin/activate asr-env

# Change to project directory
cd ~/thesis-asr

# Counter for experiments
TOTAL_EXPERIMENTS=0
COMPLETED=0

# Function to run and count experiments
run_experiment() {
    TOTAL_EXPERIMENTS=$((TOTAL_EXPERIMENTS + 1))
    echo ""
    echo "[$TOTAL_EXPERIMENTS] $1"
    echo "----------------------------------------------------------------------"
    
    if eval "$2"; then
        COMPLETED=$((COMPLETED + 1))
        echo "✅ Completed [$COMPLETED/$TOTAL_EXPERIMENTS]"
    else
        echo "❌ Failed!"
        return 1
    fi
}

# ==============================================================================
# PART 1: WHISPER EVALUATION (All 4 languages, 3 model sizes)
# ==============================================================================

echo ""
echo "======================================================================"
echo "PART 1: Whisper Evaluation (Multilingual Approach)"
echo "======================================================================"

WHISPER_MODELS=(tiny base small)
WHISPER_LANGS=(es fr hu mn)

for model in "${WHISPER_MODELS[@]}"; do
    for lang in "${WHISPER_LANGS[@]}"; do
        # Find all WAV files for this language
        for wavfile in data/wav/${lang}/*.wav; do
            # Skip if no files found (glob didn't expand)
            [ -e "$wavfile" ] || continue
            
            BASENAME=$(basename "$wavfile")
            DESC="Whisper-${model} ${lang^^} ${BASENAME}"
            CMD="python scripts/run_whisper.py \
                --mode hinted \
                --model ${model} \
                --device cuda \
                --infile \"${wavfile}\" \
                --hint-lang ${lang}"
            
            run_experiment "$DESC" "$CMD" || true
        done
    done
done

# ==============================================================================
# PART 2: WAV2VEC2 EVALUATION (ES and FR only)
# ==============================================================================

echo ""
echo "======================================================================"
echo "PART 2: Wav2Vec2 Evaluation (Language-Specific Approach)"
echo "======================================================================"

WAV2VEC2_LANGS=(es fr)

for lang in "${WAV2VEC2_LANGS[@]}"; do
    # Find all WAV files for this language
    for wavfile in data/wav/${lang}/*.wav; do
        # Skip if no files found
        [ -e "$wavfile" ] || continue
        
        BASENAME=$(basename "$wavfile")
        DESC="Wav2Vec2-XLSR-53-${lang^^} ${BASENAME}"
        CMD="python scripts/run_wav2vec2.py \
            --infile \"${wavfile}\" \
            --hint-lang ${lang} \
            --device cuda"
        
        run_experiment "$DESC" "$CMD" || true
    done
done

# ==============================================================================
# SUMMARY
# ==============================================================================

echo ""
echo "======================================================================"
echo "📊 EVALUATION COMPLETE!"
echo "======================================================================"
echo ""
echo "Total experiments: $TOTAL_EXPERIMENTS"
echo "Completed: $COMPLETED"
echo "Failed: $((TOTAL_EXPERIMENTS - COMPLETED))"
echo ""
echo "Results saved to:"
echo "  - Whisper: results/transcripts/hinted/whisper/{lang}/"
echo "  - Wav2Vec2: results/transcripts/hinted/wav2vec2/{lang}/"
echo ""
echo "Next steps:"
echo "  1. Analyze results: python scripts/analyze_results.py"
echo "  2. Create plots: python scripts/create_plots.py"
echo "  3. Commit to GitHub: git add results/ && git commit -m 'Full evaluation results'"
echo ""
echo "======================================================================"
