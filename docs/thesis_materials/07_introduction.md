## Chapter 1: Introduction

### 1.1 Motivation

Automatic Speech Recognition (ASR) has become ubiquitous in modern technology, powering applications ranging from virtual assistants (Siri, Alexa, Google Assistant) to real-time captioning and multilingual video subtitling. As global communication increasingly occurs across language boundaries, the demand for ASR systems capable of handling multiple languages has grown dramatically.

However, developing multilingual ASR systems presents fundamental trade-offs. Should developers deploy a single unified model that handles all languages, or maintain separate language-specific models optimized for individual languages? This question has profound implications for deployment costs, system latency, transcription accuracy, and practical coverage of the world's linguistic diversity.

**The unified multilingual approach** (e.g., OpenAI Whisper) offers compelling advantages: a single model download, consistent API across languages, and the ability to leverage cross-lingual transfer learning. Yet, this convenience may come at the cost of per-language accuracy, particularly when compared to models specialized for individual languages.

**The language-specific specialization approach** (e.g., fine-tuned Wav2Vec2-XLSR-53 models) promises higher accuracy by dedicating model capacity entirely to one language. However, this requires deploying N separate models for N languages, increasing storage requirements, deployment complexity, and creating gaps in language coverage where specialized models are unavailable.

Despite extensive research in multilingual ASR, **direct, controlled comparisons** of these two approaches on **identical hardware and test data** are limited in the literature. Most studies either evaluate a single multilingual system across languages or compare different architectures without isolating the multilingual strategy from other design choices. Furthermore, academic benchmarks often focus exclusively on Word Error Rate (WER), neglecting practical deployment considerations such as inference latency, memory requirements, and hardware utilization—metrics critical for real-world deployment decisions.

---

### 1.2 Research Questions

This thesis addresses the following research questions:

**RQ1: Multilingual Convenience vs. Language-Specific Accuracy**  
Do language-specific fine-tuned models (Wav2Vec2-XLSR-53) achieve higher transcription accuracy than unified multilingual models (Whisper) on high-resource languages (Spanish, French), and if so, by how much?

**RQ2: Model Scaling Trade-offs**  
How does transcription accuracy and inference speed scale with model size (39M → 74M → 244M parameters) for a multilingual ASR system (Whisper)? Is there a point of diminishing returns where additional parameters no longer justify the increased computational cost?

**RQ3: Hardware Configuration Impact**  
What are the practical implications of CPU vs. GPU deployment for multilingual ASR in terms of latency, throughput, and resource utilization? Which configurations enable real-time transcription (RTF < 1.0)?

**RQ4: Language Resource Level Effects**  
How does a unified multilingual model (Whisper) perform across languages with varying training data availability—high-resource (Spanish, French), medium-resource (Hungarian), and low-resource (Mongolian)? Does performance degrade linearly with resource level, or are there threshold effects?

**RQ5: Language Identification Impact**  
For multilingual models with built-in language identification (Whisper), what is the performance penalty when language is detected automatically (LID→ASR) compared to providing the language explicitly (language-hinted mode)? How often do LID errors cascade into transcription errors?

---

### 1.3 Thesis Contributions

This thesis makes the following contributions:

**1. Controlled Comparison of Multilingual Strategies**  
A rigorous evaluation of unified multilingual models (Whisper) versus language-specific specialization (Wav2Vec2-XLSR-53) on identical test data, hardware configurations, and evaluation metrics. This addresses the gap in prior work where architectural differences confound multilingual strategy comparisons.

**2. Deployment-Oriented Evaluation Framework**  
Goes beyond traditional WER-focused benchmarks by incorporating Real-Time Factor (RTF), latency, CPU/GPU utilization, and memory consumption—metrics directly relevant to deployment decisions. This provides actionable insights for practitioners choosing ASR systems for specific use cases.

**3. Model Scaling Analysis**  
Quantifies the speed-accuracy trade-off across three Whisper model sizes (39M, 74M, 244M parameters), identifying the point of diminishing returns for multilingual ASR. This informs resource-constrained deployment scenarios (e.g., edge devices vs. cloud servers).

**4. Language Diversity Assessment**  
Evaluates system performance across four languages spanning different resource levels (Spanish/French: high, Hungarian: medium, Mongolian: low) and linguistic typologies (Romance, Uralic, Mongolic). This reveals how well multilingual systems generalize beyond high-resource Western languages.

**5. Reproducible Methodology**  
All evaluation scripts, environment specifications, and experimental protocols are publicly available in a GitHub repository, enabling replication and extension of this work. This addresses the reproducibility crisis in ASR research.

---

### 1.4 Scope and Limitations

**Scope**:
- **Systems**: OpenAI Whisper (multilingual) and Wav2Vec2-XLSR-53 (language-specific) as representative examples of two multilingual strategies
- **Languages**: Spanish (ES), French (FR), Hungarian (HU), Mongolian (MN)—chosen to span high/medium/low resource levels
- **Hardware**: Consumer-grade CPU (Apple M-series) and enterprise GPU (NVIDIA RTX A6000)
- **Metrics**: WER, CER, RTF, latency, CPU/GPU utilization, memory consumption
- **Audio Data**: Mozilla Common Voice v11.0 test set (read speech, clean recordings)

**Limitations**:
- **Small test set**: Due to BSc thesis time constraints, ~15-20 samples per language were evaluated rather than the hundreds typical of large-scale benchmarks. Results should be interpreted as indicative trends rather than definitive rankings.

- **Limited language coverage**: Only 4 of the world's ~7,000 languages are evaluated. While chosen to represent diverse typologies and resource levels, findings may not generalize to all language families.

- **Read speech only**: Common Voice contains read speech in controlled conditions, not spontaneous conversation. Performance on noisy, real-world audio may differ.

- **Wav2Vec2 availability constraint**: Language-specific Wav2Vec2 models are only available for Spanish and French (not Hungarian or Mongolian), preventing full cross-language comparison of the two approaches.

- **No model training**: This study evaluates pre-trained models as-is; custom training or fine-tuning is not performed. Conclusions are limited to publicly available checkpoints.

**Rationale**: Despite these limitations, the controlled comparison on identical test conditions provides valuable insights into the practical trade-offs between multilingual ASR strategies—insights that are underrepresented in existing literature.

---

### 1.5 Thesis Structure

The remainder of this thesis is organized as follows:

**Chapter 2: Background and Related Work**  
Reviews ASR fundamentals (architectures, metrics), multilingual ASR challenges (phonetic diversity, data imbalance, morphology), language identification approaches, and prior work on multilingual systems and comparative studies.

**Chapter 3: Methods**  
Describes the evaluation methodology including hardware configurations (CPU/GPU), ASR systems evaluated (Whisper variants, Wav2Vec2-XLSR-53), evaluation metrics (WER, CER, RTF, resources), experimental design (languages, data, protocol), and reproducibility measures.

**Chapter 4: Results**  
Presents experimental findings organized by comparison dimension: model scaling (Whisper tiny/base/small), hardware configuration (CPU vs. GPU), system architecture (Whisper vs. Wav2Vec2), language diversity (ES/FR/HU/MN), and inference modes (hinted vs. LID→ASR).

**Chapter 5: Discussion**  
Interprets results in the context of the research questions, identifies failure modes and error patterns, discusses deployment recommendations for different use cases, acknowledges threats to validity, and positions findings relative to prior work.

**Chapter 6: Conclusions**  
Summarizes key findings, reflects on contributions and limitations, and suggests directions for future work including larger-scale evaluation, additional languages, real-world audio conditions, and emerging architectures.

---

### 1.6 Expected Outcomes

Based on prior work and preliminary testing, we hypothesize:

**H1**: Language-specific Wav2Vec2 models will achieve 5-15% lower WER than Whisper on Spanish and French, but this accuracy gain will come at the cost of 3-4× higher deployment complexity (separate models) and 4-5× larger storage requirements.

**H2**: Whisper-small (244M parameters) will achieve the best accuracy among Whisper variants, but with RTF 2-3× higher than Whisper-tiny (39M). For real-time applications (RTF < 1.0), only tiny and base models will be viable on CPU.

**H3**: GPU deployment will provide 10-20× speedup over CPU for the same model, enabling real-time transcription even for larger models (small). However, GPU memory constraints and cost will limit practicality for edge deployment.

**H4**: Whisper's performance will degrade as language resource level decreases, with Mongolian (low-resource) showing 2-3× higher WER than Spanish/French (high-resource). However, the multilingual model will still provide usable transcriptions where no specialized alternative exists.

**H5**: Automatic language identification (LID→ASR) will incur a 5-10% WER penalty compared to oracle (language-hinted) mode, primarily due to cascading errors when LID fails on short audio segments or acoustically similar languages.

These hypotheses will be tested and refined based on experimental results presented in Chapter 4.

---

## Key Points

✅ **Clear motivation**: Multilingual ASR is important but involves fundamental trade-offs  
✅ **Well-defined research questions**: Five specific, testable questions  
✅ **Concrete contributions**: What this thesis adds beyond prior work  
✅ **Honest scope and limitations**: Transparent about constraints  
✅ **Structured roadmap**: Clear outline of remaining chapters  
✅ **Testable hypotheses**: Predictions to validate or refute  

---

## Notes for Finalization

- Add specific BSc thesis context (university, department, supervisor)
- Include thesis submission deadline and institutional requirements
- Add acknowledgments section (advisor, GPU server access provider, etc.)
- Ensure all forward references to later chapters are accurate
- Polish hypotheses after seeing actual results (Chapter 4)
- Adjust "expected outcomes" to "research questions addressed" if running short on time

---

## TODO
- [ ] Add university name, department, and year
- [ ] Add supervisor name and acknowledgments
- [ ] Verify all cross-references to chapter/section numbers
- [ ] Add thesis submission date
- [ ] Polish after results are available (update hypotheses → findings)
