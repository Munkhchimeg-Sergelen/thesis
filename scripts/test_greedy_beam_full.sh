#!/bin/bash
# Full test of greedy vs beam search on GPU
# Tests ALL 1000 files per language

echo "======================================"
echo "Greedy vs Beam Search - FULL TEST"
echo "Testing 1000 files per language"
echo "======================================"

OUTPUT_DIR="results/beam_comparison"
mkdir -p "$OUTPUT_DIR"

# Function to test a language
test_language() {
    local lang=$1
    local lang_code=$2
    
    echo ""
    echo "======================================"
    echo "Processing $lang ($lang_code)"
    echo "======================================"
    
    for beam in 1 5; do
        mode_name=$([ $beam -eq 1 ] && echo "greedy" || echo "beam")
        echo ""
        echo "Testing with beam_size=$beam ($mode_name)..."
        
        output_file="$OUTPUT_DIR/${lang_code}_beam${beam}.txt"
        rm -f "$output_file"
        
        count=0
        total_time=0
        
        for file in data/wav/$lang_code/*.mp3; do
            if [ ! -f "$file" ]; then
                continue
            fi
            
            start=$(date +%s.%N)
            
            python scripts/run_whisper_beam.py \
                --model small \
                --mode hinted \
                --infile "$file" \
                --hint-lang "$lang_code" \
                --device cpu \
                --beam-size "$beam" \
                --outdir "$OUTPUT_DIR/transcripts_${lang_code}_beam${beam}" \
                > /dev/null 2>&1
            
            end=$(date +%s.%N)
            elapsed=$(echo "$end - $start" | bc)
            
            total_time=$(echo "$total_time + $elapsed" | bc)
            count=$((count + 1))
            
            # Log each file
            echo "$(basename $file),$elapsed" >> "$output_file"
            
            # Progress updates
            if [ $((count % 100)) -eq 0 ]; then
                avg=$(echo "scale=3; $total_time / $count" | bc)
                echo "  Processed $count / 1000 files... (avg: ${avg}s per file)"
            fi
        done
        
        # Final statistics
        if [ $count -gt 0 ]; then
            avg=$(echo "scale=3; $total_time / $count" | bc)
            echo "✓ Completed $count files"
            echo "  Total time: ${total_time}s"
            echo "  Average: ${avg}s per file"
            echo "SUMMARY,$count,$total_time,$avg" >> "$output_file"
        fi
    done
}

# Test each language
echo ""
echo "Starting full test..."
echo "Estimated time: 8-12 hours"
echo ""

test_language "Mongolian" "mn"
test_language "Hungarian" "hu"
test_language "Spanish" "es"
test_language "French" "fr"

echo ""
echo "======================================"
echo "✅ Full test complete!"
echo "======================================"
echo ""
echo "Results saved in: $OUTPUT_DIR/"
echo ""
echo "Summary:"
for file in "$OUTPUT_DIR"/*.txt; do
    if [ -f "$file" ]; then
        summary=$(grep "^SUMMARY" "$file")
        if [ -n "$summary" ]; then
            echo "  $(basename $file): $summary"
        fi
    fi
done
