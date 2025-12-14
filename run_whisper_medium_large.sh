#!/bin/bash
# Run Whisper medium and large-v3 on all 4 languages

set -e

LANGS="mn hu es fr"
MODELS="medium large-v3"
RESULTS_DIR="results/transcripts"

echo "============================================================"
echo "RUNNING WHISPER MEDIUM & LARGE-V3 ON ALL LANGUAGES"
echo "============================================================"
echo "Languages: $LANGS"
echo "Models: $MODELS"
echo "Output: $RESULTS_DIR"
echo ""
echo "Starting at: $(date)"
echo ""

cd ~/thesis-asr

# Activate conda environment (try different methods)
if [ -f ~/miniconda3/etc/profile.d/conda.sh ]; then
    source ~/miniconda3/etc/profile.d/conda.sh
elif [ -f ~/anaconda3/etc/profile.d/conda.sh ]; then
    source ~/anaconda3/etc/profile.d/conda.sh
fi

# Try to activate omni environment
conda activate omni 2>/dev/null || echo "Using current environment"

# Count total files
total_files=0
for lang in $LANGS; do
    lang_count=$(find data/wav/$lang -name "*.mp3" 2>/dev/null | wc -l)
    total_files=$((total_files + lang_count))
    echo "  $lang: $lang_count files"
done

echo ""
echo "Total files per model: $total_files"
echo "Total transcriptions: $((total_files * 2)) (2 models)"
echo ""

# Track overall start time
overall_start=$(date +%s)

# Run both models
for model in $MODELS; do
    echo ""
    echo "============================================================"
    echo "PHASE: WHISPER-$(echo $model | tr '[:lower:]' '[:upper:]')"
    echo "============================================================"
    start_time=$(date +%s)
    
    for lang in $LANGS; do
        echo ""
        echo "=== Running Whisper-$model on $lang ==="
        
        count=0
        total=0
        
        # Count files for this language
        for audio_file in data/wav/$lang/*.mp3; do
            [ -e "$audio_file" ] || continue
            total=$((total + 1))
        done
        
        echo "Processing $total files..."
        
        # Process all files
        for audio_file in data/wav/$lang/*.mp3; do
            [ -e "$audio_file" ] || continue
            
            python scripts/run_whisper.py \
                --mode hinted \
                --model "$model" \
                --device cuda \
                --infile "$audio_file" \
                --hint-lang "$lang" \
                --outdir "$RESULTS_DIR"
            
            count=$((count + 1))
            
            # Progress updates every 10 files
            if [ $((count % 10)) -eq 0 ]; then
                elapsed=$(($(date +%s) - start_time))
                echo "  [$count/$total] Elapsed: ${elapsed}s"
            fi
        done
        
        echo "✓ Whisper-$model $lang complete ($count files)"
    done
    
    model_elapsed=$(($(date +%s) - start_time))
    echo ""
    echo "✓ Whisper-$model complete for all languages"
    echo "  Time taken: $((model_elapsed / 60)) minutes"
done

echo ""
echo "============================================================"
echo "✅ ALL EXPERIMENTS COMPLETE!"
echo "============================================================"

# Summary
end_time=$(date +%s)
total_elapsed=$((end_time - overall_start))

echo ""
echo "Summary:"
echo "  Models run: medium, large-v3"
echo "  Languages: mn, hu, es, fr"
echo "  Total time: $((total_elapsed / 60)) minutes ($((total_elapsed / 3600)) hours)"
echo ""

# Count results
for model in $MODELS; do
    for lang in $LANGS; do
        txt_count=$(find $RESULTS_DIR/hinted/$model/$lang -name "*.txt" 2>/dev/null | wc -l)
        echo "  $model/$lang: $txt_count transcripts"
    done
done

echo ""
echo "Results saved to: $RESULTS_DIR/hinted/{medium,large-v3}/{mn,hu,es,fr}/"
echo ""
echo "Finished at: $(date)"
