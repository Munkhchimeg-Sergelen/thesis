#!/bin/bash
# Test Wav2Vec2 implementation

set -e

echo "================================"
echo "Testing Wav2Vec2 Implementation"
echo "================================"
echo

# Check environment
echo "[1/4] Checking conda environment..."
if ! conda info --envs | grep -q "asr-env"; then
    echo "ERROR: asr-env not found. Run: conda env create -f environment.yml"
    exit 1
fi
echo "✓ asr-env exists"
echo

# Check test audio
echo "[2/4] Checking test audio..."
if [ ! -f "data/wav/es/es_test.wav" ]; then
    echo "Creating test audio..."
    conda run -n asr-env python scripts/create_test_audio.py
fi
echo "✓ Test audio exists"
echo

# Test Wav2Vec2 in hinted mode
echo "[3/4] Testing Wav2Vec2 (hinted mode)..."
echo "Command: python scripts/asr_wav2vec2.py --mode hinted --infile data/wav/es/es_test.wav --hint-lang es --device cpu --save-json"
echo

# NOTE: User must activate environment manually
echo "⚠️  MANUAL STEP REQUIRED:"
echo
echo "Please run these commands in your terminal:"
echo
echo "  conda activate asr-env"
echo "  python scripts/asr_wav2vec2.py --mode hinted \\"
echo "    --infile data/wav/es/es_test.wav \\"
echo "    --hint-lang es \\"
echo "    --device cpu \\"
echo "    --save-json"
echo
echo "If successful, you should see:"
echo "  [Wav2Vec2] Loading facebook/wav2vec2-xls-r-300m on cpu..."
echo "  [Wav2Vec2] Model loaded."
echo "  [Wav2Vec2] Transcribing: data/wav/es/es_test.wav"
echo "  <transcription output>"
echo
echo "[4/4] Next steps..."
echo
echo "After Wav2Vec2 works, run comparison:"
echo "  python scripts/compare_systems.py \\"
echo "    --audio data/wav/es/es_test.wav \\"
echo "    --mode hinted \\"
echo "    --lang es \\"
echo "    --whisper-model tiny"
echo
echo "================================"
echo "Setup guide complete!"
echo "================================"
