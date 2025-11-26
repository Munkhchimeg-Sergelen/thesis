# ASR Model Comparison Plots

This folder contains all plots and statistics for the thesis comparing Whisper and OmniLingual ASR models.

## Generated: November 26, 2025

---

## 📊 Plots

### **plot1_rtf_by_language.png**
**Real-Time Factor (RTF) by Model and Language**
- Bar chart comparing RTF across 4 languages (MN, HU, ES, FR)
- Shows 4 models: Whisper-small, OmniASR_CTC_300M, OmniASR_CTC_1B, OmniASR_LLM_1B
- Red dashed line indicates real-time threshold (RTF=1.0)
- Lower is better (faster processing)

**Key Finding:** Whisper is extremely slow on Mongolian (RTF ~37), while OmniLingual models maintain consistent speed across all languages (RTF 0.014-0.51)

---

### **plot2_processing_time_avg.png**
**Average Processing Time by Model**
- Bar chart with error bars (standard deviation)
- Log scale Y-axis for better visualization
- Shows mean processing time in seconds per audio file

**Key Finding:** OmniLingual CTC models are 600x faster than Whisper-small

---

### **plot3_rtf_distribution_boxplot.png**
**RTF Distribution by Model (Log Scale)**
- Box plots showing distribution, median, and outliers
- Log scale reveals differences between fast models
- Shows consistency/variability of each model

---

### **plot4_rtf_by_language_violin.png**
**RTF Distribution by Language (All Models Combined)**
- Violin plots showing distribution shape
- Compares languages: MN, HU, ES, FR
- Shows mean and median markers

---

## 📈 Statistics Files

### **whisper_omnilingual_overall.csv**
Overall statistics per model:
- Mean RTF
- Mean processing time
- Standard deviations

### **whisper_omnilingual_statistics.csv**
Detailed statistics per model AND language:
- RTF (mean, std, median)
- Processing time (mean, std)
- Audio duration (mean)

---

## 🔢 Key Statistics Summary

| Model | Avg RTF | Avg Time (s) | Speed vs Whisper |
|-------|---------|--------------|------------------|
| **Whisper-small** | 9.89 | 49.77 | 1x (baseline) |
| **OmniASR_CTC_300M** | 0.016 | 0.067 | **618x faster** ⚡ |
| **OmniASR_CTC_1B** | 0.022 | 0.093 | **450x faster** |
| **OmniASR_LLM_1B** | 0.476 | 2.020 | **25x faster** |

---

## 📊 Dataset

- **Total transcriptions analyzed:** 16,000
- **Models tested:** 4
- **Languages:** Mongolian (mn), Hungarian (hu), Spanish (es), French (fr)
- **Files per model/language:** 1,000
- **Source:** Common Voice dataset (test split)

---

## 🎯 Major Findings

1. **Mongolian Performance Gap:** Whisper-small shows severe degradation on Mongolian (RTF 36.98 vs 0.50 for Spanish) - likely due to Cyrillic script and low-resource language status

2. **OmniLingual Consistency:** Modern multilingual models maintain consistent performance across all languages, demonstrating better multilingual support

3. **Speed-Architecture Tradeoff:**
   - CTC models: Ultra-fast parallel decoding
   - LLM models: Slower but potentially more accurate with language conditioning

4. **Real-time Capability:**
   - ✅ All OmniLingual models run faster than real-time (RTF < 1.0)
   - ❌ Whisper-small cannot process Mongolian in real-time on CPU

---

## 📝 Usage in Thesis

These plots demonstrate:
- Performance comparison across multiple ASR architectures
- Language-specific processing challenges
- Trade-offs between model size, architecture, and speed
- Importance of multilingual training data for low-resource languages

Include in thesis sections:
- **Methods:** Model specifications and evaluation metrics
- **Results:** Performance analysis with plots
- **Discussion:** Language-specific findings and architectural implications
