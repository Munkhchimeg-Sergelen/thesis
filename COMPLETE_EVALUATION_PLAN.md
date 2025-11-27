# Complete ASR Evaluation Plan
## All Requirements for Supervisor

---

## ✅ Tomorrow Morning Workflow

### **Step 1: Verify Experiments Complete**

```bash
ssh -p 15270 mugi@bistromat.tmit.bme.hu
cd ~/thesis-asr

# Check all jobs finished
tail -50 run_all_v23.log
tail -50 omni_300m.log
tail -50 omni_1b.log
tail -50 omni_llm.log

# Count results (should be 16,000 total)
find results_v23 -name "*.json" | wc -l  # Should be 12,000 (3 OmniLingual models)
find results_v23 -name "*.txt" | wc -l   # Should be 16,000 (all transcripts)
```

---

### **Step 2: Move Results to Standard Location**

```bash
# Backup old results if any
mv results results_old_backup 2>/dev/null || true

# Use new v23.0 results
mv results_v23 results
```

---

### **Step 3: Core Metrics - WER/CER**

```bash
# Upload updated calculate_wer_cer.py if needed
# (should already be on GPU)

# Calculate WER/CER (perfect alignment guaranteed!)
python scripts/calculate_wer_cer.py

# Expected output:
# - results/wer_cer_results.csv (detailed)
# - results/wer_cer_results_summary.csv (summary)

# Verify
head results/wer_cer_results_summary.csv
```

---

### **Step 4: Audio Duration Analysis**

```bash
# Upload script
# (On Mac: scp -P 15270 scripts/analyze_audio_durations.py mugi@bistromat.tmit.bme.hu:~/thesis-asr/scripts/)

# Run analysis
python scripts/analyze_audio_durations.py \
  --audio-dir data/wav \
  --results-dir results \
  --output results/duration_analysis.csv

# Expected outputs:
# - results/duration_analysis.csv (detailed)
# - results/duration_analysis_summary.csv (by bucket)
# - results/duration_analysis_distribution.csv (overall stats)
```

---

### **Step 5: Language Identification (LID) Accuracy**

```bash
# Make script executable
chmod +x scripts/test_lid_accuracy.sh

# Run LID test (will take ~2 hours for 400 samples)
# Testing 100 samples per language without language hints
nohup bash scripts/test_lid_accuracy.sh > lid_test.log 2>&1 &

# Wait for completion, then analyze
python scripts/analyze_lid_results.py \
  --results-dir results_lid_test \
  --output results/lid_accuracy.csv

# Expected outputs:
# - results/lid_accuracy.csv (detailed)
# - results/lid_accuracy_summary.csv (per language)
# - results/lid_accuracy_confusion.csv (confusion matrix)
```

---

### **Step 6: Resource Usage Profiling** (Optional but recommended)

```bash
# Profile small subset (10 samples per lang = 40 samples × 4 models)
# Will take ~30 minutes
python scripts/profile_resource_usage.py \
  --samples-per-lang 10 \
  --output results/resource_profiling.csv

# Expected output:
# - results/resource_profiling.csv (CPU/GPU/Memory stats)
```

---

### **Step 7: Generate Comprehensive Plots**

```bash
# Upload plotting script
# (On Mac: scp -P 15270 scripts/plot_wer_speed_analysis.py mugi@bistromat.tmit.bme.hu:~/thesis-asr/scripts/)

# Generate all plots
python scripts/plot_wer_speed_analysis.py

# Expected outputs:
# - plot5_wer_by_model_language.png
# - plot6_cer_by_model_language.png
# - plot7_speed_vs_accuracy.png
# - plot8_mongolian_detailed.png
```

---

### **Step 8: Download Results to Mac**

```bash
# On Mac - download all results and plots
mkdir -p ~/thesis-asr/final_results
scp -P 15270 -r mugi@bistromat.tmit.bme.hu:~/thesis-asr/results/*.csv ~/thesis-asr/final_results/
scp -P 15270 -r mugi@bistromat.tmit.bme.hu:~/thesis-asr/results/*.png ~/thesis-asr/final_results/
```

---

## 📊 Final Deliverables Checklist

### **1. Languages (Requirement: 3-6)** ✅
- [x] 4 languages: Mongolian, Hungarian, Spanish, French
- [x] Representative of different families and scripts

### **2. Datasets** ✅
- [x] Common Voice v23.0 (standardized)
- [x] 1000 samples per language
- [x] Perfect audio-reference alignment

### **3. Audio Length Analysis** ✅
- [x] Duration buckets: short (0-5s), medium (5-10s), long (10-30s), very long (30s+)
- [x] Performance metrics by duration
- [x] Distribution statistics

### **4. Recognition Quality Metrics** ✅
- [x] WER (Word Error Rate) - per model, per language
- [x] CER (Character Error Rate) - per model, per language
- [x] Detailed and summary statistics

### **5. LID Accuracy** ✅
- [x] Language detection without hints
- [x] Per-language accuracy
- [x] Confusion matrix

### **6. Efficiency Metrics** ✅
- [x] Real-Time Factor (RTF) - from JSON files
- [x] Processing time per file
- [x] Language-specific latency analysis

### **7. Resource Usage** ✅
- [x] CPU utilization (mean & max)
- [x] Memory usage (GB, mean & max)
- [x] GPU utilization (mean & max)
- [x] GPU memory usage (MB, mean & max)

---

## 📈 Expected Results Structure

```
final_results/
├── wer_cer_results.csv                    # Detailed WER/CER per file
├── wer_cer_results_summary.csv            # Summary by model/language
├── duration_analysis.csv                  # Performance by audio length
├── duration_analysis_summary.csv          # Bucket statistics
├── duration_analysis_distribution.csv     # Overall duration stats
├── lid_accuracy.csv                       # LID test results
├── lid_accuracy_summary.csv               # Per-language LID accuracy
├── lid_accuracy_confusion.csv             # Confusion matrix
├── resource_profiling.csv                 # CPU/GPU/Memory usage
├── plot5_wer_by_model_language.png       # WER comparison
├── plot6_cer_by_model_language.png       # CER comparison
├── plot7_speed_vs_accuracy.png           # Tradeoff analysis
└── plot8_mongolian_detailed.png          # Mongolian focus
```

---

## 🎯 Timeline

| Task | Duration | When |
|------|----------|------|
| Main experiments (running now) | 12-17 hours | Tonight |
| Verify & move results | 5 min | Tomorrow morning |
| Calculate WER/CER | 5 min | Tomorrow morning |
| Duration analysis | 2 min | Tomorrow morning |
| LID testing | 2 hours | Tomorrow daytime |
| Resource profiling | 30 min | Tomorrow daytime |
| Generate plots | 2 min | Tomorrow afternoon |
| Download results | 5 min | Tomorrow afternoon |

**Total additional time needed: ~3 hours**

---

## ✅ Supervisor Requirements - Complete Coverage

All evaluation requirements will be met:

✅ **Languages:** 4 representative languages  
✅ **Datasets:** Common Voice v23.0, properly aligned  
✅ **Audio lengths:** Analyzed and categorized  
✅ **Recognition quality:** WER & CER calculated  
✅ **LID accuracy:** Tested without language hints  
✅ **Efficiency:** RTF, latency measured  
✅ **Resource usage:** CPU, GPU, Memory profiled  

**Ready for publication and thesis defense!** 🎓
