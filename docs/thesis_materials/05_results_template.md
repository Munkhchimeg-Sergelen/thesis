# Results Chapter - Template

## For Thesis

### Chapter 4: Results

This chapter presents the experimental results organized by comparison dimension: model scaling, hardware configuration, inference modes, and language-specific analysis.

---

### 4.1 Dataset Summary

**Actual samples collected** (UPDATE WITH REAL NUMBERS TONIGHT):

| Language | Samples | Total Duration | Mean Duration | Speakers |
|----------|---------|----------------|---------------|----------|
| Spanish (ES) | [N] | [X.X] min | [Y.Y] sec | [N] |
| French (FR) | [N] | [X.X] min | [Y.Y] sec | [N] |
| Hungarian (HU) | [N] | [X.X] min | [Y.Y] sec | [N] |
| Mongolian (MN) | [N] | [X.X] min | [Y.Y] sec | [N] |
| **Total** | [N] | [X.X] min | [Y.Y] sec | [N] |

---

### 4.2 Model Scaling Analysis (GPU)

This section compares Whisper-tiny, Whisper-base, and Whisper-small on GPU hardware.

#### 4.2.1 Accuracy vs. Model Size

**Word Error Rate by Model**:

| Model | ES WER | FR WER | HU WER | MN WER | Mean WER |
|-------|--------|--------|--------|--------|----------|
| Tiny | [X.X]% | [X.X]% | [X.X]% | [X.X]% | [X.X]% |
| Base | [X.X]% | [X.X]% | [X.X]% | [X.X]% | [X.X]% |
| Small | [X.X]% | [X.X]% | [X.X]% | [X.X]% | [X.X]% |

**Key Findings**:
- Small model achieves [X]% lower WER than tiny (averaged across languages)
- Improvement most pronounced on low-resource language (MN): [X]% vs [X]%
- Diminishing returns: Base→Small improvement ([X]%) < Tiny→Base ([X]%)

**[INSERT FIGURE: Bar chart of WER by model and language]**

---

#### 4.2.2 Efficiency vs. Model Size

**Real-Time Factor by Model (GPU)**:

| Model | ES RTF | FR RTF | HU RTF | MN RTF | Mean RTF |
|-------|--------|--------|--------|--------|----------|
| Tiny | [X.X] | [X.X] | [X.X] | [X.X] | [X.X] |
| Base | [X.X] | [X.X] | [X.X] | [X.X] | [X.X] |
| Small | [X.X] | [X.X] | [X.X] | [X.X] | [X.X] |

**Observations**:
- All models achieve RTF < 1.0 on GPU (real-time capable)
- Small model is [X]× slower than tiny
- Linear scaling: [analyze if RTF scales linearly with parameter count]

**[INSERT FIGURE: RTF comparison bar chart]**

---

#### 4.2.3 Speed-Accuracy Trade-off

**[INSERT FIGURE: Scatter plot - WER (y-axis) vs RTF (x-axis), points labeled by model]**

**Pareto Frontier Analysis**:
- Tiny: Fastest ([X.X] RTF) but highest error ([X]% WER)
- Small: Most accurate ([X]% WER) but slowest ([X.X] RTF)
- Base: **Balanced** choice for most applications

**Deployment Recommendation**: 
[Write recommendation based on actual results - e.g., "For latency-critical applications requiring <500ms response, tiny model is acceptable for high-resource languages (ES, FR). For accuracy-critical applications, small model justifies the 2-3× latency increase."]

---

### 4.3 Hardware Configuration Comparison

Comparison of Whisper-small on CPU vs. GPU.

#### 4.3.1 Speed Comparison

**Real-Time Factor: CPU vs. GPU**:

| Language | CPU RTF | GPU RTF | Speedup |
|----------|---------|---------|---------|
| ES | [X.X] | [X.X] | [X.X]× |
| FR | [X.X] | [X.X] | [X.X]× |
| HU | [X.X] | [X.X] | [X.X]× |
| MN | [X.X] | [X.X] | [X.X]× |
| **Mean** | [X.X] | [X.X] | [X.X]× |

**Key Finding**: GPU provides [X]× mean speedup over CPU for Whisper-small.

**[INSERT FIGURE: Side-by-side bar chart, CPU vs GPU RTF per language]**

---

#### 4.3.2 Resource Utilization

**Memory Consumption**:

| Hardware | RAM/VRAM Usage | Model Load Time |
|----------|----------------|-----------------|
| CPU | [X.X] GB RAM | [X.X] sec |
| GPU | [X.X] GB VRAM | [X.X] sec |

**CPU Utilization**:
- CPU: Mean [X]% utilization across cores
- GPU: Mean [X]% GPU utilization, [X]% GPU memory

**[INSERT TABLE OR FIGURE: Resource utilization comparison]**

---

#### 4.3.3 Deployment Cost Analysis

Based on cloud provider pricing (AWS as reference, Nov 2025):

| Configuration | Instance Type | Cost/hour | RTF | Cost per hour of audio |
|---------------|---------------|-----------|-----|------------------------|
| CPU (Whisper-small) | c7g.xlarge | $0.15 | [X.X] | $[X.XX] |
| GPU (Whisper-small) | g5.xlarge | $1.00 | [X.X] | $[X.XX] |

**Economic Trade-off**: [Analyze based on actual RTF - e.g., "Despite 7× higher instance cost, GPU's 15× speedup results in 2× lower cost per audio hour processed."]

---

### 4.4 Language-Specific Analysis

#### 4.4.1 Performance by Language Resource Level

**Mean WER by Language (Whisper-small, GPU, Hinted)**:

| Language | Resource Level | WER | CER | LID Accuracy |
|----------|----------------|-----|-----|--------------|
| ES | High | [X.X]% | [X.X]% | [X]% |
| FR | High | [X.X]% | [X.X]% | [X]% |
| HU | Medium | [X.X]% | [X.X]% | [X]% |
| MN | Low | [X.X]% | [X.X]% | [X]% |

**Observations**:
- Clear correlation between resource level and WER: [describe trend]
- Mongolian WER is [X]× higher than Spanish
- Hungarian CER/WER ratio suggests [morphological complexity / word boundary issues]

**[INSERT FIGURE: WER by language, color-coded by resource level]**

---

#### 4.4.2 Language Identification Accuracy

**LID Confusion Matrix** (LID→ASR mode):

|  | Predicted ES | Predicted FR | Predicted HU | Predicted MN |
|--|--------------|--------------| -------------|--------------|
| **True ES** | [N] | [N] | [N] | [N] |
| **True FR** | [N] | [N] | [N] | [N] |
| **True HU** | [N] | [N] | [N] | [N] |
| **True MN** | [N] | [N] | [N] | [N] |

**Analysis**:
- Overall LID accuracy: [X]%
- Most common confusion: [Lang1] ↔ [Lang2] ([N] cases)
  - **Explanation**: [phonological similarity / shared Romance features / etc.]
- Mongolian perfectly identified (likely due to script/phonology uniqueness)

---

### 4.5 Inference Mode Comparison

**Hinted vs. LID→ASR Performance** (Whisper-small, GPU):

| Language | Hinted WER | LID→ASR WER | Delta | LID Errors |
|----------|------------|-------------|-------|------------|
| ES | [X.X]% | [X.X]% | +[X.X]% | [N] |
| FR | [X.X]% | [X.X]% | +[X.X]% | [N] |
| HU | [X.X]% | [X.X]% | +[X.X]% | [N] |
| MN | [X.X]% | [X.X]% | +[X.X]% | [N] |

**Findings**:
- LID→ASR incurs [X]% mean WER penalty compared to oracle (hinted) mode
- Penalty highest when LID fails: [describe cascading errors]
- Perfect LID (MN): WER identical between modes

**Practical Implication**: [e.g., "For known-language applications (call centers), hinted mode is strongly preferred. For open-domain (media transcription), LID→ASR acceptable with X% accuracy degradation."]

---

### 4.6 Failure Mode Analysis

#### 4.6.1 Common Error Patterns

**Qualitative Analysis** (sample errors):

1. **Homophones** (ES/FR): [example]
2. **Morphological errors** (HU): [example - case marking confusion]
3. **Code-switching** (if present): [example]
4. **Proper nouns**: [example - names, places]

#### 4.6.2 Error Rate by Audio Duration

[IF TIME: Analyze correlation between sample duration and WER]

---

### 4.7 Summary of Results

**Key Findings Recap**:

1. **Model Scaling**: Small model reduces WER by [X]% vs tiny at cost of [X]× latency
2. **Hardware**: GPU provides [X]× speedup with identical accuracy
3. **Languages**: Performance degrades from high-resource (ES: [X]% WER) to low-resource (MN: [X]% WER)
4. **Inference Mode**: LID→ASR adds [X]% WER penalty when LID errors occur

**Best Configuration** (context-dependent):
- **Latency-critical + high-resource languages**: Tiny on GPU
- **Accuracy-critical**: Small on GPU
- **Cost-constrained batch**: Small on CPU

---

## Instructions for Tonight

**When you get real data and run experiments:**

1. **Run analysis script**:
   ```bash
   python scripts/analyze_results.py > results/summary.txt
   ```

2. **Extract numbers** from JSON outputs:
   ```bash
   # WER by model
   grep "wer" results/**/*.json
   
   # RTF by hardware
   grep "rtf" results/**/*.json
   ```

3. **Fill in all [X.X] placeholders** in this template

4. **Generate figures**:
   ```bash
   python scripts/create_plots.py
   ```

5. **Copy figures** to `docs/thesis_materials/figures/`

6. **Write interpretations** in the "Observations" and "Findings" sections

---

## Figures Needed

- [ ] Figure 4.1: WER by model size (bar chart)
- [ ] Figure 4.2: RTF by model size (bar chart)
- [ ] Figure 4.3: Speed-accuracy trade-off (scatter plot)
- [ ] Figure 4.4: CPU vs GPU RTF (side-by-side bars)
- [ ] Figure 4.5: WER by language and resource level
- [ ] Figure 4.6: LID confusion matrix (heatmap)
- [ ] Figure 4.7: Hinted vs LID→ASR comparison

---

## Tables Needed

All tables above → export as CSV, convert to LaTeX tables

---

**This template is ~8-10 pages when filled out. Combined with Methods (~6 pages), you'll have ~14-16 pages of content!**
