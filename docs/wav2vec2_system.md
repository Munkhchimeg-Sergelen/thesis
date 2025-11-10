# Second ASR System: Wav2Vec2-XLS-R

**System**: facebook/wav2vec2-xls-r-300m  
**Type**: Self-supervised speech representation learning + CTC decoder  
**Status**: ✅ Implemented (Nov 10, 2025)

---

## Overview

Wav2Vec2-XLS-R (Cross-Lingual Speech Representation) is Meta's multilingual speech model supporting 128 languages. It provides a contrasting architecture to Whisper:

- **Whisper**: Encoder-decoder transformer (sequence-to-sequence)
- **Wav2Vec2**: Encoder-only with CTC (Connectionist Temporal Classification)

---

## Model Details

### Architecture
- **Base**: wav2vec 2.0 pre-trained on 436K hours of unlabeled multilingual speech
- **Size**: 300M parameters
- **Fine-tuning**: Multiple language-specific versions available
- **Languages Supported**: 128 languages including MN, HU, FR, ES

### Key Differences from Whisper

| Feature | Whisper | Wav2Vec2-XLS-R |
|---------|---------|----------------|
| Architecture | Encoder-Decoder | Encoder + CTC |
| Training | Supervised (labeled data) | Self-supervised + fine-tuned |
| Language ID | Built-in | External (or filename inference) |
| Size (300M variant) | N/A | 300M params |
| Size (small) | 244M params | N/A |
| Decoding | Autoregressive | CTC (non-autoregressive) |
| Speed | Slower (sequential) | Faster (parallel) |

### Advantages
- ✅ **Faster inference**: CTC allows parallel decoding
- ✅ **Lower latency**: No autoregressive bottleneck
- ✅ **Open training**: More transparent self-supervised approach
- ✅ **Fine-tunable**: Easier to adapt to specific domains

### Disadvantages
- ❌ **No built-in LID**: Requires external language detection
- ❌ **CTC alignment**: Can produce repetitions/blank tokens
- ❌ **Less robust**: May struggle with noisy/long-form audio
- ❌ **No punctuation**: Base model outputs unpunctuated text

---

## Implementation

### Installation

Dependencies already in `asr-env`:
```bash
# Already installed:
# - transformers
# - torch
# - torchaudio
```

### Usage

**Command-line interface** (`scripts/asr_wav2vec2.py`):

```bash
# Hinted mode (language provided)
python scripts/asr_wav2vec2.py \
  --mode hinted \
  --infile data/wav/hu/sample.wav \
  --hint-lang hu \
  --device cpu \
  --save-json

# LID→ASR mode (language inferred from filename)
python scripts/asr_wav2vec2.py \
  --mode lid2asr \
  --infile data/wav/es/es01.wav \
  --device cpu \
  --save-json
```

**Makefile shortcuts**:

```bash
# Hinted mode
make run_wav2vec2_hinted FILE=data/wav/fr/fr01.wav LANG=fr

# LID mode
make run_wav2vec2_lid FILE=data/wav/mn/mn01.wav
```

### Output Format

**Text output** (stdout): Transcribed text  
**JSON sidecar** (if `--save-json`):
```json
{
  "text": "transcribed text here",
  "language_used": "hu",
  "duration_sec": 10.5,
  "elapsed_sec": 2.3,
  "rtf": 0.219,
  "model": "facebook/wav2vec2-xls-r-300m",
  "audio_file": "data/wav/hu/sample.wav",
  "mode": "hinted"
}
```

**File structure**:
```
results/transcripts/
  hinted/
    wav2vec2/
      hu/
        sample.txt       # Plain text transcription
        sample.json      # Detailed metadata
  lid2asr/
    wav2vec2/
      hu/
        sample.txt
        sample.json
```

---

## LID Strategy for Wav2Vec2

**Problem**: Base Wav2Vec2-XLS-R does not include language identification.

**Solutions Implemented**:

### 1. Hinted Mode (Oracle)
Language explicitly provided via `--hint-lang`.  
✅ Used for fair comparison with Whisper's hinted mode.

### 2. LID→ASR Mode (Current)
**Simple approach**: Infer language from filename pattern.
- Files with `mn`, `hu`, `fr`, `es` in name → language detected
- Falls back to "multi" (multilingual) if not found

**Limitation**: Not true LID; relies on file naming convention.

### 3. Future: External LID (TODO)
Integrate a separate LID model:
- **Option A**: Use Whisper's LID component separately
- **Option B**: Use dedicated LID model (e.g., `speechbrain/lang-id-voxlingua107`)
- **Option C**: Use `facebook/mms-lid` (Meta's Multilingual Speech LID)

---

## Evaluation Integration

### Metrics Collection

Same metrics as Whisper:
- **WER/CER**: Use `scripts/eval_metrics.py` on output transcripts
- **RTF**: Automatically captured in JSON output
- **Latency**: `elapsed_sec` in JSON
- **Memory**: Use `scripts/measure_perf.py` wrapper

### Comparison Script

**Quick comparison** (`scripts/compare_systems.py`):

```bash
# Single file comparison
python scripts/compare_systems.py \
  --audio data/wav/hu/sample.wav \
  --mode hinted \
  --lang hu \
  --whisper-model tiny

# Batch comparison
python scripts/compare_systems.py \
  --audio data/wav \
  --mode hinted \
  --langs mn hu fr es \
  --whisper-model small \
  --out-csv results/metrics/system_comparison.csv
```

---

## Performance Expectations

### Speed (RTF on CPU)
- **Wav2Vec2**: ~0.1-0.5 (faster due to CTC)
- **Whisper-tiny**: ~0.5-1.5
- **Whisper-small**: ~1.0-2.5

**Expected**: Wav2Vec2 should be 2-5× faster than Whisper.

### Accuracy (WER)
- **High-resource (ES, FR)**: Competitive with Whisper
- **Medium-resource (HU)**: May trail Whisper slightly
- **Low-resource (MN)**: Unknown; test needed

---

## Research Implications

### Why This Comparison Matters

1. **Architecture Diversity**: Encoder-decoder vs Encoder-CTC
2. **Training Paradigm**: Supervised vs self-supervised
3. **Speed-Accuracy Trade-off**: Faster inference vs potential accuracy loss
4. **Practical Deployment**: Low-latency applications (Wav2Vec2) vs high-accuracy (Whisper)

### Thesis Contributions

- ✅ Satisfies "≥2 ASR systems" requirement
- ✅ Enables architectural comparison
- ✅ Tests generalization across different model families
- ✅ Provides speed/accuracy trade-off analysis

---

## Testing Checklist

- [ ] Verify model loads on CPU
- [ ] Test hinted mode on all 4 languages
- [ ] Test lid2asr mode (filename inference)
- [ ] Compare WER/CER with Whisper
- [ ] Compare RTF/latency with Whisper
- [ ] Test on GPU (if available)
- [ ] Generate comparison tables/plots
- [ ] Document failure modes

---

## References

- **Paper**: Babu et al. (2021) "XLS-R: Self-supervised Cross-lingual Speech Representation Learning at Scale"
- **Model Card**: https://huggingface.co/facebook/wav2vec2-xls-r-300m
- **Wav2Vec2 Paper**: Baevski et al. (2020) "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations"

---

## Next Steps

1. **Immediate**: Test on sample audio (create if needed)
2. **Week 1**: Run full evaluation on all audio data
3. **Week 1**: Generate comparison plots/tables
4. **Week 2**: Write "System Comparison" section in thesis
