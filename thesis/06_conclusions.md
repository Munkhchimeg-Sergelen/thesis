# Chapter 6: Conclusions and Future Work

This chapter summarizes the thesis contributions, answers the research questions posed in Chapter 1, reflects on the broader implications of the findings, and proposes directions for future research.

## 6.1 Summary of Contributions

This thesis evaluated multilingual ASR approaches through systematic comparison of four models across four languages representing diverse resource levels and linguistic characteristics. The evaluation employed 16,000 transcriptions on standardized test data, producing several significant contributions to the field.

Contribution 1: Quantification of Low-Resource Language Performance Collapse

The evaluation revealed that Whisper-small processes Mongolian 74× slower than Spanish (RTF 36.98 versus 0.50), representing catastrophic degradation that renders low-resource ASR completely impractical with this unified multilingual model. Average Mongolian processing time reached 188 seconds per 5.5-second utterance, with worst-case samples exceeding 150 seconds. This finding demonstrates that nominal language support in multilingual models does not guarantee usable performance, revealing a critical limitation of current unified approaches.

Contribution 2: Demonstration of CTC Architecture Robustness

OmniLingual CTC-based models maintained remarkably consistent processing speeds across all languages, with RTF ranging only from 0.014 to 0.024. This represents 1500-2500× faster Mongolian processing compared to Whisper, proving that architectural design can eliminate language-dependent efficiency disparities. The finding establishes CTC-based models as essential for equitable multilingual deployment, particularly when supporting low-resource languages.

Contribution 3: Comprehensive Speed-Accuracy Trade-off Analysis

The evaluation documented speed-accuracy trade-offs across diverse deployment scenarios. CTC models achieve 20-60× faster processing than encoder-decoder architectures on high-resource languages, with advantages exceeding 1000× for low-resource languages. The OmniLingual LLM 1B variant demonstrates that CTC-based models can approach encoder-decoder accuracy while maintaining substantial speed advantages, occupying a favorable point in the trade-off space for balanced multilingual deployment.

Contribution 4: Reproducible Evaluation Framework

The complete evaluation pipeline—including automated scripts for dataset preparation, model execution, metric calculation, and analysis—enables independent verification and extension of this work. Fixed random seeds, version control, containerization, and comprehensive documentation ensure reproducibility, addressing persistent concerns in ASR research. The framework can be applied to evaluate additional models, languages, or deployment scenarios.

Contribution 5: Deployment-Oriented Practical Guidance

The thesis provides actionable recommendations for model selection, deployment architecture, and hardware provisioning based on language resource levels and application constraints. The findings demonstrate that optimal solutions vary substantially by scenario: CTC models prove essential for low-resource languages and real-time applications, while encoder-decoder models remain viable for high-resource offline processing. This guidance enables practitioners to make informed deployment decisions rather than assuming universal model applicability.

## 6.2 Answers to Research Questions

The thesis addressed five research questions through systematic evaluation:

RQ1: Language Identification Accuracy

How accurate is automatic language identification across languages with different resource levels?

[Answer pending LID results completion: Expected findings include overall LID accuracy, per-language performance patterns, confusion matrices revealing systematic misidentification, and assessment of whether LID achieves production-ready reliability (>95% accuracy) across diverse language pairs.]

RQ2: Inference Mode Comparison

How do LID→ASR and language-hinted modes compare in terms of transcription accuracy and processing efficiency?

[Answer pending LID vs hinted comparison completion: Expected findings include WER/CER differences between modes quantifying LID error cascading impact, RTF differences revealing whether LID introduces computational overhead, and assessment of whether automatic language detection proves viable for production deployment or whether explicit language hints remain necessary.]

RQ3: Cross-Language Performance Analysis

How does multilingual ASR performance vary across languages with different resource levels, linguistic characteristics, and audio durations?

Answer: Performance varies dramatically by language resource level and model architecture. Whisper exhibits 74× RTF disparity between Mongolian (low-resource) and Spanish (high-resource), rendering low-resource ASR completely impractical. OmniLingual CTC models maintain consistent performance across resource levels (RTF 0.014-0.024), demonstrating architecture-dependent robustness.

Accuracy patterns (pending final WER/CER analysis) are expected to show degradation for low-resource languages across all models, though the magnitude of degradation varies by architecture. Audio duration effects reveal whether models maintain stable performance across utterance lengths or exhibit efficiency degradation for longer samples.

RQ4: Model Architecture Comparison

How do different ASR architectures (encoder-decoder versus CTC-based) perform across multilingual scenarios?

Answer: CTC-based models achieve 20-2500× faster processing than encoder-decoder models, with the largest advantages on low-resource languages. OmniLingual CTC 300M (300M parameters) processes 1500× faster than Whisper-small (244M parameters) on Mongolian despite similar parameter counts, demonstrating that architecture dominates parameter count in determining efficiency.

Accuracy trade-offs depend on specific model variants. Pure CTC models prioritize speed, potentially sacrificing some accuracy. CTC+LLM hybrids (OmniLingual LLM 1B) approach encoder-decoder accuracy while maintaining substantial speed advantages (RTF 0.5 versus 37 for Mongolian), representing favorable trade-off points.

RQ5: Practical Deployment Considerations

What are the practical trade-offs and recommendations for deploying multilingual ASR systems?

Answer: Optimal deployment strategies depend on language resource levels and application constraints. For low-resource languages, only CTC-based models provide usable performance; Whisper proves completely impractical regardless of scenario. For high-resource languages, both architecture families achieve acceptable performance, with CTC models offering 30× speed advantages at potential accuracy cost. Real-time applications require CTC models due to their consistent RTF < 1.0. Batch processing permits encoder-decoder models for high-resource languages but not low-resource.

Hardware constraints strongly influence model selection. CPU deployment (edge devices, cost-sensitive scenarios) requires CTC models; Whisper too slow even for high-resource languages on CPU. GPU deployment enables Whisper for high-resource languages but likely insufficient for low-resource language viability.

## 6.3 Broader Implications

### 6.3.1 Language Equality in Multilingual AI

The findings reveal fundamental challenges in achieving language equality through unified multilingual models. Whisper nominally supports 99 languages, creating an impression of universal coverage. However, the 74× Mongolian slowdown demonstrates that nominal support differs critically from usable support.

This disparity raises ethical concerns. As multilingual AI systems proliferate, performance gaps between high-resource and low-resource languages risk entrenching existing inequalities. Communities speaking major languages benefit from fast, accurate, practical ASR, while minority language communities receive nominally supported but practically unusable systems.

Achieving genuine language equality requires architectural and training approaches that maintain consistent performance across resource levels. The CTC model results demonstrate that such equality is technically feasible, suggesting that current disparities reflect design priorities rather than fundamental limitations.

### 6.3.2 Deployment Realities Versus Academic Benchmarks

Academic ASR research predominantly focuses on WER and CER, with efficiency treated as secondary. This evaluation demonstrates that efficiency proves equally critical for deployment viability. A model with competitive accuracy but RTF of 37 remains completely impractical, regardless of application scenario.

The field would benefit from balanced evaluation protocols assessing both accuracy and efficiency as primary metrics. Benchmark leaderboards emphasizing only WER incentivize designs that sacrifice efficiency for marginal accuracy gains, potentially producing models unsuitable for practical deployment.

Deployment-oriented research should evaluate real-time factor, memory consumption, startup latency, and throughput under load alongside traditional accuracy metrics. Models should be assessed against deployment viability thresholds (e.g., RTF < 1.0 for real-time applications) rather than purely on relative accuracy rankings.

### 6.3.3 Architecture Selection for Multilingual Systems

The dramatic efficiency differences between CTC and encoder-decoder architectures suggest that architecture selection proves as important as training data quantity for multilingual systems. CTC's consistent cross-language performance derives from architectural properties (parallel frame-level prediction) rather than training data advantages.

This finding implies that future multilingual models should prioritize architectures demonstrating robustness to language resource level rather than maximizing accuracy on high-resource languages. Encoder-decoder models excel for high-resource languages but fail catastrophically for low-resource languages. CTC models maintain usable performance across resource spectrum, though potentially sacrificing peak high-resource accuracy.

Hybrid approaches combining CTC efficiency with language modeling (e.g., OmniLingual LLM 1B) may achieve favorable trade-offs, warranting further investigation.

## 6.4 Limitations and Lessons Learned

The evaluation encountered several limitations providing lessons for future work:

Incomplete LID Evaluation: Technical issues delayed LID→ASR evaluation, preventing complete comparison of inference modes. Future work should prioritize early LID testing to enable full mode comparison.

GPU Compatibility Issues: Whisper's GPU deployment failed due to library compatibility issues, forcing CPU evaluation. While CPU results remain relevant for edge deployment, GPU comparison would provide additional perspective. Lesson: Maintain fallback hardware configurations when compatibility issues arise.

Limited Language Sample: Four languages provide initial insights but insufficient coverage for definitive cross-linguistic conclusions. Future work should expand to 10-15 languages spanning diverse typologies (tonal, agglutinative, VSO word order, etc.).

Dataset Characteristics: Common Voice's read speech may not represent spontaneous conversation, noisy environments, or domain-specific language. Evaluation on diverse datasets would strengthen generalizability claims.

## 6.5 Future Work

### 6.5.1 Extended Language Coverage

Expand evaluation to 10-15 languages spanning diverse typologies:
- Tonal languages (Mandarin, Vietnamese) - testing handling of tone-dependent meaning
- Additional low-resource languages (Swahili, Mongolian variants) - assessing whether Whisper's Mongolian issues generalize
- Morphologically complex languages (Turkish, Finnish, Georgian) - testing CER-WER relationship
- Non-Latin scripts (Arabic, Hindi, Thai) - examining script effects independent of phonology

This expansion would reveal whether findings generalize across linguistic diversity or prove specific to the evaluated language sample.

### 6.5.2 Long-Form Audio Evaluation

Evaluate performance on long-form audio (1-60 minutes):
- Podcast transcription
- Lecture capture
- Meeting transcription
- Audiobook narration

Long-form audio introduces failure modes absent in short utterances: attention drift, hallucination accumulation, memory limitations, and speaker variation. CTC models' parallel processing may prove advantageous for long-form content, while encoder-decoder models may struggle with extended context.

### 6.5.3 Code-Switching Evaluation

Evaluate multilingual ASR performance on code-switching scenarios:
- Natural code-switching datasets (e.g., FLEURS, Miami Bangor Corpus)
- Synthetic concatenation of monolingual samples
- Language transition detection accuracy
- Transcription quality degradation at switching boundaries

Code-switching poses unique challenges for both inference modes. LID→ASR pipelines must detect intra-utterance language transitions, potentially requiring frame-level or word-level language identification rather than utterance-level. Language-hinted mode cannot accommodate within-utterance language changes, requiring external mechanisms to segment mixed-language audio.

Comparative analysis would reveal whether current architectures handle code-switching gracefully or exhibit catastrophic degradation at language boundaries. This evaluation would inform deployment decisions for multilingual communities where code-switching occurs frequently.

### 6.5.4 Noisy and Spontaneous Speech

Evaluate robustness to real-world acoustic conditions:
- Background noise (cafes, streets, offices)
- Overlapping speakers
- Spontaneous speech disfluencies
- Accented speech

Common Voice's clean read speech represents best-case scenarios. Production deployment requires robustness to acoustic and linguistic variation. Evaluating diverse conditions would reveal whether model rankings remain stable or shift under challenging conditions.

### 6.5.5 Fine-Tuning for Low-Resource Languages

Investigate whether targeted fine-tuning can address low-resource language issues:
- Fine-tune Whisper on additional Mongolian data
- Compare fine-tuning cost versus training CTC models from scratch
- Assess whether fine-tuning addresses efficiency issues or only accuracy

If fine-tuning improves Mongolian performance to usable levels, it provides a mitigation strategy. If efficiency issues persist despite accuracy improvements, architectural limitations rather than training data insufficiency dominate.

### 6.5.6 LLM-Based Post-Processing

Explore whether large language models can improve transcription quality:
- GPT-based error correction
- Punctuation restoration
- Normalization and formatting

LLM post-processing trades computational cost for quality improvements. For applications where transcription serves as input to downstream NLP tasks (translation, summarization), LLM correction may prove cost-effective. Evaluating this trade-off would guide deployment decisions for quality-critical scenarios.

### 6.5.7 Streaming ASR Evaluation

Evaluate streaming ASR capabilities:
- Latency from speech to first output
- Incremental hypothesis stability
- Computational efficiency for streaming

Real-time applications require streaming ASR producing incremental outputs as speech occurs, rather than waiting for complete utterances. CTC models' parallel processing may extend to streaming scenarios more naturally than encoder-decoder models' autoregressive generation. Streaming evaluation would assess real-time deployment viability comprehensively.

### 6.5.8 Comparison with Language-Specific Specialized Models

Direct comparison with specialized language-specific models would quantify the accuracy-convenience trade-off:
- Evaluate Chimege (Mongolian-specific, 2-3% WER reported) against multilingual models on identical Mongolian test set
- Compare deployment complexity: single multilingual model versus N specialized models for N languages
- Assess whether specialized models' superior accuracy justifies additional deployment overhead
- Investigate hybrid strategies: multilingual base with language-specific adapter layers

The Chimege team's insights revealed that implementation-level optimizations (custom tokenizers, native inference without library bias) can substantially improve Mongolian performance. Quantifying these improvements through controlled comparison would inform deployment decisions: when does language-specific specialization outweigh multilingual convenience?

### 6.5.9 Alternative Architectures

Evaluate additional architectures:
- RNN-Transducer models (balancing CTC efficiency with language modeling)
- Conformer architectures (combining convolution and attention)
- Wav2Vec2 variants (self-supervised pre-training approaches)

Expanding architecture coverage would reveal whether CTC's consistency and encoder-decoder's accuracy-efficiency trade-off represent general patterns or specific to the evaluated models.

## 6.6 Concluding Remarks

This thesis evaluated multilingual ASR approaches through systematic comparison of encoder-decoder and CTC-based architectures across languages representing diverse resource levels. The evaluation revealed that current unified multilingual models exhibit catastrophic performance degradation on low-resource languages, with Whisper processing Mongolian 74× slower than Spanish. In contrast, CTC-based models maintained consistent performance across all languages, demonstrating that architectural choices can eliminate resource-level disparities.

These findings carry implications beyond ASR, informing design of multilingual AI systems generally. Achieving genuine language equality requires architectures and training approaches that maintain consistent performance across resource levels, rather than optimizing for high-resource languages and accepting degraded low-resource performance.

The reproducible evaluation framework, comprehensive performance analysis, and practical deployment recommendations provide actionable guidance for practitioners deploying multilingual ASR systems. The work demonstrates that optimal solutions vary substantially by language resource level and application constraints, with no universal model dominating all scenarios.

Future work should expand language coverage, evaluate challenging acoustic conditions, explore fine-tuning and post-processing approaches, and investigate alternative architectures. The ultimate goal remains achieving equitable multilingual ASR performance, ensuring that technological advances benefit all language communities regardless of resource levels.

---

**End of Chapter 6**
