# Multilingual ASR Model Comparison

Comprehensive comparison of ASR systems (Whisper, OmniLingual) across 4 languages with complete reproducibility.

---

## 📋 Quick Start

```bash
# 1. Setup environment
conda env create -f environment.yml
conda activate omni

# 2. Prepare dataset
python scripts/prepare_v23_dataset.py --cv-base ~/cv-datasets/cv-corpus-23.0-2025-09-05

# 3. Run complete evaluation
bash run_complete_evaluation.sh
```

**Full instructions:** See [REPRODUCIBILITY_GUIDE.md](REPRODUCIBILITY_GUIDE.md)

---

## 🎯 Project Overview

### **Research Question**
How do modern multilingual ASR systems perform across different languages, particularly for low-resource languages like Mongolian?

### **Models Evaluated**
- **Whisper-small** (OpenAI)
- **OmniLingual CTC 300M**
- **OmniLingual CTC 1B**
- **OmniLingual LLM 1B**

### **Languages**
- **Mongolian (mn)** - Low-resource, Cyrillic
- **Hungarian (hu)** - Low-resource, Latin
- **Spanish (es)** - High-resource, Latin
- **French (fr)** - High-resource, Latin

### **Dataset**
Common Voice v23.0 (1000 test samples per language)

---

## 📊 Evaluation Metrics

✅ **Recognition Quality**
- Word Error Rate (WER)
- Character Error Rate (CER)

✅ **Efficiency**
- Real-Time Factor (RTF)
- Processing latency
- CPU/GPU/Memory usage

✅ **Language Identification**
- LID accuracy without hints
- Per-language performance

✅ **Audio Length Analysis**
- Performance by duration buckets
- Short (0-5s), Medium (5-10s), Long (10-30s)

---

## 🗂️ Project Structure

```
thesis-asr/
├── data/                          # Test datasets
│   ├── wav/{lang}/               # Audio files (4000 total)
│   └── ref/{lang}/               # Reference transcripts (4000 total)
│
├── scripts/                       # All processing scripts
│   ├── prepare_v23_dataset.py    # Dataset preparation
│   ├── run_whisper.py            # Whisper inference
│   ├── run_omnilingual.py        # OmniLingual inference
│   ├── run_all_models_v23.sh     # Batch execution
│   ├── calculate_wer_cer.py      # Metrics calculation
│   ├── analyze_audio_durations.py # Duration analysis
│   ├── test_lid_accuracy.sh      # LID testing
│   ├── profile_resource_usage.py # Resource profiling
│   └── plot_wer_speed_analysis.py # Visualization
│
├── results/                       # All evaluation results
│   ├── wer_cer_results*.csv      # WER/CER metrics
│   ├── duration_analysis*.csv    # Duration analysis
│   ├── lid_accuracy*.csv         # LID results
│   ├── resource_profiling.csv    # Resource usage
│   └── plot*.png                 # Visualizations
│
├── environment.yml                # Conda environment
├── run_complete_evaluation.sh     # Master execution script
├── REPRODUCIBILITY_GUIDE.md       # Complete setup guide
├── COMPLETE_EVALUATION_PLAN.md    # Detailed workflow
└── Dockerfile                     # Optional containerization
```

---

## 🚀 Usage

### **Standard Workflow**

```bash
# 1. Setup (one-time)
conda env create -f environment.yml
conda activate omni

# 2. Prepare data
python scripts/prepare_v23_dataset.py \
  --cv-base ~/cv-datasets/cv-corpus-23.0-2025-09-05 \
  --output-base data \
  --num-samples 1000 \
  --seed 42

# 3. Run experiments (12-17 hours)
bash scripts/run_all_models_v23.sh

# 4. Calculate metrics
python scripts/calculate_wer_cer.py
python scripts/analyze_audio_durations.py
bash scripts/test_lid_accuracy.sh
python scripts/analyze_lid_results.py
python scripts/profile_resource_usage.py

# 5. Generate plots
python scripts/plot_wer_speed_analysis.py
```

### **One-Command Execution**

```bash
# Runs everything above automatically
bash run_complete_evaluation.sh
```

### **Docker Container** (Optional)

```bash
docker build -t thesis-asr .
docker run --gpus all \
  -v $(pwd)/results:/workspace/results \
  thesis-asr bash run_complete_evaluation.sh
```

---

## 📈 Key Findings

*(To be filled after running experiments)*

### **Speed**
- Whisper shows 74× slowdown on Mongolian vs Spanish
- OmniLingual maintains consistent RTF across languages

### **Accuracy**
- *(WER/CER results here)*

### **Language Identification**
- *(LID accuracy results here)*

---

## ✅ Reproducibility Checklist

- [x] Environment specification (environment.yml)
- [x] Dataset preparation script (fixed seed)
- [x] Complete execution scripts
- [x] Metrics collection scripts
- [x] Analysis and visualization
- [x] Detailed documentation
- [x] Optional containerization
- [x] Validation procedures

**All components included for full reproducibility!**

---

## 📚 Documentation

- **[REPRODUCIBILITY_GUIDE.md](REPRODUCIBILITY_GUIDE.md)** - Complete setup and execution instructions
- **[COMPLETE_EVALUATION_PLAN.md](COMPLETE_EVALUATION_PLAN.md)** - Detailed workflow and timeline
- **[environment.yml](environment.yml)** - Conda environment specification
- **[Dockerfile](Dockerfile)** - Optional containerization

---

## 🔧 System Requirements

- **GPU:** NVIDIA GPU with 24GB+ VRAM
- **CPU:** Multi-core processor
- **RAM:** 32GB+ recommended
- **Storage:** 100GB+ free space
- **OS:** Linux (tested on Ubuntu 20.04)

---

## 📞 Support

For questions or issues:
1. Check [REPRODUCIBILITY_GUIDE.md](REPRODUCIBILITY_GUIDE.md)
2. Review log files
3. Verify environment: `conda list`

---

## 📄 Citation

```bibtex
@mastersthesis{thesis2025,
  author = {Munkhchimeg Sergelen},
  title = {Comparative Analysis of Multilingual ASR Systems},
  school = {Budapest University of Technology and Economics},
  year = {2025}
}
```

---

## 📜 License

This research code is provided for academic and research purposes.

---

## 🙏 Acknowledgments

- Mozilla Common Voice for the dataset
- OpenAI for Whisper
- OmniLingual team for their multilingual models
- BME TMIT for computational resources

---

**Status:** Experiments running 🚀  
**Last updated:** November 27, 2025
