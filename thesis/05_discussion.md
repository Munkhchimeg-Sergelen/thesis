# Chapter 5: Discussion

This chapter interprets the experimental findings presented in Chapter 4, analyzing their implications for multilingual ASR deployment. Section 5.1 discusses key findings in context of prior work, Section 5.2 analyzes failure modes and their causes, Section 5.3 provides practical deployment recommendations, Section 5.4 acknowledges limitations, and Section 5.5 positions this work relative to the broader research landscape.

## 5.1 Interpretation of Key Findings

### 5.1.1 The Mongolian Catastrophe: Language Inequality in Multilingual Models

The most significant finding is Whisper's catastrophic performance degradation on Mongolian, processing 74× slower than Spanish (RTF 36.98 versus 0.50). This result reveals fundamental challenges in current multilingual ASR approaches when handling low-resource languages.

Several factors likely contribute to this failure:

Training Data Imbalance: Whisper's training corpus, while massive (680,000 hours), exhibits severe imbalance across languages. English likely dominates the training data, with high-resource languages well-represented and low-resource languages like Mongolian comprising a tiny fraction. During training, gradient updates predominantly reflect high-resource language patterns. The model learns acoustic-phonetic mappings optimized for Spanish, French, and English, while Mongolian representations remain underfit.

Architectural Assumptions: Autoregressive decoding in encoder-decoder models may implicitly assume linguistic patterns characteristic of high-resource languages. The decoder's language model component, learned primarily from high-resource languages, may struggle with Mongolian's distinctive morphology (agglutinative with long words) and syntax. This forces excessive decoding iterations as the model explores improbable hypotheses, accumulating computational cost.

Phonological Distinctiveness: Mongolian phonology differs substantially from Indo-European languages dominating the training corpus. Unique phonemes, prosodic patterns, and coarticulation effects absent in training data may force the encoder to rely on weaker generalizations, increasing processing time as the model expends computation resolving acoustic ambiguity.

The finding contradicts the promise of multilingual models to democratize ASR across languages. Whisper technically supports 99 languages, but this evaluation demonstrates that nominal support does not guarantee usable performance. For Mongolian, Whisper's 188-second average processing time per 5.5-second utterance renders it completely impractical for any deployment scenario.

### 5.1.2 OmniLingual's Consistent Performance: CTC Architecture Advantage

In stark contrast, OmniLingual models maintained remarkably consistent processing speeds across all languages, with RTF ranging only from 0.014 to 0.024 for CTC variants. This consistency proves critical for equitable multilingual deployment.

CTC Architecture Benefits: Non-autoregressive CTC decoding avoids the variable-length hypothesis search that plagues Whisper on Mongolian. Frame-level predictions proceed in parallel, bounded by audio duration regardless of linguistic complexity. Even if acoustic features prove challenging (requiring multiple CTC blank tokens or uncertain character predictions), processing time scales linearly with audio length rather than exploding combinatorially.

Training Objectives: CTC's frame-wise training objective may encourage more uniform cross-language representations. Unlike encoder-decoder models where the decoder's language model can dominate and introduce language-specific biases, CTC focuses on acoustic-phonetic mapping with less linguistic structure. This potentially reduces the advantage high-resource languages receive during training.

Parameter Efficiency: The OmniLingual CTC 300M model, with only 22% more parameters than Whisper-small (244M), achieves 1500-2500× faster Mongolian processing. This dramatic efficiency difference demonstrates that architectural choices dominate parameter count in determining practical performance.

The OmniLingual results prove that equitable multilingual ASR is achievable with appropriate architectural design. CTC-based models offer not just speed advantages but, crucially, consistent speed across diverse languages.

### 5.1.3 Speed-Accuracy Trade-offs: No Universal Solution

The evaluation reveals no single model dominates across all deployment scenarios. Instead, optimal choice depends on specific constraints:

High-Resource Languages (Spanish, French): Multiple models achieve acceptable performance. Whisper offers moderate speed (RTF ~0.5) with competitive accuracy. OmniLingual CTC variants provide 30× faster processing with potentially comparable accuracy. OmniLingual LLM 1B achieves similar speed to Whisper while maintaining consistent cross-language performance.

Low-Resource Languages (Mongolian): Only CTC-based models provide usable performance. Whisper's RTF of 36.98 renders it completely impractical. CTC variants achieve real-time processing (RTF 0.014-0.020), enabling deployment despite lower training data availability.

Real-Time Applications: CTC models prove essential, providing substantial margin below real-time constraints. Even OmniLingual LLM 1B maintains RTF < 0.6 across all languages, supporting real-time use cases.

Batch Processing: Whisper remains viable for high-resource languages in offline scenarios where processing time exceeds real-time by factors of 2-3. However, Mongolian remains impractical even for batch processing.

This heterogeneity in optimal solutions suggests deployment strategies should account for language-specific performance rather than assuming universal model applicability.

## 5.2 Failure Mode Analysis

### 5.2.1 LID Confusion and Error Cascading

Language identification errors cascade directly into transcription failures in LID→ASR pipelines. When LID misidentifies the spoken language, the ASR system receives inappropriate language conditioning, producing degraded or completely incorrect transcriptions.

[Analysis pending LID results completion]

Expected failure patterns include Spanish-French confusion due to linguistic similarity, potentially Hungarian confusion with Slavic languages if training data insufficiently represents Hungarian phonology, and Mongolian misidentification if acoustic distinctiveness fails to compensate for limited training representation.

The impact of LID errors depends on downstream ASR robustness. If the ASR model gracefully degrades when receiving incorrect language hints (e.g., still producing partially correct transcriptions), LID errors prove less catastrophic. If ASR completely fails under incorrect conditioning, LID accuracy requirements become stringent.

Mitigation strategies include confidence thresholding (rejecting low-confidence LID predictions), N-best LID (considering multiple language hypotheses), and fallback to language-independent multilingual mode when LID uncertainty exceeds acceptable thresholds.

### 5.2.2 Low-Resource Language Degradation

Mongolian's severe degradation across multiple dimensions (processing speed, accuracy, consistency) exemplifies low-resource language challenges in multilingual models.

The degradation manifests as both lower accuracy (higher WER/CER compared to high-resource languages) and catastrophically slower processing (74× speed disparity for Whisper). This dual failure renders low-resource languages effectively unsupported despite nominal inclusion in the model's language list.

Root Causes: Technical and Linguistic Factors

Consultation with the Chimege research team, developers of state-of-the-art Mongolian ASR systems, revealed specific technical causes for the observed performance degradation (Chimege, personal communication, December 2025):

Implementation Bias in Inference Libraries: The faster-whisper and CTranslate2 libraries used in this evaluation are highly optimized for common languages (English, Spanish, French), resulting in suboptimal performance for non-common languages like Mongolian. These optimization biases affect inference speed rather than model quality, explaining why the same Whisper model exhibits drastically different RTF across languages.

Tokenization Inefficiency: Whisper's public tokenizer operates at near-character level for Mongolian while using word-level tokens for English and other high-resource languages. This tokenization mismatch forces the model to generate many more tokens per utterance for Mongolian, directly increasing decoding time. For example, a 5-second Mongolian utterance may require 50-100 character-level tokens, while an equivalent English utterance needs only 10-15 word-level tokens, resulting in a 5-10× decoding overhead from tokenization alone.

Training Data Imbalance: Mongolian comprises perhaps <0.1% of Whisper's training corpus, leading to underfit acoustic-phonetic representations. Chimege reports achieving 2-3% WER on Mongolian using models trained on substantially larger Mongolian-specific datasets, demonstrating that adequate training data enables high-quality Mongolian ASR.

Architectural Assumptions: Gradient updates during training are dominated by high-resource languages, causing the model to learn optimization patterns favorable to common languages but suboptimal for low-resource languages.

These findings suggest that the 74× slowdown stems from implementation-level optimization bias and tokenization strategy rather than fundamental linguistic incompatibility. Properly optimized inference (ONNX format or native implementation without third-party library overhead) and appropriate tokenization could substantially reduce this disparity, though likely not eliminate it entirely given training data limitations.

Solutions require both technical and methodological changes: native inference implementations without language-specific optimization bias, language-appropriate tokenizers trained on representative corpora, balanced sampling during training to equalize gradient contributions across languages, language-specific adapter layers, and CTC-based architectures which maintain more consistent cross-language performance.

### 5.2.3 Speed Variation and Predictability

Whisper's processing time exhibits extreme variability on Mongolian, with standard deviation of 44.9 seconds around a mean of 188 seconds. Some samples process in 60-80 seconds (still impractically slow), while worst-case samples exceed 150 seconds.

This unpredictability proves problematic for deployment. Systems must provision for worst-case latency, and unpredictable response times degrade user experience. Batch processing cannot reliably schedule computational resources when processing time varies by factors of 2-3× within a single language.

In contrast, OmniLingual models maintain low standard deviation relative to mean processing time, providing predictable performance suitable for production deployment with reliable latency guarantees.

### 5.2.4 Audio Length Effects

[Analysis pending detailed duration analysis]

Expected patterns include RTF increasing with audio duration if models exhibit super-linear scaling, potentially due to attention mechanism complexity (O(n²) for sequence length n) or decoder hypothesis search space expansion.

CTC models should demonstrate near-constant RTF across duration ranges, as frame-level predictions scale linearly with audio length. Any RTF increase with duration would suggest implementation inefficiencies rather than fundamental algorithmic limitations.

Whisper may show increased RTF for longer Mongolian samples if the decoder exhausts more hypotheses attempting to resolve linguistic uncertainty. High-resource languages should maintain relatively stable RTF as the decoder efficiently explores hypotheses guided by strong language model priors.

## 5.3 Practical Deployment Recommendations

### 5.3.1 Model Selection Guidelines

For Known High-Resource Languages (Spanish, French, English):
- Whisper-small provides acceptable performance (RTF 0.5-0.6) with competitive accuracy
- OmniLingual CTC models offer 30× speed advantage if accuracy proves comparable (pending final WER/CER analysis)
- OmniLingual LLM 1B balances speed and accuracy, suitable for quality-critical applications
- Recommendation: Evaluate accuracy requirements; use CTC models if speed-critical or cost-sensitive, Whisper or LLM variant if accuracy-critical

For Medium-Resource Languages (Hungarian, Polish, Czech):
- Whisper approaches real-time constraints (RTF 1.8 for Hungarian), limiting real-time viability
- OmniLingual models maintain efficient processing (RTF 0.02-0.5)
- Recommendation: Prefer CTC-based models for real-time applications; Whisper acceptable for offline processing

For Low-Resource Languages (Mongolian, minority languages):
- Whisper completely impractical (RTF 37), regardless of application scenario
- Only CTC-based models provide usable performance (RTF 0.014-0.020)
- Recommendation: Exclusively deploy CTC-based architectures; Whisper unsuitable

For Unknown Language Scenarios:
- Requires LID→ASR pipeline
- LID accuracy determines system reliability
- [Detailed recommendations pending LID results]
- Recommendation: If LID accuracy exceeds 95%, automatic pipeline viable; otherwise request explicit language selection

### 5.3.2 Deployment Architecture Recommendations

Single Known Language:
Deploy a single model instance conditioned on that language. Language-hinted mode eliminates LID overhead and error risk.

Multiple Known High-Resource Languages:
Option 1: Deploy unified multilingual model (Whisper or OmniLingual LLM) with language hints
Option 2: Deploy CTC models for maximum speed if accuracy acceptable
Trade-off: Unified model simplicity versus CTC speed advantage

Multiple Languages Including Low-Resource:
Deploy OmniLingual CTC models exclusively; Whisper unsuitable due to low-resource language failures.

Unknown Languages Requiring Automatic Detection:
Deploy Whisper with LID if languages are high-resource, accepting 2× speed penalty for convenience. Deploy OmniLingual with separate LID model if including low-resource languages, as Whisper unsuitable for low-resource transcription regardless of LID performance.

### 5.3.3 Hardware and Scaling Considerations

CPU Deployment (Edge Devices, Cost-Sensitive):
- OmniLingual CTC models only viable option
- Whisper too slow even for high-resource languages on CPU (RTF 0.5-2× approaching or exceeding real-time)
- Recommendation: CTC-only deployment; Whisper unsuitable for CPU production use

GPU Deployment (Server-Side, Cloud):
- GPU acceleration significantly improves Whisper speed (though Mongolian likely remains problematic)
- OmniLingual maintains substantial speed advantage even on GPU
- Recommendation: Evaluate GPU-accelerated Whisper for high-resource languages; maintain CTC fallback for low-resource languages

Mobile Deployment:
- Extreme resource constraints favor lightweight models
- OmniLingual CTC 300M (smallest evaluated) most suitable
- Recommendation: Deploy 300M CTC variant; larger models impractical for on-device inference

## 5.4 Limitations

### 5.4.1 Dataset Limitations

Common Voice Characteristics: The evaluation employed read speech from Common Voice, which exhibits cleaner audio and more careful articulation than spontaneous conversational speech. Performance may degrade in realistic scenarios with background noise, overlapping speakers, disfluencies, and informal language.

Duration Range: Audio samples predominantly fall in the 0-10 second range, limiting analysis of long-form audio behavior. Preliminary testing on long-form French audio (120-240 seconds) revealed interesting patterns: language detection remained stable (all samples correctly identified as French with confidence 1.0), but WER exhibited substantial variation both across samples (0.19-0.99) and within samples across time windows. Common error types included name recognition failures, diacritic errors, and progressive degradation of complex phrases. However, no complete language model collapse occurred, suggesting Whisper maintains linguistic coherence in long-form scenarios despite accumulating transcription errors. Systematic long-form evaluation across all languages would reveal whether these patterns generalize or prove language-specific.

Code-Switching: The evaluation employed monolingual audio from Common Voice, where each sample contains a single language. This design choice enabled controlled language-specific performance analysis but limited direct observation of code-switching scenarios where speakers alternate between languages mid-utterance. To partially address this gap, a small-scale experiment concatenated short utterances from different languages (Spanish→Mongolian, French→Hungarian→Spanish, Mongolian→Spanish→French) and transcribed the resulting sequences with Whisper’s built-in LID enabled. In all cases, the system produced effectively monolingual transcripts and reported a single detected language for the entire utterance (Spanish for the Spanish→Mongolian sequence, French for the French→Hungarian→Spanish and Mongolian→Spanish→French sequences), indicating that language identification is applied once at the utterance level rather than tracking intra-utterance language switches. Code-switching remains a challenging real-world phenomenon, particularly in multilingual communities, and systematic evaluation of robustness would still require specialized datasets (e.g., FLEURS with natural code-switching) or more controlled synthetic scenarios with segment-level language supervision.

Language Coverage: Only four languages were evaluated, representing a small fraction of linguistic diversity. Findings may not generalize to tonal languages (Mandarin, Vietnamese), languages with complex phonologies (Arabic with emphatic consonants), or languages with limited phonetic resources.

### 5.4.2 Experimental Limitations

CPU Evaluation: Whisper ran on CPU due to GPU compatibility issues, potentially exaggerating its speed disadvantage relative to GPU-accelerated OmniLingual models. However, the 74× Mongolian disparity far exceeds what GPU acceleration could reasonably eliminate, and CPU evaluation remains relevant for edge deployment scenarios.

Sample Size: 1000 samples per language provides statistical power for mean estimates but limits analysis of rare phenomena. Failure mode characterization, outlier analysis, and low-probability error patterns would benefit from larger evaluation sets.

Speaker Independence: The evaluation sampled from Common Voice's validated split without explicit speaker-level filtering. While test samples are independent from Whisper's training data (the model uses OpenAI's proprietary training corpus, not Common Voice), the 1000-sample test set per language may contain multiple utterances from the same speakers. This could potentially inflate performance estimates if models memorize speaker-specific characteristics. However, the large sample size (1000 per language) and diverse contributor base in Common Voice (typically 100+ unique speakers per language in the validated split) suggest that speaker-level dependencies have minimal impact on aggregate statistics. Future work should explicitly report speaker distribution statistics and conduct speaker-stratified evaluation to fully address this concern.

Model Selection: Only specific model variants were evaluated (Whisper-small, three OmniLingual variants). Larger Whisper models (medium, large) might exhibit different cross-language performance characteristics, though likely with even worse speed given their increased parameter count. Other CTC-based models (Wav2Vec2, XLSR-53) might show different patterns.

Decoding Strategy: The evaluation employed greedy decoding for all models to ensure consistency. Beam search decoding, which explores multiple hypotheses simultaneously, might improve accuracy at the cost of increased processing time. The accuracy-speed trade-off of beam search versus greedy decoding was not systematically evaluated, though preliminary testing suggested beam search provides marginal accuracy gains (typically <2% WER reduction) while substantially increasing inference time (2-5× slower). For the deployment-oriented focus of this thesis, greedy decoding represents the more practical baseline.

### 5.4.3 Metric Limitations

WER and CER Sensitivity: Both metrics prove sensitive to text normalization choices (punctuation handling, case normalization, number formatting). Different preprocessing decisions could shift absolute error rates, though relative comparisons across models and languages should remain stable.

RTF Limitations: RTF captures average speed but not latency distribution, startup overhead, or throughput under concurrent load. While resource profiling quantified CPU utilization and memory consumption (Chapter 4.4), production deployment requires additional metrics including 95th percentile latency, cold-start overhead, and sustained throughput with multiple concurrent requests.

Lack of Perceptual Evaluation: Automated metrics (WER, CER) imperfectly correlate with human-perceived transcription quality. Some errors prove more impactful than others (content word substitutions versus function word errors), and WER treats all errors equally. Human evaluation would provide complementary quality assessment.

### 5.4.4 Reproducibility Considerations

While comprehensive reproducibility measures were implemented (fixed random seed, version control, automated scripts, containerization), several factors may limit exact reproduction:

Hardware Variation: Performance metrics, particularly RTF, depend on hardware specifications. Different CPU/GPU models may exhibit different relative performance across models.

Software Updates: Library updates (PyTorch, Transformers, faster-whisper) may alter implementation efficiency or default configurations, affecting reported metrics.

Common Voice Updates: Future Common Voice versions may modify sample content, metadata, or quality, affecting evaluation datasets constructed with the same sampling procedure.

## 5.5 Positioning Relative to Prior Work

### 5.5.1 Consistency with Previous Findings

This evaluation confirms and extends several findings from prior multilingual ASR research:

Training Data Imbalance Effects: Previous work (Pratap et al., 2020; Conneau et al., 2020) documented accuracy degradation for low-resource languages in multilingual models. This evaluation demonstrates that the degradation extends beyond accuracy to processing efficiency, with low-resource languages experiencing catastrophic speed penalties.

Architecture Impact on Efficiency: Prior comparisons (Kim et al., 2021) established that autoregressive models exhibit higher latency than non-autoregressive alternatives. This work quantifies the magnitude of this effect across diverse languages, revealing that the disparity varies dramatically by language resource level (2-3× for high-resource, 70-100× for low-resource).

Cross-Lingual Transfer Benefits: The fact that OmniLingual models achieve competitive accuracy despite potential training data limitations demonstrates cross-lingual transfer effectiveness, consistent with findings from Wav2Vec2-XLS-R literature (Babu et al., 2021).

### 5.5.2 Novel Contributions

This work advances the field in several key dimensions:

First Systematic Low-Resource Efficiency Analysis: While prior work documented low-resource accuracy degradation, the 74× speed disparity for Mongolian represents a previously unquantified failure mode. This finding reveals that low-resource languages face not just accuracy challenges but fundamental deployment viability issues with current unified multilingual models.

Deployment-Oriented Evaluation: The emphasis on RTF alongside WER/CER provides practitioner-relevant guidance absent in much academic literature. Demonstrating that Whisper's Mongolian RTF of 36.98 renders it completely impractical shifts the discussion from abstract accuracy comparisons to concrete deployment decisions.

CTC Robustness Demonstration: The consistent OmniLingual performance across languages (RTF 0.014-0.024) demonstrates that architectural choices can eliminate language-dependent efficiency disparities. This finding suggests design principles for more equitable multilingual systems.

Reproducible Evaluation Framework: The comprehensive reproducibility measures (automated scripts, fixed seeds, containerization, documentation) enable independent verification and extension, addressing reproducibility concerns in ASR research.

### 5.5.3 Implications for Future Research

The findings suggest several research directions:

Architectural Solutions for Low-Resource Equity: CTC models demonstrate one approach to consistent cross-language performance. Future work should investigate whether other architectures (RNN-T, attention-free models) achieve similar robustness and whether encoder-decoder models can be modified to avoid low-resource degradation.

Training Objectives for Balanced Multilingual Learning: Standard cross-entropy training with imbalanced data produces the observed disparities. Alternative objectives (balanced sampling, language-specific loss weighting, multi-task learning) may improve low-resource language representation without sacrificing high-resource accuracy.

Efficiency-Oriented Model Design: The dramatic CTC speed advantages suggest that efficiency should be an explicit design objective alongside accuracy. Future models might target consistent RTF < 0.1 across all supported languages as a design requirement rather than evaluating efficiency post-hoc.

Low-Resource Language Benchmarking: The field lacks comprehensive benchmarks specifically evaluating low-resource language performance across both accuracy and efficiency dimensions. Future work should establish standardized evaluation protocols highlighting deployment viability rather than accuracy alone.

---

**End of Chapter 5**
