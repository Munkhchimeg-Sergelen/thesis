#!/bin/bash
# Run MMS on all 4 languages in parallel

echo "======================================"
echo "Starting MMS Processing - All Languages"
echo "======================================"

# Function to process a language
process_language() {
    local lang=$1
    local lang_name=$2
    
    echo "Starting $lang_name ($lang)..."
    
    count=0
    for file in data/wav/$lang/*.mp3; do
        python scripts/run_mms.py \
            --infile "$file" \
            --hint-lang "$lang" \
            --device cpu \
            --save-json \
            --outdir results/transcripts/hinted/mms
        
        count=$((count + 1))
        if [ $((count % 100)) -eq 0 ]; then
            echo "  $lang_name: Processed $count files..."
        fi
    done
    
    echo "✅ $lang_name completed: $count files"
}

# Export function for parallel execution
export -f process_language

# Run all 4 languages in parallel
process_language mn "Mongolian" > mn_mms.log 2>&1 &
process_language hu "Hungarian" > hu_mms.log 2>&1 &
process_language es "Spanish" > es_mms.log 2>&1 &
process_language fr "French" > fr_mms.log 2>&1 &

echo ""
echo "All 4 languages started in parallel!"
echo "Monitor progress:"
echo "  tail -f mn_mms.log"
echo "  tail -f hu_mms.log"
echo "  tail -f es_mms.log"
echo "  tail -f fr_mms.log"
echo ""
echo "Check file counts:"
echo "  ls results/transcripts/hinted/mms/*/*.json | wc -l"

# Wait for all to complete
wait

echo ""
echo "======================================"
echo "✅ All Languages Complete!"
echo "======================================"
echo "  MN: $(ls results/transcripts/hinted/mms/mn/*.json 2>/dev/null | wc -l) files"
echo "  HU: $(ls results/transcripts/hinted/mms/hu/*.json 2>/dev/null | wc -l) files"
echo "  ES: $(ls results/transcripts/hinted/mms/es/*.json 2>/dev/null | wc -l) files"
echo "  FR: $(ls results/transcripts/hinted/mms/fr/*.json 2>/dev/null | wc -l) files"
