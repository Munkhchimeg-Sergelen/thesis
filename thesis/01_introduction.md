# Chapter 1: Introduction

## 1.1 Motivation and Background

Automatic Speech Recognition (ASR) has become increasingly important in modern applications, from virtual assistants and automated transcription services to accessibility tools for individuals with disabilities. As globalization accelerates, the need for ASR systems that can handle multiple languages has grown substantially. However, deploying multilingual ASR systems presents fundamental challenges: should a single unified model handle all languages, or should language-specific models be deployed for each target language?

Multilingual ASR systems face a critical decision point at inference time. When audio is received, the system must either (i) automatically detect the spoken language and then transcribe it (LID→ASR pipeline), or (ii) accept an explicit language hint from the user or application context (language-hinted mode). Each approach presents distinct trade-offs in terms of accuracy, processing efficiency, and deployment complexity.

Furthermore, low-resource languages—those with limited training data—present additional challenges. Languages such as Mongolian, with only 5.2 million native speakers and limited digital resources, often suffer from degraded performance compared to high-resource languages like Spanish or French. Understanding these performance disparities is essential for developing equitable multilingual ASR systems.

Despite extensive research in multilingual ASR, practical questions remain underexplored:
- How accurate is automatic language identification for diverse languages?
- What is the computational cost of automatic language detection versus explicit language hints?
- How do low-resource languages perform compared to high-resource languages in unified multilingual models?
- What are the practical trade-offs between unified multilingual models and language-specific specialized models?

This thesis addresses these questions through a comprehensive evaluation of multilingual ASR approaches using real-world systems and datasets.

## 1.2 Problem Statement

This thesis investigates **multilingual automatic speech recognition approaches** with a focus on comparing two inference strategies:

1. **LID→ASR Pipeline (Mode A)**: Automatic language identification from audio followed by language-specific transcription
2. **Language-Hinted ASR (Mode B)**: Direct transcription with explicitly provided language information

The core research problem is: **How does prior knowledge of the spoken language impact ASR system performance in terms of recognition quality, processing efficiency, and robustness across languages with varying resource levels?**

## 1.3 Research Questions

This thesis addresses the following specific research questions:

**RQ1: Language Identification Accuracy**  
How accurate is automatic language identification across languages with different resource levels (high-resource: Spanish, French; medium-resource: Hungarian; low-resource: Mongolian)?

**RQ2: Inference Mode Comparison**  
How do LID→ASR and language-hinted modes compare in terms of:
- Transcription accuracy (WER, CER)
- Processing efficiency (Real-Time Factor)
- Resource utilization

**RQ3: Cross-Language Performance Analysis**  
How does multilingual ASR performance vary across languages with different:
- Resource availability (training data)
- Linguistic characteristics (script, morphology)
- Audio duration

**RQ4: Model Architecture Comparison**  
How do different ASR architectures (encoder-decoder vs CTC-based) perform across multilingual scenarios in terms of:
- Accuracy
- Speed
- Consistency across languages

**RQ5: Practical Deployment Considerations**  
What are the practical trade-offs and recommendations for deploying multilingual ASR systems in real-world scenarios?

## 1.4 Contributions

This thesis makes the following contributions:

**1. Comprehensive Multilingual ASR Evaluation**  
Systematic evaluation of 4 ASR models across 4 languages, representing 16,000 transcriptions. The evaluation includes both unified multilingual models (Whisper) and language-specific fine-tuned models (OmniLingual variants).

**2. Dual-Mode Inference Analysis**  
First direct comparison of LID→ASR versus language-hinted modes on identical test sets, quantifying the impact of automatic language detection on both accuracy and efficiency.

**3. Low-Resource Language Performance Quantification**  
Detailed analysis of Mongolian (low-resource) performance, revealing critical efficiency issues:
- **74× processing time disparity** between Mongolian and Spanish for Whisper
- RTF of 36.98 for Mongolian versus 0.50 for Spanish, rendering real-time processing infeasible

**4. Reproducible Evaluation Framework**  
Complete evaluation pipeline with:
- 15+ automated scripts for data preparation, evaluation, and analysis
- Docker containerization for environment reproducibility
- Comprehensive documentation and version control
- Publicly available code repository

**5. Practical Deployment Recommendations**  
Evidence-based guidelines for model selection, inference mode choice, and deployment strategies based on use case requirements (real-time vs batch, known vs unknown language, resource constraints).

## 1.5 Key Findings Preview

The evaluation revealed several important findings:

**Finding 1: Severe Low-Resource Language Degradation**  
Whisper exhibits a **74× speed difference** between Mongolian (RTF 36.98) and Spanish (RTF 0.50), making real-time Mongolian ASR impossible with this model on CPU.

**Finding 2: Architecture-Dependent Performance Patterns**  
OmniLingual models maintain **consistent speed across all languages** (RTF ~0.01-0.05), demonstrating superior efficiency for low-resource languages compared to Whisper.

**Finding 3: Speed-Accuracy Trade-offs Vary by Model**  
OmniLingual CTC models achieve **100× faster processing** than Whisper while maintaining competitive accuracy, offering practical advantages for real-time applications.

**Finding 4: Language-Specific Error Patterns**  
CER proves more informative than WER for agglutinative languages (Mongolian, Hungarian), revealing performance patterns masked by word-level metrics.

**Finding 5: Perfect Alignment Methodology**  
Achieved **1000/1000 audio-reference alignment** through systematic sampling from Common Voice v23.0, eliminating data quality issues that plagued previous studies.

These findings provide actionable insights for practitioners deploying multilingual ASR systems.

## 1.6 Thesis Organization

The remainder of this thesis is structured as follows:

**Chapter 2: Background and Related Work** reviews ASR fundamentals, multilingual modeling approaches, language identification techniques, and prior work in multilingual ASR evaluation.

**Chapter 3: Methodology** describes the evaluation framework, including language and dataset selection (4 languages, Common Voice v23.0, 1000 samples per language), ASR systems evaluated (Whisper-small, OmniLingual CTC 300M/1B, OmniLingual LLM 1B), inference modes, evaluation metrics (WER, CER, RTF, LID accuracy), and reproducibility measures.

**Chapter 4: Results** presents experimental findings organized by recognition quality (WER/CER analysis), efficiency (RTF and processing time), language identification accuracy, audio duration effects, and detailed error analysis.

**Chapter 5: Discussion** interprets the results in context of the research questions, analyzes failure modes (LID confusion, low-resource degradation, speed variation), provides practical deployment recommendations, discusses limitations, and positions findings relative to prior work.

**Chapter 6: Conclusions and Future Work** summarizes key contributions, answers research questions, acknowledges limitations, and proposes future research directions including improved LID for short clips, streaming ASR, and domain-specific fine-tuning.

---

**End of Chapter 1**
