# Methods: Evaluation Metrics

## For Thesis

### 3.4 Evaluation Metrics

System performance was assessed using both accuracy metrics (transcription quality) and efficiency metrics (computational resource usage), providing a comprehensive view of deployment trade-offs.

---

#### 3.4.1 Accuracy Metrics

##### Word Error Rate (WER)

Word Error Rate (WER) is the primary metric for ASR evaluation, measuring the edit distance between the hypothesis (system output) and reference (ground truth) transcriptions at the word level.

**Definition**:

$$\text{WER} = \frac{S + D + I}{N} \times 100\%$$

where:
- $S$ = number of substitutions (words replaced)
- $D$ = number of deletions (words omitted)
- $I$ = number of insertions (extra words added)
- $N$ = total number of words in reference

**Interpretation**:
- WER = 0%: Perfect transcription
- WER = 100%: Complete mismatch
- WER > 100%: Possible when insertions exceed reference length

**Implementation**: Computed using the `jiwer` library (Levenshtein distance algorithm) with default normalization (lowercasing, punctuation removal).

**Rationale**: WER is the de facto standard for ASR evaluation, enabling direct comparison with prior work. However, it can be sensitive to inconsequential variations (e.g., "don't" vs. "do not"), potentially overstating errors.

---

##### Character Error Rate (CER)

Character Error Rate (CER) measures edit distance at the character level, providing finer-grained error analysis.

**Definition**:

$$\text{CER} = \frac{S_c + D_c + I_c}{N_c} \times 100\%$$

where subscript $c$ denotes character-level operations.

**Advantages over WER**:
1. **Morphologically rich languages**: Better suited for languages like Hungarian with complex word formation
2. **Partial credit**: Recognizes partially correct words (e.g., "recognize" → "reconize" has low CER, high WER)
3. **Language-agnostic**: No word tokenization required (important for Mongolian)

**Complementary use**: CER and WER together provide nuanced error characterization. High WER with low CER suggests word boundary/morphology issues; high CER indicates phonetic confusions.

---

#### 3.4.2 Language Identification Accuracy

For the LID→ASR mode, language identification accuracy directly impacts overall system performance.

**Definition**:

$$\text{LID Accuracy} = \frac{\text{Correctly identified samples}}{\text{Total samples}} \times 100\%$$

**Confusion Matrix**: We additionally report language confusion matrices to identify systematic misclassifications (e.g., Hungarian ↔ Finnish due to phonological similarity).

**Confidence Scores**: Whisper's LID module outputs probability distributions over languages. We analyze:
- Mean confidence for correct predictions
- Mean confidence for incorrect predictions
- Confidence threshold selection for fallback strategies

---

#### 3.4.3 Efficiency Metrics

##### Real-Time Factor (RTF)

Real-Time Factor (RTF) measures inference speed relative to audio duration.

**Definition**:

$$\text{RTF} = \frac{T_{\text{processing}}}{T_{\text{audio}}}$$

where:
- $T_{\text{processing}}$ = wall-clock time for transcription
- $T_{\text{audio}}$ = duration of input audio

**Interpretation**:
- RTF < 1.0: Faster than real-time (e.g., RTF = 0.5 → 10s audio processed in 5s)
- RTF = 1.0: Real-time processing
- RTF > 1.0: Slower than real-time (batch-only scenarios)

**Threshold for Real-Time Applications**: RTF ≤ 1.0 is required for streaming/live transcription. We report percentage of samples meeting this threshold per configuration.

---

##### Absolute Latency

While RTF is scale-invariant, absolute latency matters for user experience.

**Metrics**:
- **Mean latency**: Average processing time across samples
- **95th percentile**: Tail latency for worst-case planning
- **Throughput**: Samples processed per second (batch scenarios)

**Measurement**: Wall-clock time captured using Python's `time.perf_counter()` with microsecond precision.

---

##### Resource Utilization

**CPU Metrics** (via `psutil`):
- **CPU percentage**: Core utilization during inference
- **RSS (Resident Set Size)**: Memory consumption in MB
- **Peak memory**: Maximum memory usage per sample

**GPU Metrics** (via `pynvml`):
- **VRAM usage**: GPU memory consumption in MB
- **GPU utilization**: Compute utilization percentage
- **CUDA kernel time**: GPU-specific processing time

**Rationale**: Resource metrics inform deployment cost estimation:
- **Cloud deployment**: CPU/GPU-hour costs
- **Edge deployment**: Memory footprint for device selection
- **Sustainability**: Energy consumption proxy via utilization

---

#### 3.4.4 Statistical Significance

Given the relatively small dataset size (necessity for a BSc thesis timeframe), we report:

1. **Descriptive statistics**: Mean, standard deviation, min/max for all metrics
2. **Effect sizes**: Cohen's d for comparing model sizes and hardware configurations
3. **Confidence intervals**: 95% CI for mean WER/CER where applicable

**Note on significance testing**: Formal hypothesis testing (e.g., paired t-tests) is presented where sample sizes permit, but emphasis is placed on practical significance (e.g., 5% WER difference) over purely statistical significance.

---

## Supporting Data

**Metric Computation Scripts**:
- `scripts/eval_metrics.py`: WER/CER computation
- `scripts/measure_perf.py`: Latency and resource profiling
- `scripts/lid_from_whisper.py`: LID accuracy evaluation

**Libraries**:
- `jiwer==4.0.0`: WER/CER computation (edit distance)
- `psutil`: CPU/memory monitoring
- `pynvml`: GPU monitoring (CUDA environments)

---

## Key Points

✅ **Comprehensive**: Both accuracy (WER, CER, LID) and efficiency (RTF, latency, resources)  
✅ **Standard metrics**: WER enables comparison with prior work  
✅ **Practical focus**: RTF and resource usage inform deployment decisions  
✅ **Rigorous**: Statistical measures acknowledge dataset limitations  
✅ **Reproducible**: All metric computation scripts provided

---

## Notes for Writing

- Include example calculations in an appendix (e.g., WER for one sample)
- Cross-reference with Results chapter (e.g., "WER results in Section 4.2")
- Cite foundational papers for WER/CER (e.g., NIST evaluation standards)
- Mention any metric normalization choices (e.g., case, punctuation)

---

## TODO
- [ ] Add citation for WER/CER definitions
- [ ] Add citation for RTF metric
- [ ] Verify formula rendering in final LaTeX
- [ ] Add example calculation to appendix
