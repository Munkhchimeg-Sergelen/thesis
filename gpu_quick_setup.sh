#!/bin/bash
# Quick GPU Setup & Test Script
# Run this on the GPU server to verify everything works

echo "======================================"
echo "🖥️  GPU Setup & Verification"
echo "======================================"
echo

# Check if on GPU server
if ! command -v nvidia-smi &> /dev/null; then
    echo "⚠️  WARNING: nvidia-smi not found"
    echo "   Are you on the GPU server?"
    echo
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ NVIDIA drivers detected"
    echo
    nvidia-smi
    echo
fi

# Check if repo exists
if [ ! -d "thesis-asr" ]; then
    echo "📥 Cloning repository..."
    git clone git@github.com:Munkhchimeg-Sergelen/thesis.git thesis-asr
    cd thesis-asr
else
    echo "✓ Repository exists"
    cd thesis-asr
    echo "📥 Pulling latest changes..."
    git pull
fi

echo

# Check conda environment
if ! conda env list | grep -q "asr-env"; then
    echo "🔧 Creating conda environment..."
    conda env create -f environment.yml
else
    echo "✓ Conda environment exists"
fi

echo

# Activate and verify
echo "🔍 Verifying environment..."
conda run -n asr-env python -c "
import sys
print('Python:', sys.version)

try:
    import torch
    print('✓ PyTorch:', torch.__version__)
    print('✓ CUDA available:', torch.cuda.is_available())
    if torch.cuda.is_available():
        print('✓ CUDA version:', torch.version.cuda)
        print('✓ GPU:', torch.cuda.get_device_name(0))
        print('✓ VRAM:', f'{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
except ImportError as e:
    print('✗ PyTorch not installed or CUDA issue:', e)
    sys.exit(1)

try:
    import transformers
    print('✓ Transformers:', transformers.__version__)
except ImportError:
    print('✗ Transformers not installed')
    sys.exit(1)

print('\\n✅ Environment ready!')
"

if [ $? -ne 0 ]; then
    echo
    echo "❌ Environment setup failed"
    echo "   Try: conda env update -f environment.yml"
    exit 1
fi

echo

# Save hardware info
echo "💾 Saving hardware info..."
nvidia-smi > docs/gpu_hardware_info.txt 2>/dev/null || echo "nvidia-smi output" > docs/gpu_hardware_info.txt
conda run -n asr-env python -c "
import torch
with open('docs/gpu_env_info.txt', 'w') as f:
    f.write(f'PyTorch: {torch.__version__}\\n')
    if torch.cuda.is_available():
        f.write(f'CUDA: {torch.version.cuda}\\n')
        f.write(f'Device: {torch.cuda.get_device_name(0)}\\n')
        f.write(f'VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB\\n')
print('✓ Saved to docs/gpu_env_info.txt')
" 2>/dev/null

echo
echo "======================================"
echo "✅ GPU Setup Complete!"
echo "======================================"
echo
echo "Next steps:"
echo "  1. Test Whisper on GPU:"
echo "     conda activate asr-env"
echo "     python scripts/run_whisper.py --mode hinted --model tiny \\"
echo "       --device cuda --infile data/wav/es/es_test.wav --hint-lang es"
echo
echo "  2. If that works, run full GPU sweep:"
echo "     ./scripts/run_gpu_sweep.sh"
echo
