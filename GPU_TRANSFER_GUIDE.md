# 🚀 GPU Server Experiment Guide

## Files to Transfer to GPU Server

### 1. Audio Data (80MB)
```bash
data/wav/mn/*.mp3  (1000 files)
data/wav/hu/*.mp3  (1000 files)
```

### 2. Scripts
```bash
scripts/compare_systems.py
scripts/run_whisper.py
scripts/asr_wav2vec2.py
scripts/run_comparison_batch.sh
```

### 3. Dependencies File
```bash
requirements.txt (will create below)
```

---

## Step-by-Step GPU Setup

### On Your MacBook (Prepare Package):

```bash
# Create transfer package
cd ~/thesis-asr
tar -czf gpu_experiment.tar.gz data/wav/ scripts/*.py scripts/*.sh requirements.txt

# Check size
ls -lh gpu_experiment.tar.gz
```

### Transfer to GPU Server:

```bash
# Transfer to bistromat GPU server
scp -P 15270 gpu_experiment.tar.gz mugi@bistromat.tmit.bme.hu:~/
```

### On GPU Server:

```bash
# SSH into server
ssh -p 15270 mugi@bistromat.tmit.bme.hu

# Extract
cd ~
tar -xzf gpu_experiment.tar.gz

# Install dependencies
pip install -r requirements.txt

# Verify GPU available
python -c "import torch; print('GPU:', torch.cuda.is_available())"

# Make scripts executable
chmod +x scripts/*.sh

# Run experiment (will use GPU automatically)
nohup ./scripts/run_comparison_batch.sh > experiment_gpu.txt 2>&1 &

# Monitor progress
tail -f experiment_gpu.txt
```

---

## Expected Timeline on GPU

- Hungarian (1000 files): ~2-3 hours
- Mongolian (1000 files): ~4-6 hours
- **Total: 6-9 hours** (vs 2 weeks on CPU!)

---

## Check Progress Remotely

```bash
# SSH into server and check
ssh -p 15270 mugi@bistromat.tmit.bme.hu
cd ~
./scripts/check_experiment_status.sh
```

---

## Download Results When Done

```bash
# On your MacBook
scp -P 15270 -r mugi@bistromat.tmit.bme.hu:~/results/ ~/thesis-asr/results/
```
