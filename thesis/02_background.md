# Chapter 2: Background and Related Work

This chapter provides the foundational concepts necessary to understand the multilingual ASR evaluation presented in this thesis. Section 2.1 introduces automatic speech recognition fundamentals, Section 2.2 discusses multilingual ASR challenges and approaches, Section 2.3 covers language identification techniques, and Section 2.4 reviews related work in this field.

## 2.1 Automatic Speech Recognition Fundamentals

### 2.1.1 Task Definition

Automatic Speech Recognition (ASR) is the computational task of converting spoken language audio into written text. Given an acoustic signal representing an utterance, the goal is to produce the most likely word sequence that corresponds to the spoken content.

Modern ASR systems have evolved from traditional Hidden Markov Model (HMM) approaches to neural network-based end-to-end models. These systems take raw audio or acoustic features as input and directly produce text transcriptions as output.

### 2.1.2 Neural ASR Architectures

Two major architectural paradigms dominate modern ASR:

Encoder-Decoder Models use a Transformer-based architecture where an encoder processes the acoustic input into hidden representations, and a decoder generates text tokens autoregressively. OpenAI Whisper is a prominent example, featuring multilingual capabilities with 244M parameters in its small variant. These models offer strong performance across diverse languages and conditions but suffer from slower inference due to sequential decoding.

Connectionist Temporal Classification (CTC) Models employ an encoder that maps audio to frame-level predictions with a special blank token allowing variable-length alignment. CTC decoders enable non-autoregressive parallel decoding, resulting in faster inference. The OmniLingual models evaluated in this thesis use CTC-based architectures, achieving significantly faster processing speeds compared to encoder-decoder approaches.

### 2.1.3 Evaluation Metrics

Word Error Rate (WER) is the standard metric for ASR evaluation, computed as the edit distance between hypothesis and reference at the word level:

WER = (S + D + I) / N × 100%

where S represents substitutions, D represents deletions, I represents insertions, and N represents total reference words. Lower WER indicates better performance, with WER = 0% representing perfect transcription.

Character Error Rate (CER) applies the same calculation at the character level. CER is particularly appropriate for morphologically rich languages such as Hungarian and Mongolian, where word-based metrics may not adequately reflect transcription quality.

Real-Time Factor (RTF) measures inference speed relative to audio duration:

RTF = Processing Time / Audio Duration

RTF < 1.0 indicates faster than real-time processing (suitable for live transcription), RTF = 1.0 represents real-time processing, and RTF > 1.0 indicates slower than real-time (batch-only scenarios). This metric is critical for deployment decisions.

## 2.2 Multilingual ASR

### 2.2.1 Motivation for Multilingual Systems

The world's approximately 7,000 languages represent diverse phonological systems, writing scripts, and grammatical structures. Developing separate monolingual ASR systems for each language is impractical due to resource constraints and deployment complexity.

Multilingual ASR systems address this challenge through two primary approaches: unified models that handle multiple languages with a single architecture, and specialized models fine-tuned for specific languages from a multilingual base. Each approach presents distinct trade-offs in accuracy, efficiency, and deployment complexity.

### 2.2.2 Technical Challenges

Phonetic and Phonological Variation presents a fundamental challenge. Different languages employ different sound inventories, ranging from Hawaiian with approximately 13 phonemes to languages with over 100 distinct sounds. A multilingual ASR system must learn representations that generalize across this diversity.

Orthographic Variation adds complexity through diverse writing systems. Latin, Cyrillic, Arabic, logographic, and syllabic scripts each require different tokenization and output representation strategies. The models evaluated in this thesis handle both Cyrillic (Mongolian) and Latin scripts (Hungarian, Spanish, French).

Morphological Complexity varies significantly across languages. Mongolian and Hungarian exhibit agglutinative morphology with extensive suffixing, while Spanish and French display fusional morphology. This variation affects both model training and evaluation metric selection.

Data Imbalance constitutes a critical challenge. High-resource languages like Spanish have tens of thousands of hours of transcribed speech, while low-resource languages like Mongolian often have fewer than 100 hours. Naive multilingual training can result in high-resource languages dominating learned representations, degrading low-resource language performance.

### 2.2.3 Multilingual Modeling Approaches

Joint Multilingual Training involves training a single model on pooled data from all target languages. This approach enables cross-lingual transfer, where low-resource languages benefit from high-resource data through shared phonetic representations. Whisper exemplifies this approach, trained on 680,000 hours of multilingual audio covering 99 languages.

Language-Specific Fine-Tuning begins with a multilingual pre-trained model, then fine-tunes separate models per language. This approach can achieve higher per-language accuracy through specialization but increases deployment complexity. Each language requires a separate model, multiplying storage and memory requirements.

The OmniLingual models evaluated in this thesis represent a hybrid approach: multilingual base models with language-conditioned decoding, allowing a single model to achieve language-specific performance through explicit language hints.

## 2.3 Language Identification

### 2.3.1 Task Definition and Role in ASR

Language Identification (LID) determines which language is spoken in an audio segment. For multilingual ASR deployment, LID serves two critical purposes: routing audio to appropriate language-specific systems in multi-model architectures, and conditioning multilingual models to expect a particular language.

LID integration introduces a fundamental trade-off. Automatic language detection eliminates the need for external language metadata, enabling fully automatic transcription. However, LID errors cascade into transcription errors when incorrect language identification leads to inappropriate model selection or conditioning.

### 2.3.2 LID Approaches

Standalone LID Models employ dedicated classifiers trained specifically for language prediction. Traditional approaches extract acoustic features (MFCCs, i-vectors) and train statistical classifiers. Modern neural approaches use CNNs or RNNs on spectrograms. These models offer optimized LID performance but require separate training data and deployment.

Joint LID-ASR Models integrate language identification as an auxiliary task during ASR training. Whisper exemplifies this approach, predicting language from the same encoder representations used for transcription. This eliminates the need for a separate LID model and ensures consistent acoustic processing, though LID accuracy depends on ASR model quality.

### 2.3.3 LID Error Propagation

In a LID→ASR pipeline, language identification errors directly impact transcription quality. When LID correctly identifies the language, appropriate model conditioning leads to accurate transcription. When LID fails, incorrect language conditioning produces degraded or completely incorrect transcriptions.

This cascading error effect makes LID accuracy critical for automatic multilingual ASR deployment. High LID accuracy (>95%) is generally considered necessary for production systems, though acceptable thresholds depend on application requirements and error tolerance.

## 2.4 Related Work

### 2.4.1 OpenAI Whisper

Whisper, released by OpenAI in 2022, represents a landmark achievement in multilingual ASR. The model was trained using large-scale weak supervision on 680,000 hours of multilingual audio scraped from the internet with noisy labels.

The architecture employs a Transformer encoder-decoder design ranging from 39M (tiny) to 1.5B (large) parameters. A single model handles 99 languages through language-conditioned decoding, where the decoder is explicitly informed which language to expect.

Key findings from the original Whisper paper include competitive performance with state-of-the-art systems on English benchmarks, strong zero-shot transfer to other languages, and robustness to acoustic variations including noise, accents, and recording conditions. However, limitations include hallucination (generating plausible but incorrect text, especially on silence or music), lower accuracy on low-resource languages compared to specialized models, and slower inference due to autoregressive decoding.

For this thesis, Whisper represents the unified multilingual approach, where one model handles all languages with minimal deployment complexity but potential per-language performance trade-offs.

### 2.4.2 OmniLingual and CTC-Based Models

OmniLingual represents a family of multilingual ASR models designed specifically for efficient cross-lingual performance. These models employ CTC-based architectures, enabling non-autoregressive decoding for significantly faster inference compared to encoder-decoder models.

The models evaluated in this thesis include three OmniLingual variants: CTC 300M (lightweight, optimized for speed), CTC 1B (larger, higher accuracy), and LLM 1B (best accuracy with language model integration). All variants support language-hinted mode where the target language is explicitly specified.

CTC-based models offer distinct advantages for deployment: parallel decoding enables real-time processing on modest hardware, simpler architecture reduces computational requirements, and consistent speed across languages avoids the variable latency issues observed in some encoder-decoder models.

### 2.4.3 Common Voice Dataset

Mozilla Common Voice represents a crowdsourced multilingual speech dataset designed to democratize voice technology. The dataset includes validated recordings across 100+ languages, with metadata including demographic information and recording quality metrics.

Version 23.0, used in this thesis, represents a substantial update with improved data quality and expanded language coverage. The dataset's open license and comprehensive metadata make it ideal for reproducible research, though limitations include predominantly read speech, clean recording conditions, and relatively short utterances (typically 5-15 seconds).

Previous studies using Common Voice have established baseline performance metrics across languages, though direct comparisons are often complicated by version differences and varying evaluation protocols.

### 2.4.4 Language-Specific ASR Development: Chimege

Chimege represents a specialized Mongolian ASR system developed specifically to address the unique challenges of Mongolian speech recognition. Unlike general-purpose multilingual models, Chimege focuses exclusively on Mongolian, employing language-specific optimizations including custom tokenizers trained on Mongolian text corpora and substantially larger Mongolian-specific training datasets exceeding the Mongolian portion of Common Voice.

The Chimege team reports achieving 2-3% WER on domain-specific Mongolian speech, representing state-of-the-art performance for models under 1 billion parameters. This performance level substantially exceeds what general multilingual models achieve on Mongolian, demonstrating the effectiveness of language-specific development approaches.

Chimege's research provides critical insights into Mongolian ASR challenges. Their analysis reveals that standard multilingual model implementations suffer from tokenization inefficiency (character-level tokenization for Mongolian versus word-level for English) and inference library optimization bias favoring common languages. These findings inform the interpretation of cross-language performance disparities observed in this thesis.

The Chimege approach exemplifies the specialized language-specific strategy, achieving superior accuracy for a single language at the cost of requiring separate development effort and deployment for each target language. This contrasts with the unified multilingual approach represented by Whisper, which offers broader language coverage but potentially lower per-language performance.

### 2.4.5 Research Gaps

Despite extensive prior work, several practical questions remain underexplored:

Multilingual Convenience versus Specialized Accuracy: Most studies compare architectures within a single approach. Direct comparison of unified multilingual models against language-specific specialized models on identical hardware and test sets remains limited.

Processing Efficiency Across Resource Levels: While accuracy degradation for low-resource languages is well-documented, processing speed disparities have received less attention. The extent to which multilingual models exhibit variable efficiency across languages of different resource levels requires systematic investigation.

LID Impact Quantification: The performance gap between automatic language detection (LID→ASR) and explicit language hints is often mentioned but rarely rigorously quantified across diverse languages representing different resource levels and linguistic characteristics.

Deployment-Oriented Evaluation: Academic benchmarks focus primarily on WER and CER. Practical deployment requires holistic evaluation including processing speed, resource utilization, and operational trade-offs, which remain underrepresented in literature.

This thesis addresses these gaps through a comprehensive, reproducible comparison of multilingual ASR approaches with deployment-relevant metrics, explicit focus on low-resource language performance, and systematic evaluation of both LID→ASR and language-hinted inference modes.

---

**End of Chapter 2**
