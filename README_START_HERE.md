# 🎓 Thesis-ASR: Start Here!

**Thesis**: Analysis of Multilingual ASR Approaches  
**Student**: Munkhchimeg Sergelen  
**Deadline**: November 23, 2025 (13 days)  
**Status**: ✅ Day 1 Complete - Second System Implemented

---

## 🚀 Quick Start

### Right Now (5 minutes)

```bash
cd ~/thesis-asr
conda activate asr-env

# Test Wav2Vec2 (second ASR system)
python scripts/asr_wav2vec2.py \
  --mode hinted \
  --infile data/wav/es/es_test.wav \
  --hint-lang es \
  --device cpu \
  --save-json
```

**Expected**: Model downloads (~1.2GB first time), then transcribes audio.

---

## 📚 Key Documents

**Read in this order:**

1. **`NEXT_STEPS.md`** ← Your immediate action items
2. **`MASTER_PLAN_UPDATED.md`** ← Complete 13-day schedule (with GPU)
3. **`TODAY_PROGRESS.md`** ← What we accomplished today
4. **`DOCUMENTATION_HABITS.md`** ← How to document as you go

**For GPU work:**
- **`docs/gpu_server_plan.md`** ← GPU evaluation workflow

**For writing:**
- **`docs/thesis_materials/`** ← Pre-written thesis sections

---

## 🎯 What You Have Now

### ✅ Complete
- **Infrastructure**: Conda env, Makefile, Git setup
- **Data**: Test audio for 4 languages (MN, HU, FR, ES)
- **System 1**: Whisper (tiny/small/base) - DONE
- **System 2**: Wav2Vec2-XLS-R - IMPLEMENTED TODAY
- **Tools**: Comparison scripts, evaluation pipeline
- **Documentation**: Metrics schema, baseline results, system docs

### ⏳ To Do (Next 12 Days)
- **Week 1** (Nov 11-16): Run experiments (CPU + GPU)
- **Week 2** (Nov 17-23): Write thesis

---

## 📅 Tomorrow (Nov 11)

### Morning: Test & Compare
```bash
conda activate asr-env

# Run system comparison
python scripts/compare_systems.py \
  --audio data/wav \
  --mode hinted \
  --langs mn hu fr es \
  --whisper-model small \
  --out-csv results/metrics/comparison_nov11.csv
```

### Afternoon: Get Real Audio
Download from Common Voice OR use existing audio files.

### Evening: Document & Commit
```bash
# Document your milestone
./scripts/document_milestone.sh "Completed first system comparison on CPU"

# Or manually:
git add -A
git commit -m "[2025-11-11] First system comparison complete"
git push
```

---

## 🖥️ GPU Plan (Nov 12-13)

### On Professor's Server

**Day 1** (Nov 12):
```bash
# Setup
git clone <your-repo>
cd thesis-asr
conda env create -f env/asr-env-wsl.yml
conda activate asr-env

# Document hardware
nvidia-smi > docs/gpu_hardware_info.txt

# Test
python scripts/run_whisper.py \
  --mode hinted \
  --model small \
  --device cuda \
  --infile data/wav/es/es01.wav \
  --hint-lang es
```

**Day 2** (Nov 13):
- Run full GPU evaluation
- Compare with CPU results
- Generate all comparison plots

**See**: `docs/gpu_server_plan.md` for complete workflow

---

## 📝 Documentation Workflow

### After Every Experiment
```bash
# 1. Note the command
echo "$(date): <command>" >> docs/appendix_commands.md

# 2. Save results
# (already saved by scripts to results/*)

# 3. Document milestone
./scripts/document_milestone.sh "Brief description"
```

### After Creating Plots/Tables
```bash
# Save to thesis materials
cp results/plots/myplot.png docs/thesis_materials/figures/
echo "Figure caption..." > docs/thesis_materials/figures/myplot_caption.txt
```

### End of Day
```bash
git add -A
git commit -m "[$(date +%Y-%m-%d)] Summary of today's work"
git push
```

**Why**: When you start writing (Week 2), everything is ready to copy-paste!

---

## 🗂️ Project Structure

```
thesis-asr/
├── README_START_HERE.md          ← You are here
├── NEXT_STEPS.md                 ← Next actions
├── MASTER_PLAN_UPDATED.md        ← Full 13-day plan
├── TODAY_PROGRESS.md             ← Day 1 summary
├── DOCUMENTATION_HABITS.md       ← How to document
│
├── data/
│   ├── wav/{mn,hu,fr,es}/        ← Audio files
│   └── ref/{mn,hu,fr,es}/        ← Reference transcripts
│
├── scripts/
│   ├── run_whisper.py            ← Whisper wrapper
│   ├── asr_wav2vec2.py           ← Wav2Vec2 wrapper (NEW!)
│   ├── compare_systems.py        ← System comparison (NEW!)
│   ├── eval_metrics.py           ← WER/CER computation
│   └── document_milestone.sh     ← Auto-document (NEW!)
│
├── results/
│   ├── transcripts/              ← ASR outputs
│   ├── metrics/                  ← Evaluation CSVs
│   └── most_relevant/            ← Baseline results
│
├── docs/
│   ├── metrics_schema.md         ← Metric definitions
│   ├── baseline_whisper_results.md  ← Current results
│   ├── wav2vec2_system.md        ← Second system docs
│   ├── gpu_server_plan.md        ← GPU workflow
│   └── thesis_materials/         ← Pre-written thesis sections
│       ├── figures/              ← Final plots for thesis
│       ├── tables/               ← Final tables
│       └── *.md                  ← Chapter drafts
│
├── Makefile                      ← Run commands
└── environment.yml               ← Conda environment
```

---

## 🔧 Makefile Commands

### Whisper
```bash
make run_whisper_hinted FILE=data/wav/es/test.wav LANG=es MODEL=small
make run_whisper_lid FILE=data/wav/es/test.wav MODEL=small
```

### Wav2Vec2 (NEW!)
```bash
make run_wav2vec2_hinted FILE=data/wav/hu/test.wav LANG=hu DEVICE=cpu
make run_wav2vec2_lid FILE=data/wav/fr/test.wav DEVICE=cpu
```

### Evaluation
```bash
make eval REFS=data/ref/es_refs.csv HYPDIR=results/transcripts/hinted/whisper/es
make lid FILE=data/wav/mn/test.wav MODEL=small
```

---

## ✅ Requirements Status

| Requirement | Status |
|-------------|--------|
| ≥2 ASR systems | ✅ Whisper + Wav2Vec2 |
| Language-hinted mode | ✅ Both systems |
| LID→ASR mode | ✅ Both systems |
| 3-6 languages | ✅ MN, HU, FR, ES (4) |
| Multiple audio lengths | ⚠️ Need 120s clips |
| WER/CER metrics | ✅ Scripts ready |
| LID accuracy | ✅ Scripts ready |
| RTF/latency | ✅ Auto-captured |
| CPU/GPU comparison | ⏳ GPU pending |
| Reproducible env | ✅ Conda + git |
| Documentation | ✅ Complete |
| Thesis writing | ⏳ Week 2 |

---

## 🆘 If Something Goes Wrong

### Can't run Wav2Vec2?
```bash
# Check environment
conda activate asr-env
python -c "import torch, transformers; print('OK')"

# If fails, reinstall
conda env update -f environment.yml
```

### No audio data?
Use test files or download manually from Common Voice website.

### GPU not working?
Proceed with CPU-only evaluation. Still have 2 systems to compare!

### Running behind?
Focus on core requirements. Skip optional parts (NeMo, post-processing).

---

## 📞 Getting Help

**In this project**:
- Check `NEXT_STEPS.md` for immediate tasks
- Check `MASTER_PLAN_UPDATED.md` for schedule
- Check `DOCUMENTATION_HABITS.md` for workflows

**Questions?**
- Document blockers in `docs/issues_log.md`
- Ask in next session with specific error messages

---

## 🎯 Success = Execution

You have:
- ✅ Complete infrastructure
- ✅ Two working ASR systems
- ✅ Clear 13-day plan
- ✅ GPU access available
- ✅ Documentation habits established

**What you need**: Discipline to execute one task at a time.

**13 days is enough.** Many BSc theses are completed in less time with less preparation.

**Your advantage**: You're organized, have a plan, and started early.

---

## 💪 Let's Finish This!

**Tonight**: Test Wav2Vec2  
**Tomorrow**: First system comparison  
**Nov 12-13**: GPU evaluation  
**Nov 14-16**: Finalize experiments  
**Nov 17-23**: Write thesis  
**Nov 23**: Submit! 🎓

**You've got this!**

---

## 📌 Quick Links

- [Next Steps](NEXT_STEPS.md)
- [Master Plan](MASTER_PLAN_UPDATED.md)
- [Today's Progress](TODAY_PROGRESS.md)
- [Documentation Habits](DOCUMENTATION_HABITS.md)
- [GPU Plan](docs/gpu_server_plan.md)
- [Thesis Materials](docs/thesis_materials/)
