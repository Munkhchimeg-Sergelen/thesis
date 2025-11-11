# Methods: Experimental Design

## For Thesis

### 3.5 Experimental Design

#### 3.5.1 Target Languages

Four languages representing diverse linguistic characteristics and resource availability were selected:

| Language | Code | Family | Resource Level | Speakers (M) | Whisper Training Data |
|----------|------|--------|----------------|--------------|----------------------|
| **Spanish** | ES | Romance | High | 485 | Abundant |
| **French** | FR | Romance | High | 280 | Abundant |
| **Hungarian** | HU | Uralic | Medium | 13 | Moderate |
| **Mongolian** | MN | Mongolic | Low | 5.2 | Limited |

**Selection Rationale**:

1. **Resource Diversity**: The language set spans high-resource (ES, FR), medium-resource (HU), and low-resource (MN) scenarios, enabling assessment of how system performance degrades with decreasing training data availability.

2. **Linguistic Diversity**:
   - **Romance languages (ES, FR)**: Similar phonology and orthography; tests language confusion
   - **Hungarian**: Agglutinative morphology with extensive case marking; challenges word-based metrics
   - **Mongolian**: Cyrillic script, subject-object-verb word order; underrepresented in training data

3. **Practical Relevance**: Languages span different global regions and use cases:
   - ES/FR: International business, education
   - HU: Regional EU application (author's institutional context)
   - MN: Endangered language documentation, digital inclusion

4. **Limitations Acknowledged**: Ideal experimental design would include more language families and scripts (e.g., Arabic, Mandarin). Current selection balances diversity with BSc thesis scope constraints.

---

#### 3.5.2 Audio Data

**Source**: Mozilla Common Voice v11.0 (community-contributed speech corpus)

**Data Selection Criteria**:
- **Split**: Test set (held-out data, never used in model training)
- **Quality**: Validated recordings (≥2 community approvals)
- **Duration**: 10-30 second segments (typical utterance length)
- **Sampling rate**: 16 kHz mono (ASR standard)

**Dataset Characteristics** (per language):

- **Target sample size**: 15-20 utterances per language
- **Duration range**: 5-30 seconds per sample
- **Speaker diversity**: Multiple speakers (Common Voice design)
- **Recording conditions**: Varied (real-world robustness test)

**Preprocessing**:
1. **Resampling**: All audio resampled to 16 kHz (Whisper requirement)
2. **Normalization**: PCM format, single channel (mono)
3. **No augmentation**: Raw audio used (worst-case evaluation)
4. **Reference transcripts**: Ground truth from Common Voice metadata

**Limitations**:
- Small dataset size (~60-80 total samples) due to:
  - BSc thesis time constraints
  - Common Voice API access issues during evaluation period
  - Mongolian limited availability in Common Voice
- Results should be interpreted as indicative trends rather than definitive benchmarks
- Future work should scale to larger test sets (100+ samples per language)

**Ethical Considerations**:
- Common Voice data is CC0-licensed (public domain)
- No speaker identification or demographic analysis performed
- Data handling complies with institutional research ethics guidelines

---

#### 3.5.3 Evaluation Protocol

**Test Configurations**:

The evaluation matrix covers 24 distinct configurations:

| Dimension | Values | Count |
|-----------|--------|-------|
| Model size | tiny, base, small | 3 |
| Hardware | CPU, GPU | 2 |
| Inference mode | Hinted, LID→ASR | 2 |
| Languages | MN, HU, FR, ES | 4 |

**Total combinations**: 3 × 2 × 2 × 4 = 48 configurations

**Simplification**: Due to time constraints, evaluation focuses on:
- **Primary**: GPU × 3 models × Hinted mode × 4 languages = 12 runs
- **Secondary**: CPU × small model × Hinted mode × 4 languages = 4 runs (baseline)
- **Tertiary**: LID→ASR mode evaluation (if time permits)

---

#### 3.5.4 Experimental Procedure

**For Each Configuration**:

1. **Load Model**: Initialize Whisper variant on target device
2. **Inference**:
   ```python
   for audio_file in language_samples:
       start_time = time.perf_counter()
       transcript = model.transcribe(audio_file, language=lang)
       end_time = time.perf_counter()
       
       # Capture metrics
       rtf = (end_time - start_time) / audio_duration
       # ... resource monitoring
   ```
3. **Metrics Collection**:
   - Transcription output
   - Wall-clock time
   - CPU/GPU utilization
   - Memory consumption
4. **Aggregation**: Compute mean, std, min, max across language samples

**Reproducibility Measures**:
- **Random seed**: Fixed for any stochastic operations (though Whisper is deterministic)
- **Environment specification**: Exact library versions recorded (`environment.yml`)
- **Code availability**: All evaluation scripts in public repository
- **Temperature = 0**: Deterministic decoding (Whisper parameter)

---

#### 3.5.5 Baseline Comparison

**Internal Baseline**: Whisper-small on CPU (hinted mode) serves as the reference point for all comparisons.

**Relative Metrics**:
- **Speedup**: GPU RTF / CPU RTF
- **Accuracy delta**: |WER_model - WER_baseline|
- **Resource ratio**: VRAM / RAM

**External Baselines**: Where possible, results are compared to published Whisper benchmarks:
- Radford et al. (2022): Original Whisper paper results
- HuggingFace leaderboards: Common Voice test set WER

**Limitations**: Direct comparison with external work is challenging due to:
- Different test set sizes
- Varying audio quality criteria
- Hardware configuration differences

Comparisons are presented as indicative context rather than definitive ranking.

---

#### 3.5.6 Threat to Validity

**Internal Validity**:
- **GPU server sharing**: Concurrent user load may inflate latency (acknowledged in results)
- **Small sample size**: Statistical power is limited
- **Cold start vs. warm cache**: First inference may be slower (mitigated by warm-up run)

**External Validity**:
- **Common Voice bias**: Read speech, not spontaneous conversation
- **Clean audio**: Real-world noise not fully represented
- **Language selection**: Results may not generalize to other language families

**Construct Validity**:
- **WER limitations**: Insensitive to semantic equivalence
- **RTF on shared resources**: May not reflect dedicated deployment

**Mitigation Strategies**:
1. Transparent reporting of limitations
2. Multiple metrics (WER + CER + efficiency)
3. Qualitative error analysis to complement quantitative metrics
4. Reproducible methodology for future replication with larger datasets

---

## Key Points

✅ **Diverse languages**: High/medium/low resource coverage  
✅ **Controlled evaluation**: Standardized protocol across configurations  
✅ **Transparent limitations**: Dataset size and validity threats acknowledged  
✅ **Reproducible**: Exact procedure documented with code  
✅ **Practical focus**: Evaluation scenarios match real deployment  

---

## For Thesis

**Suggested placement**: 
- Section 3.5 (Methods chapter)
- Cross-reference with Section 4 (Results) for actual sample sizes used

**Figures to add**:
- Language selection map (geographic distribution)
- Evaluation matrix diagram (configurations tested)
- Data preprocessing pipeline flowchart

---

## Notes

- Adjust sample sizes based on actual data obtained tonight
- Update "BSc thesis constraints" → specific timeline if needed
- Add table of actual per-language sample counts in Results chapter
- Consider moving "Limitations" to Discussion if preferred by advisor
