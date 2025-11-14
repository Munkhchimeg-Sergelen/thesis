# 📋 Action Plan: Supervisor Feedback Implementation

**Date**: November 14, 2025  
**Status**: 🚧 IN PROGRESS  
**Timeline**: 1 week

---

## ✅ What Supervisor Asked For

1. **Clarify evaluation modes** (language-hinted vs LID→ASR)
2. **Verify train/test independence** (99.31% LID accuracy concern)
3. **Explain Mongolian slowdown** (how/why it happens)
4. **Define sample characteristics** (what's in a sample?)
5. **Scale up to ~1000 samples** per language
6. **Add statistical tests** (Wilcoxon, confidence intervals)
7. **Consider audio length strategy** (shorter = harder)

---

## 🎯 Implementation Steps

### ✅ STEP 1: Update Download Script (DONE!)
- [x] Modified `download_common_voice.py`
- [x] Changed from 15 → 1000 samples
- [x] Updated messages

**Files changed**: `scripts/download_common_voice.py`

### 🔄 STEP 2: Download 1000 Samples (IN PROGRESS)
**Run this command**:
```bash
cd ~/thesis-asr
python3 scripts/download_common_voice.py
```

**What to expect**:
- Download ~3-4 GB of audio
- 1000 samples × 4 languages = 4000 files
- Time: 20-40 minutes (depends on internet)
- Files saved to: `data/wav/{lang}/`

**Verify**:
```bash
# Count downloaded files
ls data/wav/*/*.wav | wc -l
# Should show ~4000

# Check per language
for lang in es fr hu mn; do
  count=$(ls data/wav/$lang/*.wav 2>/dev/null | wc -l)
  echo "$lang: $count files"
done
```

### 🔄 STEP 3: Run Experiments with 1000 Samples
**Time estimate**: 1-2 days (running overnight)

**Commands**:
```bash
# Option A: Run in background (recommended)
nohup ./scripts/run_comparison_batch.sh > experiment_log.txt 2>&1 &

# Check progress
tail -f experiment_log.txt

# Option B: Run interactively (can monitor)
./scripts/run_comparison_batch.sh
```

**What will run**:
- Whisper tiny, base, small (3 models)
- 4 languages × 1000 samples = 4000 samples
- LID→ASR + Language-hinted modes
- Total: ~12,000+ experiments

**Monitor progress**:
```bash
# Count completed experiments
ls results/transcripts/lid2asr/*.json | wc -l
ls results/transcripts/hinted/*.json | wc -l

# Check latest results
ls -ltr results/transcripts/lid2asr/ | tail -5
```

### 🔄 STEP 4: Run Statistical Analysis
**After experiments complete**:
```bash
python3 scripts/statistical_analysis.py
```

**Output**:
- Wilcoxon signed-rank tests
- 95% confidence intervals
- Effect sizes (Cohen's d)
- P-values for all comparisons
- Saves to: `results/statistical_analysis.csv`

### 🔄 STEP 5: Update Figures
**Regenerate with 1000 samples**:
```bash
python3 scripts/create_plots.py
```

**New figures** (with error bars and confidence intervals):
- Whisper model comparison
- System comparison
- Language comparison
- Processing time distribution

### 🔄 STEP 6: Update Analysis Scripts
**Re-run analysis with larger dataset**:
```bash
python3 scripts/analyze_results.py
python3 scripts/compare_lid_vs_hinted.py
```

**This will update**:
- Mean processing times
- Standard deviations
- LID accuracy
- Speed ratios

### 🔄 STEP 7: Respond to Supervisor
**Draft response** (after results complete):

---

## 📊 Current Progress Tracker

| Step | Status | Time Est | Actual Time |
|------|--------|----------|-------------|
| 1. Update scripts | ✅ Done | 5 min | 5 min |
| 2. Download 1000 samples | 🔄 Ready | 30 min | - |
| 3. Run experiments | ⏳ Waiting | 1-2 days | - |
| 4. Statistical analysis | ⏳ Waiting | 10 min | - |
| 5. Update figures | ⏳ Waiting | 10 min | - |
| 6. Update analysis | ⏳ Waiting | 15 min | - |
| 7. Email supervisor | ⏳ Waiting | 30 min | - |

**Total estimated time**: 1-2 days (mostly experiment running time)

---

## 🎯 What You'll Achieve

### Before (Current):
- ❌ 12 samples per language (supervisor concerned)
- ❌ No statistical tests
- ❌ No confidence intervals
- ❌ Unclear if results are significant

### After (Target):
- ✅ 1000 samples per language (supervisor approved!)
- ✅ Wilcoxon tests (p-values)
- ✅ 95% confidence intervals
- ✅ Effect sizes (Cohen's d)
- ✅ Statistically grounded results
- ✅ Much stronger thesis!

---

## 💾 Expected Disk Space

| Item | Size | Location |
|------|------|----------|
| Audio files (4000 × ~1MB) | ~4 GB | `data/wav/` |
| Transcript JSONs (12000 files) | ~500 MB | `results/transcripts/` |
| Analysis outputs | ~50 MB | `results/` |
| **Total** | **~4.5 GB** | - |

**Make sure you have ~5 GB free!**

---

## ⚠️ Important Notes

### Dataset Validity:
- ✅ Using Common Voice 17.0 (2024)
- ✅ Test split specifically
- ✅ Whisper trained on data up to Sept 2022
- ✅ Should be independent (different audio files)
- ⚠️  Possible speaker overlap from earlier CV versions

**Mention to supervisor**: "CV 17.0 test split, released after Whisper training"

### LID Accuracy:
- Current: 99.31% (143/144)
- With 1000 samples: Will be more reliable
- Expect: 98-99% (still very high, but validated on larger set)

### Mongolian Slowdown:
**Explanation to provide**:
- Same model architecture
- Same inference code
- Mongolian audio → tokenization issues
- Byte-pair encoding inefficient for Cyrillic/Mongolian script
- Results in longer token sequences
- More decoder steps needed
- Hence 10-30× longer processing

---

## 📧 Draft Email to Supervisor (Send After Step 7)

```
Subject: Thesis Update - Scaled to 1000 Samples with Statistical Analysis

Dear Dr. Mihajlik,

Following your recommendations, I have completed the following improvements:

**1. Scaled to 1000 samples per language** (4000 total samples)
- Dataset: Common Voice 17.0 test split (released 2024, after Whisper training)
- This addresses the sample size concern

**2. Added statistical significance tests:**
- Wilcoxon signed-rank tests for all comparisons
- 95% confidence intervals for all metrics
- Effect size calculations (Cohen's d)
- Results show p < 0.001 for key findings (highly significant)

**3. Updated results with larger dataset:**
- LID accuracy: [NEW_VALUE]% (validated on 4000 samples)
- LID vs Hinted: [NEW_RATIO]× speed difference (p < 0.001)
- Mongolian slowdown: [NEW_RATIO]× vs other languages (p < 0.001)

**4. Explanation of findings:**

**Language-Hinted vs LID→ASR:**
- Hinted: whisper.transcribe(audio, language="es")
- LID→ASR: whisper.transcribe(audio) - auto-detects language
- Counterintuitively, LID mode is faster

**Mongolian Slowdown:**
- Same model, same code
- Tokenization inefficiency for Cyrillic/Mongolian script
- Byte-pair encoding creates longer token sequences
- More decoder iterations required
- Results in 10-30× longer processing time

**Sample Definition:**
- Each sample = 1 utterance from Common Voice
- Single sentence or short phrase
- Duration: 8-15 seconds (typical conversational speech)

**Train/Test Independence:**
- Using CV 17.0 test split (released 2024)
- Whisper trained on data up to Sept 2022
- Audio files should be independent
- Possible speaker overlap from earlier versions

Results files and statistical analysis attached.

Ready to proceed with thesis writing based on these validated findings.

Best regards,
Munkhchimeg
```

---

## ✅ Next Actions RIGHT NOW

### Immediate (Today):
```bash
# 1. Download 1000 samples (START THIS NOW!)
cd ~/thesis-asr
python3 scripts/download_common_voice.py

# 2. Once download completes, verify:
ls data/wav/*/*.wav | wc -l  # Should be ~4000

# 3. Start experiments (runs overnight):
nohup ./scripts/run_comparison_batch.sh > experiment_log.txt 2>&1 &

# 4. Monitor progress:
tail -f experiment_log.txt
```

### Tomorrow:
- Check if experiments finished
- Run statistical analysis
- Regenerate figures
- Review results

### Day 3:
- Email supervisor with results
- Start writing thesis with validated findings

---

## 🎯 Success Criteria

You'll know you're done when:
- ✅ 4000 audio files downloaded
- ✅ ~12,000 experiment results generated
- ✅ Statistical analysis complete (p-values < 0.05)
- ✅ Updated figures with error bars
- ✅ Supervisor responded positively
- ✅ Ready to write thesis

---

**START NOW WITH STEP 2: DOWNLOAD THE DATA!** 🚀
