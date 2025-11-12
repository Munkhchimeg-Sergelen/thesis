# Analysis of Multilingual Automatic Speech Recognition Approaches

**BSc Thesis** | Budapest University of Technology and Economics  
**Author**: Munkhchimeg Sergelen  
**Supervisor**: Dr. Mihajlik Péter  
**Department**: Department of Telecommunications and Media Informatics  
**Date**: November 2025

---

## 📋 Abstract

This thesis evaluates two multilingual ASR approaches: **LID→ASR** (automatic language identification followed by transcription) versus **language-hinted ASR** (where language is explicitly provided). Through 312 controlled experiments across 4 languages (Spanish, French, Hungarian, Mongolian), we discovered that:

- 🎯 **Whisper's LID achieves 99.31% accuracy** - production-ready performance
- ⚡ **LID→ASR is 2.76× faster** than language-hinted mode (surprising!)
- 🇲🇳 **Mongolian processes 10-30× slower** than other languages (critical inequality)
- 📊 **Model size scaling**: 6× speed difference between tiny and small models
- 🏆 **Whisper dominates** multilingual scenarios over language-specific models

---

## 🔬 Research Questions

1. **How accurate is automatic language identification for multilingual ASR?**  
   → 99.31% - near-perfect across all tested languages

2. **How does processing efficiency compare between LID→ASR and language-hinted approaches?**  
   → LID→ASR is 2.76× faster (6.80s vs 18.78s average)

3. **How do different Whisper model sizes compare in processing efficiency?**  
   → 6× speed difference (tiny: 2.28s, small: 13.80s)

4. **How does multilingual ASR performance vary across languages?**  
   → Mongolian 10-30× slower than Spanish/French/Hungarian

5. **How do different ASR systems compare for multilingual deployment?**  
   → Whisper better for multilingual use (built-in LID, broader coverage)

---

## 🚀 Quick Start

### Prerequisites

```bash
# Create conda environment
conda create -n asr-env python=3.10
conda activate asr-env

# Install dependencies
pip install faster-whisper transformers torch librosa soundfile numpy pandas matplotlib seaborn
```

### Running Evaluations

```bash
# 1. Language-Hinted Mode (168 experiments)
./scripts/run_full_evaluation.sh

# 2. LID→ASR Mode (144 experiments)
./scripts/run_lid_evaluation.sh

# 3. Analyze Results
python scripts/analyze_results.py
python scripts/analyze_lid_accuracy.py
python scripts/compare_lid_vs_hinted.py

# 4. Generate Plots
python scripts/create_plots.py
```

---

## 📊 Key Results

### Language Identification Accuracy

| Language   | Accuracy | Samples | Errors |
|------------|----------|---------|--------|
| Spanish    | 100.0%   | 36      | 0      |
| French     | 100.0%   | 36      | 0      |
| Hungarian  | 97.22%   | 36      | 1      |
| Mongolian  | 100.0%   | 36      | 0      |
| **Overall** | **99.31%** | **144** | **1** |

### Processing Time Comparison

| Mode                 | Mean (s) | Speedup |
|----------------------|----------|---------|
| LID→ASR             | 6.80     | 2.76×   |
| Language-Hinted     | 18.78    | 1.0×    |

### Model Size Impact

| Model  | Parameters | Mean Time (s) | Speed vs Tiny |
|--------|------------|---------------|---------------|
| Tiny   | 39M        | 2.28          | 1.0×          |
| Base   | 74M        | 4.31          | 1.89×         |
| Small  | 244M       | 13.80         | 6.05×         |

### Language-Specific Performance

| Language   | Mean (s) | Std Dev (s) | Slowdown vs Spanish |
|------------|----------|-------------|---------------------|
| Spanish    | 2.56     | 1.80        | 1.0×                |
| French     | 2.80     | 1.97        | 1.09×               |
| Hungarian  | 3.27     | 2.26        | 1.28×               |
| **Mongolian** | **30.56** | **32.02** | **11.9×** ⚠️ |

---

## 📁 Repository Structure

```
thesis-asr/
├── data/
│   └── wav/                          # Audio test files (not included)
│       ├── es/                       # Spanish samples
│       ├── fr/                       # French samples
│       ├── hu/                       # Hungarian samples
│       └── mn/                       # Mongolian samples
├── docs/
│   └── thesis_materials/             # Thesis chapters
│       ├── 00_abstract.md
│       ├── 01_introduction.md
│       ├── 02_background.md
│       ├── 01_methods_hardware.md
│       ├── 02_methods_systems.md
│       ├── 03_results.md
│       ├── 05_discussion.md
│       ├── 06_conclusions.md
│       ├── 10_bibliography.md
│       └── figures/                  # Generated plots
├── scripts/
│   ├── run_whisper.py                # Whisper inference
│   ├── run_wav2vec2.py               # Wav2Vec2 inference
│   ├── run_full_evaluation.sh        # Hinted mode evaluation
│   ├── run_lid_evaluation.sh         # LID mode evaluation
│   ├── analyze_results.py            # Statistical analysis
│   ├── analyze_lid_accuracy.py       # LID accuracy metrics
│   ├── compare_lid_vs_hinted.py      # Mode comparison
│   └── create_plots.py               # Generate figures
├── results/
│   ├── transcripts/                  # Raw transcription outputs
│   │   ├── hinted/                   # Language-hinted results
│   │   └── lid2asr/                  # LID→ASR results
│   └── analysis/                     # Analysis outputs
│       ├── summary.txt
│       ├── mode_comparison_report.txt
│       ├── lid_accuracy_summary.txt
│       └── *.csv                     # Detailed statistics
└── README.md                         # This file
```

---

## 🔄 Reproducing Results

### Step 1: Obtain Test Data

Download Mozilla Common Voice v11.0 test set:
```bash
# Spanish
wget https://mozilla-common-voice-datasets.s3.amazonaws.com/cv-corpus-11.0-2022-09-21/cv-corpus-11.0-2022-09-21-es.tar.gz

# French, Hungarian, Mongolian (similar URLs)
```

Extract 12 samples per language to `data/wav/{lang}/`

### Step 2: Run Evaluations

```bash
# Activate environment
conda activate asr-env

# Run hinted mode (3 hours)
./scripts/run_full_evaluation.sh

# Run LID mode (2-3 hours)
./scripts/run_lid_evaluation.sh
```

### Step 3: Analyze & Plot

```bash
# Generate all analysis files
python scripts/analyze_results.py
python scripts/analyze_lid_accuracy.py
python scripts/compare_lid_vs_hinted.py
python scripts/create_plots.py
```

Results will be in `results/analysis/` and `docs/thesis_materials/figures/`

---

## 📊 Generated Outputs

### Analysis Files

- `results/analysis/summary.txt` - Quick overview
- `results/analysis/overall_statistics.csv` - Aggregated stats
- `results/analysis/whisper_model_comparison.csv` - Model scaling
- `results/analysis/language_analysis.csv` - Language performance
- `results/analysis/lid_accuracy_summary.txt` - LID metrics
- `results/analysis/lid_confusion_matrix.csv` - LID errors
- `results/analysis/mode_comparison_report.txt` - **Core finding!**

### Figures

- `whisper_model_comparison.png/pdf` - Model size comparison
- `system_comparison.png/pdf` - Whisper vs Wav2Vec2
- `language_comparison.png/pdf` - Performance by language
- `processing_time_dist.png/pdf` - Processing time distribution
- `summary_table.png` - Summary statistics table

---

## 🎯 Key Contributions

1. **First systematic evaluation of Whisper's LID capability** (99.31% accuracy)
2. **Discovery that LID→ASR is faster than hinted mode** (2.76× speedup)
3. **Quantification of low-resource language performance gap** (Mongolian 10-30× slower)
4. **Deployment-focused evaluation methodology** (efficiency metrics, not just WER)
5. **Fully reproducible framework** with open-source scripts

---

## 💡 Practical Recommendations

### For Practitioners:

✅ **Use LID→ASR by default** - Faster AND 99% accurate  
✅ **Choose model size based on constraints**:
  - Real-time applications: Whisper-tiny (2.28s avg)
  - Batch processing: Whisper-small (13.80s avg)
  - Balanced: Whisper-base (4.31s avg)

⚠️ **Avoid Whisper-small for low-resource languages** - Use tiny/base instead  
⚠️ **Test all target languages before deployment** - Performance varies 10-30×  
⚠️ **Implement timeout mechanisms** - Protect against 151s worst-case slowdowns

### For Researchers:

✅ **Evaluate low-resource languages explicitly** - Don't assume universal models work universally  
✅ **Report efficiency metrics** - WER alone insufficient for deployment  
✅ **Test LID accuracy** - Don't assume it works, measure it  
✅ **Document worst-case behavior** - Report max latency, not just mean

---

## ⚠️ Limitations

- **No WER/CER metrics**: Lack of reference transcripts (future work)
- **CPU-only evaluation**: GPU failed due to cuDNN compatibility
- **Limited audio characteristics**: Only ~10-15s clean clips
- **Small sample size**: 12 samples per language per model
- **Limited language coverage**: 4 of 99 Whisper-supported languages

All limitations acknowledged and discussed in thesis.

---

## 🔮 Future Work

### Immediate Extensions:
- Add WER/CER evaluation with reference transcripts
- Resolve GPU cuDNN issues for GPU evaluation
- Test broader language coverage (10-20 languages)
- Evaluate varying audio lengths (5s, 15s, 60s+)

### Advanced Research:
- Root cause analysis of Mongolian slowdown
- Investigation of LID speed advantage mechanism
- Code-switching evaluation
- Long-form audio strategies
- Low-resource language optimization
- Noisy audio robustness testing

---

## 📚 Citation

If you use this work, please cite:

```bibtex
@mastersthesis{sergelen2025multilingual,
  title={Analysis of Multilingual Automatic Speech Recognition Approaches},
  author={Sergelen, Munkhchimeg},
  year={2025},
  school={Budapest University of Technology and Economics},
  type={Bachelor's Thesis},
  supervisor={Dr. Mihajlik Péter}
}
```

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **Dr. Mihajlik Péter** - Thesis supervisor
- **OpenAI** - Whisper model
- **Facebook AI** - Wav2Vec2-XLSR-53 model
- **Mozilla** - Common Voice dataset
- **Budapest University of Technology and Economics** - Resources and support

---

## 📧 Contact

**Munkhchimeg Sergelen**  
Budapest University of Technology and Economics  
Department of Telecommunications and Media Informatics

For questions about this thesis, please contact via GitHub issues.

---

## 📊 Thesis Status

- ✅ **312 experiments completed** (100% success rate)
- ✅ **All 5 research questions answered**
- ✅ **2 surprising discoveries** (LID speed, Mongolian slowdown)
- ✅ **51 pages written**
- ✅ **5 publication-quality plots generated**
- ✅ **Ready for submission** (November 2025)

---

**Last Updated**: November 12, 2025  
**Thesis Defense**: TBD  
**Status**: 95% Complete - Polishing Phase
