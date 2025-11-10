#!/bin/bash
# GPU Evaluation Sweep
# Runs both systems (Whisper + Wav2Vec2) on GPU for comparison

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="results/gpu_sweep_${TIMESTAMP}"
DEVICE="cuda"

echo "======================================"
echo "🚀 GPU Evaluation Sweep"
echo "======================================"
echo "Output: ${OUTDIR}"
echo "Timestamp: ${TIMESTAMP}"
echo

# Check CUDA
if ! python -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
    echo "❌ ERROR: CUDA not available"
    echo "   Make sure you're on the GPU server"
    echo "   Run: python -c 'import torch; print(torch.cuda.is_available())'"
    exit 1
fi

echo "✓ CUDA available"
echo

# Check audio files
WAV_COUNT=$(find data/wav -name "*.wav" 2>/dev/null | wc -l | tr -d ' ')
echo "Found ${WAV_COUNT} audio files"

if [ "$WAV_COUNT" -lt 5 ]; then
    echo "⚠️  WARNING: Only ${WAV_COUNT} files."
    echo "   Run on CPU first or download more audio."
    echo
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create output directories
mkdir -p "${OUTDIR}/whisper_tiny"
mkdir -p "${OUTDIR}/whisper_small"
mkdir -p "${OUTDIR}/whisper_base"
mkdir -p "${OUTDIR}/wav2vec2"

echo "======================================"
echo "Phase 1: Whisper on GPU"
echo "======================================"

# Whisper models to test
for MODEL in tiny small base; do
    echo
    echo "--- Whisper-${MODEL} on GPU ---"
    echo
    
    for LANG in mn hu fr es; do
        echo "  Processing ${LANG}..."
        
        # Find audio files for this language
        for WAVFILE in data/wav/${LANG}/*.wav; do
            [ -e "$WAVFILE" ] || continue
            
            BASENAME=$(basename "$WAVFILE" .wav)
            
            # Run Whisper
            python scripts/run_whisper.py \
                --mode hinted \
                --model "${MODEL}" \
                --device cuda \
                --infile "${WAVFILE}" \
                --hint-lang "${LANG}" \
                --outdir "${OUTDIR}/whisper_${MODEL}/transcripts" \
                2>&1 | grep -v "FutureWarning" || true
        done
    done
    
    echo "  ✓ Whisper-${MODEL} complete"
done

echo
echo "======================================"
echo "Phase 2: Wav2Vec2 on GPU"
echo "======================================"
echo

for LANG in mn hu fr es; do
    echo "  Processing ${LANG}..."
    
    for WAVFILE in data/wav/${LANG}/*.wav; do
        [ -e "$WAVFILE" ] || continue
        
        # Run Wav2Vec2
        python scripts/asr_wav2vec2.py \
            --mode hinted \
            --device cuda \
            --infile "${WAVFILE}" \
            --hint-lang "${LANG}" \
            --outdir "${OUTDIR}/wav2vec2/transcripts" \
            --save-json \
            2>&1 | grep -v "FutureWarning" || true
    done
done

echo "  ✓ Wav2Vec2 complete"

echo
echo "======================================"
echo "Phase 3: Collect Metrics"
echo "======================================"
echo

# Collect all JSON outputs for analysis
find "${OUTDIR}" -name "*.json" > "${OUTDIR}/all_results.txt"
echo "Found $(wc -l < ${OUTDIR}/all_results.txt) result files"

# Create summary
python -c "
import json
import glob
from pathlib import Path

results = []
for json_file in glob.glob('${OUTDIR}/**/**.json', recursive=True):
    try:
        with open(json_file) as f:
            data = json.load(f)
            results.append(data)
    except:
        pass

if results:
    print(f'\\nProcessed {len(results)} results')
    
    # Quick stats
    rtfs = [r.get('rtf', 0) for r in results if 'rtf' in r]
    if rtfs:
        print(f'Average RTF: {sum(rtfs)/len(rtfs):.3f}')
        print(f'Min RTF: {min(rtfs):.3f}')
        print(f'Max RTF: {max(rtfs):.3f}')
else:
    print('No results found')
" || echo "Could not generate summary"

echo
echo "======================================"
echo "✅ GPU Sweep Complete!"
echo "======================================"
echo
echo "Results saved to: ${OUTDIR}/"
echo
echo "Next steps:"
echo "  1. Compare with CPU results"
echo "  2. Generate comparison plots"
echo "  3. Update thesis materials:"
echo "     nano docs/thesis_materials/06_results_gpu.md"
echo "  4. Commit:"
echo "     ./scripts/document_milestone.sh \"Completed GPU evaluation\""
echo
