#!/bin/bash
# Quick test of greedy vs beam search on GPU
# Tests 5 files per language

echo "======================================"
echo "Greedy vs Beam Search Test"
echo "Testing 5 files per language"
echo "======================================"

# Test files
MN_FILES=(data/wav/mn/mn0001.mp3 data/wav/mn/mn0010.mp3 data/wav/mn/mn0020.mp3 data/wav/mn/mn0030.mp3 data/wav/mn/mn0040.mp3)
HU_FILES=(data/wav/hu/hu0001.mp3 data/wav/hu/hu0010.mp3 data/wav/hu/hu0020.mp3 data/wav/hu/hu0030.mp3 data/wav/hu/hu0040.mp3)
ES_FILES=(data/wav/es/es0001.mp3 data/wav/es/es0010.mp3 data/wav/es/es0020.mp3 data/wav/es/es0030.mp3 data/wav/es/es0040.mp3)
FR_FILES=(data/wav/fr/fr0001.mp3 data/wav/fr/fr0010.mp3 data/wav/fr/fr0020.mp3 data/wav/fr/fr0030.mp3 data/wav/fr/fr0040.mp3)

OUTPUT_FILE="beam_test_results.txt"
rm -f "$OUTPUT_FILE"

echo "Results:" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Function to test a language
test_language() {
    local lang=$1
    shift
    local files=("$@")
    
    echo "" >> "$OUTPUT_FILE"
    echo "======================================" >> "$OUTPUT_FILE"
    echo "$lang:" >> "$OUTPUT_FILE"
    echo "======================================" >> "$OUTPUT_FILE"
    
    for beam in 1 5; do
        echo "" >> "$OUTPUT_FILE"
        echo "Beam size: $beam ($([ $beam -eq 1 ] && echo 'GREEDY' || echo 'BEAM SEARCH'))" >> "$OUTPUT_FILE"
        echo "---" >> "$OUTPUT_FILE"
        
        total_time=0
        count=0
        
        for file in "${files[@]}"; do
            if [ ! -f "$file" ]; then
                echo "  $file: NOT FOUND" >> "$OUTPUT_FILE"
                continue
            fi
            
            start=$(date +%s.%N)
            
            python scripts/run_whisper_beam.py \
                --model small \
                --mode hinted \
                --infile "$file" \
                --hint-lang "$lang" \
                --device cpu \
                --beam-size "$beam" \
                --outdir results/test_beam > /dev/null 2>&1
            
            end=$(date +%s.%N)
            elapsed=$(echo "$end - $start" | bc)
            
            total_time=$(echo "$total_time + $elapsed" | bc)
            count=$((count + 1))
            
            echo "  $(basename $file): ${elapsed}s" >> "$OUTPUT_FILE"
        done
        
        if [ $count -gt 0 ]; then
            avg=$(echo "scale=3; $total_time / $count" | bc)
            echo "  Average: ${avg}s" >> "$OUTPUT_FILE"
        fi
    done
}

# Test each language
echo "Testing Mongolian..."
test_language "mn" "${MN_FILES[@]}"

echo "Testing Hungarian..."
test_language "hu" "${HU_FILES[@]}"

echo "Testing Spanish..."
test_language "es" "${ES_FILES[@]}"

echo "Testing French..."
test_language "fr" "${FR_FILES[@]}"

echo ""
echo "======================================"
echo "✅ Test complete!"
echo "Results saved to: $OUTPUT_FILE"
echo "======================================"
cat "$OUTPUT_FILE"
