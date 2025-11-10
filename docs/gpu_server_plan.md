# GPU Server Evaluation Plan

**Server Access**: ✅ Available (Professor's GPU server)  
**Purpose**: Scale experiments + GPU vs CPU comparison  
**Priority**: High (enables richer analysis)

---

## 🎯 Why GPU Matters for Your Thesis

### 1. Practical Deployment Insights
- **CPU**: Batch processing, cost-sensitive applications
- **GPU**: Real-time, high-throughput scenarios
- **Comparison**: Speed-accuracy-cost trade-offs

### 2. Model Scaling
- Whisper-tiny (CPU): baseline
- Whisper-small/base (GPU): better quality
- Shows how model size impacts performance

### 3. Complete Evaluation
- Hardware diversity (CPU vs GPU)
- Resource profiling (VRAM, latency)
- Deployment recommendations

---

## 📅 Integration with 13-Day Plan

### Original Plan
```
Week 1: CPU experiments only
Week 2: Writing
```

### Updated Plan (with GPU)
```
Week 1: 
  Nov 10-11: CPU baseline + Wav2Vec2 (done/in-progress)
  Nov 12-13: GPU evaluation + scaling
  Nov 14-15: Analysis + comparison
  Nov 16: Buffer

Week 2: Writing (with richer results!)
```

**Impact**: GPU runs in parallel with CPU analysis → no time lost!

---

## 🚀 GPU Evaluation Workflow

### Phase A: Environment Setup (30 min)

**On GPU Server**:
```bash
# 1. Clone repo
git clone <your-repo-url>
cd thesis-asr

# 2. Create conda env
conda env create -f env/asr-env-wsl.yml
conda activate asr-env

# 3. Install GPU-specific packages
pip install pynvml  # GPU monitoring

# 4. Verify CUDA
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

**Document hardware**:
```bash
# Save GPU info
nvidia-smi > docs/gpu_hardware_info.txt

# Save to results for thesis
python -c "
import torch
print(f'PyTorch: {torch.__version__}')
print(f'CUDA: {torch.version.cuda}')
print(f'Device: {torch.cuda.get_device_name(0)}')
print(f'VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
" | tee docs/gpu_env_info.txt
```

### Phase B: Run Whisper on GPU (2-3 hours)

**Models to test**: tiny, small, base

```bash
# For each model size
for MODEL in tiny small base; do
  for LANG in mn hu fr es; do
    # Hinted mode
    make run_whisper_hinted \
      MODEL=$MODEL \
      DEVICE=cuda \
      FILE=data/wav/$LANG/*.wav \
      LANG=$LANG
    
    # LID→ASR mode
    make run_whisper_lid \
      MODEL=$MODEL \
      DEVICE=cuda \
      FILE=data/wav/$LANG/*.wav
  done
done
```

**Automated batch script** (create this):
```bash
# scripts/run_gpu_sweep.sh
#!/bin/bash
for model in tiny small base; do
  python scripts/sweep_decode.py \
    --model $model \
    --device cuda \
    --in data/wav \
    --out results/transcripts/gpu_sweep/$model
done
```

### Phase C: Run Wav2Vec2 on GPU (1-2 hours)

```bash
for LANG in mn hu fr es; do
  make run_wav2vec2_hinted \
    DEVICE=cuda \
    FILE=data/wav/$LANG/*.wav \
    LANG=$LANG
done
```

### Phase D: Performance Profiling (1 hour)

**Measure VRAM + latency**:
```bash
# Whisper with GPU monitoring
python scripts/measure_perf.py \
  --cmd "python scripts/run_whisper.py --mode hinted --model small --device cuda --infile data/wav/es/es01.wav --hint-lang es" \
  --audio data/wav/es/es01.wav \
  --device cuda \
  --out results/metrics/perf_gpu_whisper_small_$(date +%s).json
```

**Expected metrics**:
- VRAM usage (MB)
- GPU utilization (%)
- CUDA kernel time
- Total latency
- RTF (real-time factor)

---

## 📊 Comparison Tables to Generate

### Table 1: CPU vs GPU Performance

| System | Model | Device | RTF | Latency (s) | Memory (MB) | WER (avg) |
|--------|-------|--------|-----|-------------|-------------|-----------|
| Whisper | tiny | CPU | 1.5 | 15.0 | 1700 | 0.68 |
| Whisper | tiny | GPU | 0.2 | 2.0 | 800 (VRAM) | 0.68 |
| Whisper | small | CPU | 3.2 | 32.0 | 2400 | 0.58 |
| Whisper | small | GPU | 0.4 | 4.0 | 1200 (VRAM) | 0.58 |
| Wav2Vec2 | 300M | CPU | 0.8 | 8.0 | 1500 | 0.62 |
| Wav2Vec2 | 300M | GPU | 0.15 | 1.5 | 600 (VRAM) | 0.62 |

### Table 2: Model Scaling on GPU

| Model | Params | VRAM (MB) | RTF | WER (HU) | WER (MN) | WER (ES) | WER (FR) |
|-------|--------|-----------|-----|----------|----------|----------|----------|
| Whisper-tiny | 39M | 800 | 0.2 | 0.85 | 1.03 | 0.17 | 0.42 |
| Whisper-small | 244M | 1200 | 0.4 | 0.72 | 0.88 | 0.12 | 0.35 |
| Whisper-base | 74M | 900 | 0.3 | 0.78 | 0.95 | 0.14 | 0.38 |

---

## 📈 Plots to Create

1. **Speed Comparison**: RTF bar chart (CPU vs GPU, all systems)
2. **Model Scaling**: WER vs model size (GPU only)
3. **Efficiency Frontier**: WER vs latency scatter (Pareto front)
4. **Resource Usage**: VRAM/RAM by system and model

---

## 🗂️ Results Organization

### Directory Structure
```
results/
  cpu/                    # Existing CPU results
    transcripts/
    metrics/
  gpu/                    # New GPU results
    transcripts/
      whisper_tiny/
      whisper_small/
      whisper_base/
      wav2vec2/
    metrics/
      perf_*.json         # GPU profiling
      wer_cer_gpu_*.csv
  comparison/             # CPU vs GPU analysis
    cpu_vs_gpu_summary.csv
    model_scaling.csv
    efficiency_table.csv
```

---

## 📝 Documentation Requirements

### During GPU Runs (capture immediately)

**1. Hardware Context** → `docs/gpu_hardware_info.txt`
```
GPU Model: [e.g., NVIDIA RTX 4090]
VRAM: [e.g., 24GB]
CUDA Version: [e.g., 12.1]
Driver: [e.g., 535.129.03]
CPU: [for reference]
RAM: [for reference]
```

**2. Per-Run Logs** → `results/gpu/logs/`
- Command executed
- Environment variables
- Start/end timestamps
- Any warnings/errors

**3. Summary After Runs** → `docs/gpu_results_summary.md`
- Key findings (CPU vs GPU speedup)
- Model scaling insights
- Failure modes on GPU
- Recommendations

### For Thesis Writing

Create these NOW (fill in after GPU runs):

**`docs/thesis_materials/`**:
- `01_methods_hardware.md` - Hardware specs for Methods section
- `02_results_gpu_cpu.md` - CPU/GPU comparison for Results
- `03_discussion_deployment.md` - Deployment insights for Discussion
- `04_figures_captions.md` - All figure captions
- `05_tables_data.csv` - All tables in CSV format

---

## ⏱️ Realistic Timeline

### Nov 12 (Tomorrow Afternoon/Evening)
- [ ] SSH to GPU server
- [ ] Setup environment (30 min)
- [ ] Test Whisper-tiny on 1 file (verify CUDA works)
- [ ] Document hardware specs

### Nov 13 (GPU Day)
- [ ] Morning: Full Whisper sweep (tiny/small/base, all langs)
- [ ] Afternoon: Wav2Vec2 on GPU
- [ ] Evening: Collect all results, commit to GitHub

### Nov 14 (Analysis Day)
- [ ] Generate comparison tables (CPU vs GPU)
- [ ] Create plots
- [ ] Write analysis notes
- [ ] Update `docs/gpu_results_summary.md`

---

## 🎓 Thesis Impact

### What GPU Adds to Your Thesis

**Before (CPU only)**:
- ✅ 2 systems compared
- ✅ 2 modes evaluated
- ✅ 4 languages tested
- ⚠️ Limited to one hardware config

**After (CPU + GPU)**:
- ✅ 2 systems compared
- ✅ 2 modes evaluated
- ✅ 4 languages tested
- ✅ **2 hardware configs** (CPU vs GPU)
- ✅ **Model scaling analysis** (tiny/small/base)
- ✅ **Deployment recommendations** (when to use what)
- ✅ **Resource profiling** (VRAM, latency, throughput)

### Additional Thesis Sections Enabled

1. **Methods**: Hardware comparison methodology
2. **Results**: "GPU Acceleration Analysis" subsection
3. **Discussion**: "Deployment Considerations" subsection
4. **Conclusions**: Practical recommendations for practitioners

---

## 🚨 Important Notes

### Do NOT Over-scope
- GPU is a **bonus**, not a requirement
- If GPU fails, CPU results are sufficient
- Focus on comparison, not exhaustive tuning

### Keep It Reproducible
- Document exact commands
- Save environment files
- Note any GPU-specific tweaks

### Time Management
- GPU runs can happen in parallel with writing
- Don't let GPU work delay thesis submission
- If GPU takes >2 days, skip and finish with CPU

---

## ✅ GPU Evaluation Checklist

### Pre-Run
- [ ] Environment verified (`torch.cuda.is_available()`)
- [ ] Hardware documented
- [ ] Git repo up-to-date on server
- [ ] Test run successful

### During Runs
- [ ] Capture all output logs
- [ ] Monitor VRAM usage
- [ ] Save transcripts + metrics
- [ ] Commit results to GitHub after each batch

### Post-Run
- [ ] Generate comparison tables
- [ ] Create plots
- [ ] Write summary document
- [ ] Update thesis materials folder
- [ ] Push everything to GitHub

---

## 🎯 Success Criteria

**Minimum** (if time-constrained):
- Whisper-small on GPU vs CPU (1 system, 2 configs)
- Basic speedup comparison
- 1 comparison table

**Target** (realistic):
- Whisper (tiny/small) + Wav2Vec2 on GPU
- Full CPU vs GPU comparison
- Model scaling analysis
- 3-4 comparison tables/plots

**Stretch** (if time permits):
- Whisper-base included
- NeMo integration on GPU
- Detailed profiling

---

**Bottom Line**: GPU is a **force multiplier** for your thesis quality, but don't let it delay submission. Get it done by Nov 14 or proceed with CPU-only results.
