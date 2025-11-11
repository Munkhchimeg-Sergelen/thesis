#!/bin/bash
# Simple GPU Setup Script for bistromat
# Run this ON THE GPU SERVER after connecting

echo "======================================"
echo "🖥️  GPU Server Setup for Thesis"
echo "======================================"
echo

# Step 1: Check GPU
echo "[1/6] Checking GPU..."
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo

# Step 2: Check/Install Miniconda
echo "[2/6] Setting up Miniconda..."
if [ ! -d "$HOME/miniconda3" ]; then
    echo "Installing Miniconda..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p $HOME/miniconda3
    rm /tmp/miniconda.sh
    $HOME/miniconda3/bin/conda init bash
    source ~/.bashrc
    echo "✓ Miniconda installed"
else
    echo "✓ Miniconda already installed"
fi

# Make sure conda is in PATH
export PATH="$HOME/miniconda3/bin:$PATH"

echo

# Step 3: Clone/Update Repo
echo "[3/6] Cloning repository..."
if [ ! -d "$HOME/thesis-asr" ]; then
    cd ~
    git clone https://github.com/Munkhchimeg-Sergelen/thesis.git thesis-asr
    cd thesis-asr
    echo "✓ Repository cloned"
else
    cd $HOME/thesis-asr
    git pull
    echo "✓ Repository updated"
fi

echo

# Step 4: Create Environment
echo "[4/6] Creating conda environment..."
echo "This may take 5-10 minutes..."

conda create -n asr-env python=3.10 -y

echo "✓ Base environment created"
echo

# Step 5: Install Packages
echo "[5/6] Installing PyTorch with CUDA..."
conda activate asr-env
conda install -n asr-env pytorch torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y

echo
echo "Installing transformers and other packages..."
conda run -n asr-env pip install transformers datasets soundfile librosa jiwer

echo "✓ Packages installed"
echo

# Step 6: Verify Setup
echo "[6/6] Verifying installation..."
conda run -n asr-env python -c "
import torch
print('✓ PyTorch:', torch.__version__)
print('✓ CUDA available:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('✓ CUDA version:', torch.version.cuda)
    print('✓ GPU 0:', torch.cuda.get_device_name(0))
    if torch.cuda.device_count() > 1:
        print('✓ GPU 1:', torch.cuda.get_device_name(1))
    print('✓ GPU count:', torch.cuda.device_count())
"

echo
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo
echo "Next steps:"
echo "1. Activate environment: conda activate asr-env"
echo "2. Test Whisper: python scripts/run_whisper.py --mode hinted --model tiny --device cuda --infile data/wav/es/es_test.wav --hint-lang es"
echo "3. Run full sweep: ./scripts/run_gpu_sweep.sh"
echo
