# ASR Model Comparison - Reproducibility Guide

Complete instructions to reproduce all experiments and results.

---

## 🔧 System Requirements

- **GPU:** NVIDIA GPU with 24GB+ VRAM (tested on RTX A6000)
- **CPU:** Multi-core processor (tested on Intel Xeon)
- **RAM:** 32GB+ recommended
- **Storage:** 100GB+ free space
- **OS:** Ubuntu 20.04+ (tested) or similar Linux distribution

---

## 📦 Environment Setup

### **1. Clone Repository**

```bash
git clone <your-repo-url>
cd thesis-asr
```

### **2. Install Conda** (if not already installed)

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### **3. Create Environment**

```bash
# Create environment from specification
conda env create -f environment.yml

# Activate environment
conda activate omni
```

### **4. Verify Installation**

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
python -c "import faster_whisper; print('Faster-Whisper: OK')"
```

---

## 📥 Dataset Preparation

### **1. Download Common Voice v23.0**

Download from Mozilla Common Voice Delta:
- Spanish: https://datacollective.mozillafoundation.org/ (search "Spanish")
- French: https://datacollective.mozillafoundation.org/ (search "French")
- Hungarian: https://datacollective.mozillafoundation.org/ (search "Hungarian")
- Mongolian: https://datacollective.mozillafoundation.org/datasets/cmflnuzw62lynu310rvwy9yod

Place tar.gz files in `~/cv-datasets/`

### **2. Extract Datasets**

```bash
mkdir -p ~/cv-datasets
cd ~/cv-datasets

tar -xzf mcv-scripted-es-v23.0.tar.gz
tar -xzf mcv-scripted-fr-v23.0.tar.gz
tar -xzf mcv-scripted-hu-v23.0.tar.gz
tar -xzf mcv-scripted-mn-v23.0.tar.gz
```

### **3. Prepare Test Dataset**

```bash
cd ~/thesis-asr

python scripts/prepare_v23_dataset.py \
  --cv-base ~/cv-datasets/cv-corpus-23.0-2025-09-05 \
  --output-base data \
  --num-samples 1000 \
  --langs es fr hu mn \
  --seed 42
```

**Expected output:**
- `data/wav/{lang}/` - 1000 audio files per language
- `data/ref/{lang}/` - 1000 reference transcripts per language

---

## 🚀 Running Experiments

### **Option 1: Run All Experiments (Recommended)**

```bash
# Single command to run all 4 models on all 4 languages
nohup bash scripts/run_all_models_v23.sh > run_all.log 2>&1 &

# Monitor progress
tail -f run_all.log

# Expected duration: 12-17 hours
```

### **Option 2: Run Models Individually**

**Whisper:**
```bash
for lang in mn hu es fr; do
    for audio_file in data/wav/$lang/*.mp3; do
        python scripts/run_whisper.py \
            --mode hinted \
            --model small \
            --device cpu \
            --infile "$audio_file" \
            --hint-lang $lang \
            --outdir results/transcripts
    done
done
```

**OmniLingual CTC 300M:**
```bash
for lang in mn hu es fr; do
    for audio_file in data/wav/$lang/*.mp3; do
        python scripts/run_omnilingual.py \
            --infile "$audio_file" \
            --hint-lang $lang \
            --model omniASR_CTC_300M \
            --save-json \
            --outdir results/transcripts/hinted/omnilingual/omniASR_CTC_300M/$lang
    done
done
```

*(Similar for CTC_1B and LLM_1B - see scripts/run_all_models_v23.sh)*

---

## 📊 Analysis & Metrics

### **1. Calculate WER/CER**

```bash
python scripts/calculate_wer_cer.py

# Outputs:
# - results/wer_cer_results.csv
# - results/wer_cer_results_summary.csv
```

### **2. Analyze Audio Durations**

```bash
python scripts/analyze_audio_durations.py \
  --audio-dir data/wav \
  --results-dir results \
  --output results/duration_analysis.csv

# Outputs:
# - results/duration_analysis.csv
# - results/duration_analysis_summary.csv
# - results/duration_analysis_distribution.csv
```

### **3. Test LID Accuracy**

```bash
bash scripts/test_lid_accuracy.sh

python scripts/analyze_lid_results.py \
  --results-dir results_lid_test \
  --output results/lid_accuracy.csv

# Outputs:
# - results/lid_accuracy.csv
# - results/lid_accuracy_summary.csv
# - results/lid_accuracy_confusion.csv
```

### **4. Profile Resource Usage**

```bash
python scripts/profile_resource_usage.py \
  --samples-per-lang 10 \
  --output results/resource_profiling.csv

# Output:
# - results/resource_profiling.csv
```

### **5. Generate Plots**

```bash
python scripts/plot_wer_speed_analysis.py

# Outputs:
# - results/plot5_wer_by_model_language.png
# - results/plot6_cer_by_model_language.png
# - results/plot7_speed_vs_accuracy.png
# - results/plot8_mongolian_detailed.png
```

---

## ✅ Expected Results

### **File Counts**

```bash
# Audio files
find data/wav -name "*.mp3" | wc -l  # Should be 4000

# References
find data/ref -name "*.txt" | wc -l  # Should be 4000

# Transcriptions
find results/transcripts -name "*.txt" | wc -l  # Should be 16000
find results/transcripts -name "*.json" | wc -l  # Should be 12000
```

### **Result Files**

```
results/
├── wer_cer_results.csv                    # 16000 rows (4 models × 4 langs × 1000)
├── wer_cer_results_summary.csv            # 16 rows (4 models × 4 langs)
├── duration_analysis.csv                  # Detailed duration analysis
├── duration_analysis_summary.csv          # Summary by bucket
├── duration_analysis_distribution.csv     # Overall statistics
├── lid_accuracy.csv                       # LID test results (400 samples)
├── lid_accuracy_summary.csv               # Per-language accuracy
├── lid_accuracy_confusion.csv             # Confusion matrix
├── resource_profiling.csv                 # Resource usage stats
└── plot*.png                              # Visualization plots
```

---

## 🔬 Validation

### **Verify Dataset Alignment**

```bash
# Check that audio and reference match
python -c "
from pathlib import Path
for lang in ['es', 'fr', 'hu', 'mn']:
    audio_files = set(f.stem for f in Path(f'data/wav/{lang}').glob('*.mp3'))
    ref_files = set(f.stem for f in Path(f'data/ref/{lang}').glob('*.txt'))
    assert audio_files == ref_files, f'{lang} mismatch!'
    print(f'{lang}: {len(audio_files)} files matched')
"
```

### **Verify WER/CER Calculation**

```bash
# Ensure reasonable WER/CER values (not > 200%)
python -c "
import pandas as pd
df = pd.read_csv('results/wer_cer_results_summary.csv')
print(df[['model', 'language', 'wer', 'cer']].describe())
assert df['wer'].max() < 2.0, 'WER too high - check alignment!'
"
```

---

## 🐳 Docker Container (Optional)

### **Build Container**

```bash
# Create Dockerfile (see Dockerfile in repo)
docker build -t thesis-asr .
```

### **Run Experiments in Container**

```bash
docker run --gpus all \
  -v $(pwd)/data:/workspace/data \
  -v $(pwd)/results:/workspace/results \
  thesis-asr bash scripts/run_all_models_v23.sh
```

---

## 📓 Jupyter Notebooks (Optional)

### **Start Jupyter**

```bash
conda activate omni
jupyter lab --port 8888

# Open analysis_notebook.ipynb
```

---

## 📋 Troubleshooting

### **CUDA Out of Memory**

```bash
# Run models sequentially instead of parallel
# Edit run_all_models_v23.sh to disable parallel execution
```

### **Missing Dependencies**

```bash
# Reinstall environment
conda env remove -n omni
conda env create -f environment.yml
conda activate omni
pip install faster-whisper
```

### **Slow Whisper Processing**

```bash
# Expected: ~40-60 seconds per file on CPU
# Use GPU for faster processing:
# Edit scripts to use --device cuda
```

---

## 📞 Support

For issues or questions:
- Check COMPLETE_EVALUATION_PLAN.md
- Review log files in `run_all.log`, `omni_*.log`
- Verify environment: `conda list`

---

## 📄 Citation

If you use this code, please cite:

```bibtex
@mastersthesis{thesis2025,
  author = {Your Name},
  title = {Comparative Analysis of Multilingual ASR Systems},
  school = {Your University},
  year = {2025}
}
```

---

## ✅ Reproducibility Checklist

- [ ] Environment created from environment.yml
- [ ] Datasets downloaded and extracted
- [ ] Data prepared with fixed seed (--seed 42)
- [ ] All 4 models run on all 4 languages
- [ ] WER/CER calculated successfully
- [ ] All analysis scripts executed
- [ ] Plots generated
- [ ] Results validated (file counts, value ranges)
- [ ] Documentation reviewed

**All steps complete = Fully reproducible!** ✅
