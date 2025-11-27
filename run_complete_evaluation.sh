#!/bin/bash
# Master script to run complete ASR evaluation
# Executes all experiments and analyses in correct order

set -e

echo "============================================================"
echo "COMPLETE ASR EVALUATION - Master Script"
echo "============================================================"
echo "This will run all experiments and analyses"
echo "Estimated time: 15-20 hours total"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Activate environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate omni

cd ~/thesis-asr

# Step 1: Verify data prepared
echo ""
echo "============================================================"
echo "STEP 1: Verifying Dataset"
echo "============================================================"

if [ ! -d "data/wav/es" ] || [ ! -d "data/ref/es" ]; then
    echo "❌ Dataset not prepared!"
    echo "Run: python scripts/prepare_v23_dataset.py first"
    exit 1
fi

file_count=$(find data/wav -name "*.mp3" | wc -l)
echo "✓ Found $file_count audio files"

if [ $file_count -ne 4000 ]; then
    echo "⚠️  Expected 4000 files, found $file_count"
fi

# Step 2: Run all ASR experiments
echo ""
echo "============================================================"
echo "STEP 2: Running ASR Experiments"
echo "============================================================"
echo "This will take 12-17 hours..."

if [ -d "results" ]; then
    echo "Backing up existing results..."
    mv results results_backup_$(date +%Y%m%d_%H%M%S)
fi

bash scripts/run_all_models_v23.sh

# Wait for completion
echo "Waiting for experiments to complete..."
echo "You can monitor progress with: tail -f run_all_v23.log"
# (In practice, this would be run with nohup and checked later)

# Step 3: Calculate WER/CER
echo ""
echo "============================================================"
echo "STEP 3: Calculating WER/CER"
echo "============================================================"

python scripts/calculate_wer_cer.py

echo "✓ WER/CER calculation complete"

# Step 4: Duration analysis
echo ""
echo "============================================================"
echo "STEP 4: Analyzing Audio Durations"
echo "============================================================"

python scripts/analyze_audio_durations.py \
  --audio-dir data/wav \
  --results-dir results \
  --output results/duration_analysis.csv

echo "✓ Duration analysis complete"

# Step 5: LID testing
echo ""
echo "============================================================"
echo "STEP 5: Testing LID Accuracy"
echo "============================================================"
echo "This will take ~2 hours..."

bash scripts/test_lid_accuracy.sh

python scripts/analyze_lid_results.py \
  --results-dir results_lid_test \
  --output results/lid_accuracy.csv

echo "✓ LID testing complete"

# Step 6: Resource profiling
echo ""
echo "============================================================"
echo "STEP 6: Profiling Resource Usage"
echo "============================================================"
echo "This will take ~30 minutes..."

python scripts/profile_resource_usage.py \
  --samples-per-lang 10 \
  --output results/resource_profiling.csv

echo "✓ Resource profiling complete"

# Step 7: Generate plots
echo ""
echo "============================================================"
echo "STEP 7: Generating Plots"
echo "============================================================"

python scripts/plot_wer_speed_analysis.py

echo "✓ Plot generation complete"

# Step 8: Validation
echo ""
echo "============================================================"
echo "STEP 8: Validating Results"
echo "============================================================"

echo "Checking file counts..."
transcript_count=$(find results/transcripts -name "*.txt" | wc -l)
json_count=$(find results/transcripts -name "*.json" | wc -l)

echo "  Transcripts (.txt): $transcript_count (expected: 16000)"
echo "  Metadata (.json): $json_count (expected: 12000)"

if [ -f "results/wer_cer_results_summary.csv" ]; then
    echo "✓ WER/CER results found"
else
    echo "❌ WER/CER results missing"
fi

if [ -f "results/duration_analysis.csv" ]; then
    echo "✓ Duration analysis found"
else
    echo "❌ Duration analysis missing"
fi

if [ -f "results/lid_accuracy.csv" ]; then
    echo "✓ LID accuracy results found"
else
    echo "❌ LID accuracy missing"
fi

if [ -f "results/resource_profiling.csv" ]; then
    echo "✓ Resource profiling found"
else
    echo "❌ Resource profiling missing"
fi

plot_count=$(find results -name "plot*.png" | wc -l)
echo "  Plots generated: $plot_count (expected: 4+)"

# Final summary
echo ""
echo "============================================================"
echo "✅ EVALUATION COMPLETE"
echo "============================================================"
echo ""
echo "Results summary:"
echo "  - Transcriptions: $transcript_count"
echo "  - WER/CER: results/wer_cer_results_summary.csv"
echo "  - Duration analysis: results/duration_analysis.csv"
echo "  - LID accuracy: results/lid_accuracy.csv"
echo "  - Resource usage: results/resource_profiling.csv"
echo "  - Plots: $plot_count files"
echo ""
echo "All results saved in: results/"
echo ""
echo "Next: Review results and download to local machine"
echo "  scp -r -P 15270 mugi@bistromat.tmit.bme.hu:~/thesis-asr/results ./final_results"
echo ""
echo "For detailed analysis, see REPRODUCIBILITY_GUIDE.md"
echo ""
echo "Finished at: $(date)"
