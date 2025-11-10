#!/bin/bash
# Quick checklist and commands for Nov 11

echo "======================================"
echo "📋 Tomorrow's Tasks (Nov 11)"
echo "======================================"
echo

echo "✅ Step 1: Activate Environment"
echo "Command: conda activate asr-env"
echo

echo "✅ Step 2: Verify Wav2Vec2 Works"
echo "Command:"
echo "  python scripts/asr_wav2vec2.py \\"
echo "    --mode hinted \\"
echo "    --infile data/wav/es/es_test.wav \\"
echo "    --hint-lang es \\"
echo "    --device cpu \\"
echo "    --save-json"
echo
echo "Expected: Model downloads (~1.2GB), then transcribes"
echo

echo "✅ Step 3: Check Audio Data Status"
echo "Command: ls -lh data/wav/*/*.wav | wc -l"
echo "Current: $(find data/wav -name "*.wav" 2>/dev/null | wc -l | tr -d ' ') files"
echo

if [ $(find data/wav -name "*.wav" 2>/dev/null | wc -l) -gt 4 ]; then
    echo "✓ You have audio data! Ready to compare."
    echo
    echo "✅ Step 4: Run System Comparison"
    echo "Command: ./scripts/run_comparison_batch.sh"
else
    echo "⚠️  You need more audio data."
    echo
    echo "✅ Step 4a: Get Audio Data (Choose One)"
    echo
    echo "Option A: Download from Common Voice"
    echo "  1. Go to: https://commonvoice.mozilla.org/"
    echo "  2. Download: Mongolian, Hungarian, French, Spanish"
    echo "  3. Extract 10-20 files per language"
    echo "  4. Place in: data/wav/{lang}/"
    echo
    echo "Option B: Try FLEURS (if API fixed)"
    echo "  pip install --upgrade datasets"
    echo "  python scripts/fetch_small_multilang.py"
    echo
    echo "Option C: Use existing audio elsewhere"
    echo "  Copy your audio files to data/wav/{lang}/"
    echo
    echo "Then create references:"
    echo "  # For each audio file, create matching .txt in data/ref/{lang}/"
    echo
fi

echo "✅ Step 5: Document & Commit"
echo "Command: ./scripts/document_milestone.sh \"Completed first comparison\""
echo

echo "======================================"
echo "📚 Key Files to Reference:"
echo "  - NEXT_STEPS.md (detailed instructions)"
echo "  - MASTER_PLAN_UPDATED.md (full schedule)"
echo "  - docs/gpu_server_plan.md (for GPU work)"
echo "======================================"
