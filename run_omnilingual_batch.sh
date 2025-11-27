#!/bin/bash
# Run OmniLingual ASR on all 4 languages with multiple model sizes

echo "======================================"
echo "OmniLingual ASR Batch Processing"
echo "Testing 3 models × 4 languages"
echo "======================================"

# Models to test (as suggested by supervisor)
# CTC: Parallel generation (fast), LLM: Language-conditioned (more accurate)
MODELS=("omniASR_CTC_300M" "omniASR_CTC_1B" "omniASR_LLM_1B")
LANGUAGES=("mn" "hu" "es" "fr")

for MODEL in "${MODELS[@]}"; do
    echo ""
    echo "======================================"
    echo "Processing with $MODEL"
    echo "======================================"
    
    for LANG in "${LANGUAGES[@]}"; do
        echo ""
        echo "--- Language: $LANG ---"
        
        count=0
        for file in data/wav/$LANG/*.mp3; do
            python scripts/run_omnilingual.py \
                --infile "$file" \
                --hint-lang "$LANG" \
                --model "$MODEL" \
                --save-json \
                --outdir results/transcripts/hinted/omnilingual
            
            count=$((count + 1))
            if [ $((count % 100)) -eq 0 ]; then
                echo "  Processed $count files with $MODEL..."
            fi
        done
        
        echo "✅ $LANG completed: $count files with $MODEL"
    done
done

echo ""
echo "======================================"
echo "✅ All Models & Languages Complete!"
echo "======================================"
echo ""
echo "Results:"
for MODEL in "${MODELS[@]}"; do
    echo "  $MODEL:"
    for LANG in "${LANGUAGES[@]}"; do
        count=$(ls results/transcripts/hinted/omnilingual/$MODEL/$LANG/*.json 2>/dev/null | wc -l)
        echo "    $LANG: $count files"
    done
done
