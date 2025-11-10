# 🌅 Tomorrow with GPU Access (Nov 11)

**Advantage**: You can run CPU + GPU in parallel!  
**Strategy**: Get CPU baseline working, then start GPU  
**Time**: Can complete 2 days of work in 1 day 🚀

---

## 🎯 Two-Track Approach

### Track A: CPU Work (Morning, 2-3 hours)
**On your laptop**:
1. Get audio data
2. Test both systems
3. Run CPU comparison

### Track B: GPU Work (Afternoon, 2-3 hours)  
**On professor's server**:
1. Setup environment
2. Test GPU
3. Run GPU sweep

**By end of day**: Both CPU and GPU results! 💪

---

## ☕ Morning: CPU Track (Your Laptop)

### 1. Get Audio Data (20 min)
```bash
cd ~/thesis-asr
conda activate asr-env

# Download Common Voice samples
python scripts/download_common_voice.py
```

### 2. Test Systems (10 min)
```bash
# Test Wav2Vec2
python scripts/asr_wav2vec2.py \
  --mode hinted \
  --infile data/wav/es/es_test.wav \
  --hint-lang es \
  --device cpu \
  --save-json

# If works, you're good!
```

### 3. Run CPU Comparison (45 min)
```bash
# Run full comparison
./scripts/run_comparison_batch.sh small cpu

# Review results
ls -l results/comparison_*/
```

### 4. Document & Push (10 min)
```bash
# Commit so GPU server can pull latest data
git add data/wav data/ref results/comparison_*
git commit -m "[2025-11-11] CPU baseline complete, ready for GPU"
git push
```

---

## 🚀 Afternoon: GPU Track (Professor's Server)

### 1. SSH to GPU Server
```bash
# Your server access command
ssh [your-username]@[server-address]
```

### 2. Setup Environment (10 min)
```bash
# Run setup script
bash gpu_quick_setup.sh

# This will:
# - Clone/pull your repo
# - Create conda environment  
# - Verify CUDA
# - Save hardware info
```

### 3. Test GPU (5 min)
```bash
conda activate asr-env

# Quick GPU test
python scripts/run_whisper.py \
  --mode hinted \
  --model tiny \
  --device cuda \
  --infile data/wav/es/es_test.wav \
  --hint-lang es
```

**Expected**: Much faster than CPU!

### 4. Run GPU Sweep (60-90 min)
```bash
# Run full GPU evaluation
./scripts/run_gpu_sweep.sh

# This runs:
# - Whisper tiny/small/base on GPU
# - Wav2Vec2 on GPU
# - Collects all metrics
```

**Note**: This will take time. You can:
- Run in `screen` or `tmux` session
- Do other work while it runs
- Come back to check progress

### 5. Download Results (5 min)
```bash
# On server: commit results
git add results/gpu_sweep_* docs/gpu_*_info.txt
git commit -m "[2025-11-11] GPU evaluation complete"
git push

# On laptop: pull results
git pull
```

---

## 📊 End of Day: Analysis

### What You'll Have
- ✅ CPU comparison results
- ✅ GPU evaluation results
- ✅ Both systems tested on both devices
- ✅ Hardware specs documented

### Quick Comparison
```bash
# Compare CPU vs GPU
python -c "
import json
import glob

print('CPU Results:')
for f in glob.glob('results/comparison_*/system_comparison.csv'):
    print(f'  {f}')

print('\\nGPU Results:')  
for f in glob.glob('results/gpu_sweep_*/all_results.txt'):
    print(f'  {f}')
"
```

---

## 🎯 Alternative Plan (If Time is Tight)

### Minimum Viable (3-4 hours total)

**Morning**: 
- Download audio (20 min)
- Test systems on CPU (20 min)
- Skip full CPU comparison for now

**Afternoon**:
- Setup GPU (15 min)
- Run GPU comparison only (60 min)
- **GPU results are more impressive anyway!**

**Later**: Come back to CPU for comparison

---

## 💡 Pro Tips

### For Long-Running GPU Jobs

**Use tmux/screen**:
```bash
# On GPU server
tmux new -s thesis

# Run your sweep
./scripts/run_gpu_sweep.sh

# Detach: Ctrl+B then D
# Reattach later: tmux attach -t thesis
```

### Parallel Experimentation
- Run different model sizes simultaneously if server has capacity
- Test one language per GPU if multi-GPU

### Resource Monitoring
```bash
# Watch GPU usage in another terminal
watch -n 1 nvidia-smi
```

---

## 📝 Documentation Checklist

As you work, document:
- [ ] GPU hardware specs → `docs/gpu_hardware_info.txt`
- [ ] Environment details → `docs/gpu_env_info.txt`
- [ ] Commands run → `docs/appendix_commands.md`
- [ ] Speed observations → `docs/thesis_materials/06_results_gpu.md`
- [ ] Any issues → `docs/issues_log.md`

---

## 🎯 Success Criteria

By end of Nov 11:
- ✅ Audio data downloaded (10-15 files per lang)
- ✅ Both systems tested
- ✅ CPU results OR GPU results (ideally both!)
- ✅ Hardware specs documented
- ✅ Everything committed to GitHub

**Even partial success = great progress!**

---

## 🆘 If Things Go Wrong

### GPU Not Available
- Run everything on CPU
- Still have 2 systems to compare
- GPU is bonus, not required

### Audio Download Fails
- Use test audio
- Document as limitation
- Get real data later

### Time Runs Short
- Pick one track (GPU preferred)
- Do other track tomorrow
- Both aren't needed same day

---

## 📞 Check-in Point

**Evening (6-7pm)**:
Share:
- What worked
- What blocked you
- What you have

Even if only partial success, we'll plan next steps!

---

## 🚀 Bottom Line

**With GPU access, you can accelerate by 1-2 days!**

**Priority Order**:
1. Get audio data ✅
2. Test systems work ✅
3. GPU evaluation (impressive!) ⭐
4. CPU comparison (for completeness)

**By tomorrow night, you could have most experimental work done!**

---

**Let's crush Day 2! 💪**
