# Baseline Results: Whisper-small (CPU)

**Date**: October 24, 2025  
**System**: OpenAI Whisper-small  
**Hardware**: CPU (WSL/Linux)  
**Status**: ✅ Complete

---

## Executive Summary

This document captures the baseline evaluation of Whisper-small across 4 languages (MN, HU, FR, ES) in two inference modes:
1. **Language-Hinted** (oracle, language explicitly provided)
2. **LID→ASR** (language auto-detected, then transcription)

### Key Findings

✅ **Spanish and French**: Good performance (WER 0.13-0.47)  
⚠️ **Hungarian**: Moderate difficulty (WER 0.79-0.85)  
❌ **Mongolian**: Poor performance (WER 1.03-1.48, often >1.0)

🎯 **LID Impact**: Minimal difference between hinted vs LID→ASR for well-detected languages  
⚠️ **LID Weakness**: Low confidence for MN (72.7% acc) and HU (83.3% acc)

---

## 1. Recognition Quality (WER/CER)

### Summary Table

| Language | Mode | WER Mean | CER Mean | n | Interpretation |
|----------|------|----------|----------|---|----------------|
| **ES** (Spanish) | hinted | 0.172 | 0.049 | 20 | Excellent |
| ES | lid2asr | 0.189 | 0.055 | 10 | Excellent |
| ES | sweep | 0.135 | 0.029 | 30 | Excellent |
| **FR** (French) | hinted | 0.425 | 0.213 | 20 | Good |
| FR | lid2asr | 0.410 | 0.205 | 10 | Good |
| FR | sweep | 0.467 | 0.211 | 30 | Good |
| **HU** (Hungarian) | hinted | 0.850 | 0.446 | 20 | Poor |
| HU | lid2asr | 0.807 | 0.444 | 6 | Poor |
| HU | sweep | 0.790 | 0.318 | 30 | Poor |
| **MN** (Mongolian) | hinted | 1.036 | 0.947 | 20 | Very Poor |
| MN | lid2asr | 1.026 | 0.976 | 6 | Very Poor |
| MN | sweep | 1.479 | 1.392 | 30 | Very Poor |

**Notes**:
- WER > 1.0 indicates more errors than words in reference (heavy hallucination/substitution)
- "sweep" mode combines multiple decoding parameter sets
- Sample sizes vary due to LID failures (see Section 2)

### Observations

1. **Language Resource Effect**: Well-resourced languages (ES, FR) perform significantly better than low-resource languages (MN)

2. **Morphological Complexity**: Hungarian's agglutinative nature contributes to higher WER despite being Latin-script

3. **Mode Comparison**: 
   - Hinted vs LID→ASR differences are small (<5% WER delta)
   - When LID is correct, performance is nearly identical
   - Bottleneck is the ASR model, not the language hint

4. **Mongolian Failure**: 
   - WER >1.0 suggests model may be hallucinating or using wrong script
   - Whisper-small likely undertrained on Cyrillic/Mongolian data

---

## 2. Language Identification (LID)

### Accuracy by Language

| Language | Total | Correct | Accuracy | Low Conf (<0.60) | Median Prob |
|----------|-------|---------|----------|------------------|-------------|
| **ES** | 11 | 10 | **90.9%** | 1 | 0.980 |
| **FR** | 11 | 10 | **90.9%** | 1 | 0.989 |
| **HU** | 12 | 10 | **83.3%** | 5 | 0.689 |
| **MN** | 11 | 8 | **72.7%** | 8 | 0.552 |

### Observations

1. **High Confidence Languages**: FR and ES have median probabilities >0.98
   - LID failures are rare (<10%)
   - Model is confident in predictions

2. **Uncertain Languages**: HU and MN show low confidence
   - MN median probability 0.55 (barely better than random for 2 classes!)
   - 73% of MN clips flagged as low-confidence

3. **Failure Mode**: When LID fails, it impacts the LID→ASR pipeline
   - Wrong language → wrong phoneme set → cascading errors
   - This explains reduced sample size for MN/HU in lid2asr mode

4. **Short Audio Challenge**: All clips are 10-30s; LID may improve with longer context (test needed)

### LID Confusion Matrix

**Source**: `results/most_relevant/lid_confusion.csv`

*(Note: Full confusion matrix to be added after detailed analysis)*

---

## 3. Efficiency Metrics

### Real-Time Factor (RTF)

**Source**: Plot `docs/figs/rtf_by_lang.png`

- **Typical RTF**: 0.4-1.7 (varies by audio length)
- **Interpretation**: 
  - RTF <1.0: System processes faster than real-time (streaming viable)
  - RTF ~1.7: Slower than real-time for shortest clips (overhead-dominated)

**Key Finding**: CPU inference is near or below real-time for most cases, making it viable for batch processing but marginal for live streaming.

### Resource Usage

**Sample Data** (from `run_summary.csv`):
- **CPU Average**: ~0-5% (varies with system load; measurement may be incomplete)
- **RSS Peak**: ~1.7 MB (likely underestimated; check measurement tool)

⚠️ **Data Quality Issue**: CPU/memory measurements appear incomplete. Need to verify `scripts/measure_perf.py` implementation.

---

## 4. Data Summary

### Languages & Rationale

| Language | Code | Script | Resource Level | Why Selected |
|----------|------|--------|----------------|--------------|
| Mongolian | MN | Cyrillic | Low | Test low-resource, non-Latin script |
| Hungarian | HU | Latin | Medium | Test agglutinative morphology |
| French | FR | Latin | High | Well-resourced baseline |
| Spanish | ES | Latin | High | Well-resourced baseline |

### Audio Characteristics

- **Format**: 16kHz mono WAV (normalized via `scripts/normalize_audio.sh`)
- **Length**: Primarily 10-30s clips
- **Missing**: No 120s clips yet (required by thesis)
- **Sources**: *(Document datasets used)*

---

## 5. Experimental Setup

### System Configuration

- **Model**: `openai/whisper-small` (~244M parameters)
- **Device**: CPU
- **OS**: WSL/Linux
- **Conda Env**: `asr-env` (see `env/asr-env-wsl.yml`, `env/asr-env-freeze.txt`)

### Inference Modes

1. **Language-Hinted** (`make run_whisper_hinted`)
   ```bash
   python scripts/run_whisper.py --mode hinted --model small \
     --device cpu --hint-lang <LANG> --infile <FILE>
   ```

2. **LID→ASR** (`make run_whisper_lid`)
   ```bash
   python scripts/run_whisper.py --mode lid2asr --model small \
     --device cpu --infile <FILE>
   ```

### Evaluation Pipeline

1. **Transcription**: `scripts/run_whisper.py`
2. **LID**: `scripts/lid_from_whisper.py`
3. **Metrics**: `scripts/eval_metrics.py` (WER/CER)
4. **Performance**: `scripts/measure_perf.py` (RTF, CPU, memory)
5. **Aggregation**: `scripts/run_summary.py`

---

## 6. Artifacts & Reproducibility

### Key Files

- **Metrics**: `results/most_relevant/wer_cer_summarized.csv`
- **LID**: `results/most_relevant/lid_accuracy.csv`
- **Plots**: 
  - `docs/figs/lid_acc_by_lang.png`
  - `docs/figs/rtf_by_lang.png`
- **Environment**: 
  - `env/asr-env-wsl.yml` (conda spec)
  - `env/asr-env-freeze.txt` (pip freeze)
- **Commands**: `docs/appendix_commands.md`

### Reproducibility Checklist

- [x] Conda environment documented
- [x] Audio normalization script provided
- [x] Makefile with all run commands
- [x] Metrics computation scripts
- [x] Results CSV files committed
- [ ] Dataset sources documented (TODO)
- [ ] Full hardware specs documented (TODO)

---

## 7. Known Issues & Limitations

### Current Limitations

1. **Audio Length**: Only 10-30s clips tested; need 120s for thesis requirement
2. **Single System**: Only Whisper evaluated; thesis requires ≥2 systems
3. **No GPU Data**: All runs on CPU; GPU comparison pending
4. **Limited Data**: Small sample sizes (n=6-30 per condition)
5. **Measurement Gaps**: CPU/memory metrics incomplete

### Known Bugs

- ⚠️ `measure_perf.py` may not capture peak CPU correctly
- ⚠️ LID confusion matrix not yet generated in detail

### Failure Modes Identified

1. **LID Confusion**: MN/HU mispredictions reduce effective sample size
2. **Mongolian Hallucination**: WER >1.0 suggests wrong language/script being used
3. **Short Audio LID**: Confidence drops for <30s clips

---

## 8. Next Steps (Toward Thesis Completion)

### Critical Path

1. ✅ **DONE**: Whisper-small baseline on CPU
2. 🔴 **TODO**: Add second ASR system (Wav2Vec2-XLS-R or NeMo)
3. 🔴 **TODO**: Run comparison experiments
4. 🟡 **TODO**: Expand to 120s audio clips
5. 🟡 **TODO**: GPU evaluation (if available)
6. 🟡 **TODO**: Detailed failure mode analysis
7. 🟢 **TODO**: Write thesis chapters

### Questions to Address

- Why does Mongolian fail so badly? (Wrong language detection? Undertrained?)
- How does LID accuracy change with audio length?
- What happens with code-switching or noisy audio?
- How do Whisper and System-2 compare head-to-head?

---

## Appendix: Command History

See `docs/appendix_commands.md` for full command log.

**Key Commands**:
```bash
# LID from audio
make lid FILE=data/wav/mn/mn1.wav MODEL=small

# Transcribe with language hint
make run_whisper_hinted FILE=data/wav/es/es1.wav LANG=es MODEL=small

# Transcribe with auto-detected language
make run_whisper_lid FILE=data/wav/fr/fr1.wav MODEL=small

# Evaluate transcripts
make eval REFS=data/refs/fr_refs.csv HYPDIR=results/transcripts/hinted/whisper/fr

# Measure performance
make perf CMD="python scripts/run_whisper.py --mode hinted ..." \
  FILE=data/wav/es/es1.wav
```
