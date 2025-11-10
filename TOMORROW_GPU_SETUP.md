# 🌅 Tomorrow Morning: GPU Server Setup

**Time Needed**: 20-30 minutes  
**Goal**: Get environment ready on bistromat

---

## ✅ What We Know

**Connection**: ✅ Works!  
**Hardware**: 2x NVIDIA RTX A6000 (49GB VRAM each) 🔥  
**Issue**: Conda not in default PATH (need to set up)

---

## 🚀 Step-by-Step Setup (Tomorrow Morning)

### 1. Connect to Server (1 min)
```bash
ssh -p 15270 mugi@bistromat.tmit.bme.hu
# Enter password when prompted
```

### 2. Check Python Environment (2 min)
```bash
# Check what's available
python3 --version
which python3
which pip3

# Check if conda exists somewhere
ls ~/miniconda3/bin/conda 2>/dev/null || ls ~/anaconda3/bin/conda 2>/dev/null || echo "Need to install conda"
```

### 3. Install Miniconda (if needed, 5 min)
```bash
# If conda not found, install it
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
rm Miniconda3-latest-Linux-x86_64.sh

# Initialize conda
~/miniconda3/bin/conda init bash
source ~/.bashrc
```

### 4. Clone Your Repo (2 min)
```bash
# Clone thesis repo
git clone git@github.com:Munkhchimeg-Sergelen/thesis.git thesis-asr
cd thesis-asr

# Pull latest if already exists
git pull
```

### 5. Create Environment (10 min)
```bash
# Create conda environment from your yml file
conda env create -f environment.yml

# Activate it
conda activate asr-env

# Verify PyTorch with CUDA
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

### 6. Save Hardware Info (2 min)
```bash
# Save GPU specs
nvidia-smi > docs/gpu_hardware_info.txt

# Save environment info
python -c "
import torch
with open('docs/gpu_env_info.txt', 'w') as f:
    f.write(f'PyTorch: {torch.__version__}\n')
    f.write(f'CUDA: {torch.version.cuda}\n')
    f.write(f'GPU 0: {torch.cuda.get_device_name(0)}\n')
    f.write(f'GPU 1: {torch.cuda.get_device_name(1)}\n')
    f.write(f'VRAM 0: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB\n')
    f.write(f'VRAM 1: {torch.cuda.get_device_properties(1).total_memory / 1e9:.1f} GB\n')
"

# Check the file
cat docs/gpu_env_info.txt
```

### 7. Quick Test (5 min)
```bash
# Test Whisper on GPU
python scripts/run_whisper.py \
  --mode hinted \
  --model tiny \
  --device cuda \
  --infile data/wav/es/es_test.wav \
  --hint-lang es

# If it works, you're ready! 🎉
```

---

## 🎯 If Everything Works

You're ready to run the full GPU sweep:
```bash
# Run full evaluation
./scripts/run_gpu_sweep.sh

# This will take 1-2 hours
# Use tmux to keep it running:
tmux new -s thesis
./scripts/run_gpu_sweep.sh
# Detach with: Ctrl+B then D
```

---

## 🆘 Troubleshooting

### Conda Not Found After Install
```bash
# Manually initialize
~/miniconda3/bin/conda init bash
source ~/.bashrc
```

### PyTorch Can't Find CUDA
```bash
# Check CUDA version
nvidia-smi

# Reinstall PyTorch with correct CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Permission Issues
```bash
# Make sure you're in your home directory
cd ~
pwd  # Should show /home/mugi or similar
```

---

## 📝 After Setup Complete

Commit the hardware info:
```bash
git add docs/gpu_hardware_info.txt docs/gpu_env_info.txt
git commit -m "[2025-11-11] GPU server setup complete - 2x RTX A6000"
git push
```

---

## 🎯 Success Criteria

By end of setup:
- [ ] Can connect to server
- [ ] Conda environment works
- [ ] PyTorch detects CUDA
- [ ] Whisper runs on GPU
- [ ] Hardware specs saved

**Then you're ready for full GPU evaluation!** 🚀

---

## 💡 Pro Tip

With **2x RTX A6000**, you have TONS of VRAM (98 GB total!). You can:
- Run Whisper-large if you want
- Run multiple experiments in parallel
- Not worry about memory at all

**This is high-end hardware. Perfect for your thesis!** 💪
