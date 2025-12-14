# Chapter 3: Methodology

This chapter describes the evaluation methodology employed to compare multilingual ASR approaches. Section 3.1 outlines the overall evaluation framework, Section 3.2 details language and dataset selection, Section 3.3 describes the ASR systems evaluated, Section 3.4 explains the two inference modes tested, Section 3.5 defines evaluation metrics, and Section 3.6 documents the experimental setup and reproducibility measures.

## 3.1 Evaluation Framework

The evaluation framework was designed to address the research questions through systematic comparison of multilingual ASR systems across diverse languages, representing different resource levels and linguistic characteristics. The framework emphasizes reproducibility, controlled experimental conditions, and deployment-relevant metrics.

The evaluation comprises three main components: system comparison (unified multilingual versus language-specific models), inference mode comparison (LID→ASR versus language-hinted), and cross-language performance analysis (high-resource versus low-resource languages).

All experiments were conducted on identical hardware using standardized evaluation protocols. Random sampling employed a fixed seed (42) to ensure reproducibility. The framework includes comprehensive documentation, automated scripts, and containerized environments to enable independent verification of results.

## 3.2 Languages and Dataset

### 3.2.1 Language Selection

Four languages were selected to represent diverse linguistic characteristics and resource levels:

Mongolian (mn) represents a low-resource language with approximately 5.2 million native speakers. It employs Cyrillic script and exhibits agglutinative morphology, where words are formed through extensive suffixing. Mongolian presents particular challenges for ASR due to limited training data availability and complex morphological structure.

Hungarian (hu) constitutes a medium-resource language with approximately 13 million native speakers. Like Mongolian, Hungarian exhibits agglutinative morphology but uses Latin script. This combination allows analysis of morphological complexity effects independent of script differences.

Spanish (es) and French (fr) represent high-resource languages with approximately 559 million and over 300 million native speakers respectively. Both employ Latin script and fusional morphology, where inflections encode multiple grammatical features simultaneously. These languages benefit from abundant training data and extensive prior research.

This language selection enables controlled comparison across resource levels (low, medium, high), scripts (Cyrillic, Latin), and morphological typologies (agglutinative, fusional).

### 3.2.2 Dataset Selection and Preparation

Mozilla Common Voice version 23.0 (September 2025 release) served as the primary data source. Common Voice provides crowdsourced speech recordings with validated transcriptions across 100+ languages under an open license, making it ideal for reproducible research.

The dataset preparation employed stratified random sampling with a fixed seed to ensure reproducibility. From each language's test split, 1000 samples were randomly selected. This sample size provides statistical power while remaining computationally feasible for comprehensive multi-model evaluation.

The sampling procedure guaranteed perfect alignment between audio files and reference transcripts by extracting both from the same TSV row in the Common Voice metadata. This eliminates data quality issues that plagued previous studies, where misaligned references could artificially inflate error rates.

Audio files were converted from the original MP3 format at 48kHz to a standardized format for processing. Reference transcripts underwent minimal normalization: lowercasing and basic punctuation removal, following standard ASR evaluation protocols.

The preparation script (prepare_v23_dataset.py) implements this procedure systematically:

```
python scripts/prepare_v23_dataset.py \
  --cv-base ~/cv-datasets/cv-corpus-23.0-2025-09-05 \
  --output-base data \
  --num-samples 1000 \
  --langs es fr hu mn \
  --seed 42
```

### 3.2.3 Dataset Statistics

The final dataset comprises 4000 audio samples (1000 per language) with corresponding reference transcripts. Audio duration statistics reveal characteristic differences across languages:

Spanish samples exhibit median duration of 4.06 seconds, representing concise conversational utterances typical of read speech in Common Voice. French samples show similar characteristics with median duration of 4.33 seconds.

Hungarian samples present slightly longer utterances with median duration of 4.17 seconds, potentially reflecting morphological complexity where agglutinative word formation produces longer surface forms.

Mongolian samples demonstrate the longest median duration at 5.51 seconds. This pattern may reflect multiple factors: agglutinative morphology producing longer words, script-specific reading patterns, or differences in speaking rate among Mongolian contributors to Common Voice.

Duration distribution analysis groups samples into buckets: short (0-5 seconds), medium (5-10 seconds), and long (10-30 seconds). This enables post-hoc analysis of audio length effects on model performance without introducing selection bias through pre-filtering.

## 3.3 ASR Systems

Four ASR systems representing different architectural approaches and parameter scales were evaluated:

### 3.3.1 Whisper-small

Whisper-small (OpenAI, 244M parameters) exemplifies the unified multilingual approach. The model employs a Transformer encoder-decoder architecture trained on 680,000 hours of weakly supervised multilingual audio covering 99 languages.

The encoder processes mel-spectrogram acoustic features through multi-layer Transformer blocks, producing contextual representations. The decoder generates text tokens autoregressively using attention over encoder outputs, incorporating an implicit language model through its training objective.

Whisper implements multilingual support through language-conditioned decoding: a language token prepended to the decoder input conditions the model to generate text in the specified language. Built-in language identification capability enables automatic language detection when no explicit language hint is provided.

Whisper was deployed using the faster-whisper library, which provides optimized inference through CTranslate2. The model ran on CPU for this evaluation due to GPU compatibility issues, though this configuration remains relevant for edge deployment scenarios.

### 3.3.2 OmniLingual CTC 300M

OmniLingual CTC 300M represents a lightweight CTC-based architecture optimized for speed. The model employs a convolutional encoder followed by Transformer layers, outputting frame-level character predictions with CTC blank tokens enabling variable-length alignment.

With 300M parameters, this model targets real-time applications where processing speed is critical. Non-autoregressive decoding enables parallel processing, avoiding the sequential dependencies that slow encoder-decoder models.

The model supports multilingual operation through language-conditioned encoding, where language embeddings modulate the encoder representations. This approach differs from Whisper's decoder-side conditioning but achieves similar multilingual capability.

### 3.3.3 OmniLingual CTC 1B

OmniLingual CTC 1B scales the lightweight architecture to 1 billion parameters, offering improved accuracy while maintaining CTC's speed advantages. The larger parameter count enables more nuanced acoustic modeling and better handling of acoustic variability.

Architecture and conditioning mechanisms remain consistent with the 300M variant, allowing direct comparison of parameter scaling effects on both accuracy and efficiency.

### 3.3.4 OmniLingual LLM 1B

OmniLingual LLM 1B integrates a language model component for enhanced accuracy. This variant processes CTC outputs through an additional language modeling stage, improving linguistic coherence and reducing recognition errors.

The additional LLM stage introduces modest computational overhead compared to pure CTC models but remains significantly faster than autoregressive encoder-decoder architectures like Whisper. This represents an intermediate point in the speed-accuracy trade-off spectrum.

## 3.4 Inference Modes

Two inference modes were evaluated to quantify the impact of language knowledge on system performance:

### 3.4.1 Mode A: LID→ASR Pipeline

The LID→ASR pipeline mode implements fully automatic multilingual transcription. The system receives audio without language metadata and must first identify the spoken language before transcribing.

For Whisper, built-in language identification executes during the initial encoder pass. The model analyzes acoustic features and predicts the most likely language through a classification layer. This prediction then conditions the decoder for transcription.

The pipeline introduces potential error cascading: incorrect language identification leads to inappropriate decoder conditioning, producing degraded or incorrect transcriptions. However, it eliminates the requirement for external language metadata, enabling deployment in scenarios where spoken language is unknown.

LID→ASR testing employed 100 samples per language (400 total), randomly selected from the main 1000-sample dataset. This subset size provides sufficient statistical power for LID accuracy estimation while limiting computational requirements.

### 3.4.2 Mode B: Language-Hinted ASR

Language-hinted mode represents the oracle scenario where correct language identity is provided to the system. This eliminates LID error cascading and represents optimal performance for language-conditioned models.

For Whisper, the language hint directly conditions the decoder without executing language identification. For OmniLingual models, the language embedding is specified explicitly, conditioning the encoder representations accordingly.

Language-hinted mode was evaluated on the full dataset (1000 samples per language, 4000 total). All four models support this mode, enabling comprehensive system comparison under controlled conditions.

### 3.4.3 Mode Comparison Methodology

Direct comparison between modes uses Whisper on identical test samples. The 100 samples per language tested in LID→ASR mode were also evaluated in language-hinted mode, providing paired observations for statistical analysis.

Performance differences between modes quantify the cost of automatic language detection in terms of both accuracy (WER/CER degradation) and efficiency (RTF overhead). This analysis addresses a key research question regarding the practical trade-offs between convenience and performance.

## 3.5 Evaluation Metrics

### 3.5.1 Word Error Rate (WER)

Word Error Rate quantifies transcription accuracy at the word level using edit distance:

WER = (Substitutions + Deletions + Insertions) / Reference Words × 100%

Implementation employed the jiwer Python library with standard tokenization. Both hypothesis and reference underwent identical preprocessing: lowercasing, punctuation removal, and whitespace normalization.

WER provides interpretable accuracy measurement for isolating languages like Spanish and French, where word boundaries are clear. However, WER has limitations for agglutinative languages where complex morphology produces long words that may be considered single errors despite multiple constituent errors.

### 3.5.2 Character Error Rate (CER)

Character Error Rate applies identical edit distance calculation at the character level:

CER = (Substitutions + Deletions + Insertions) / Reference Characters × 100%

CER provides more granular error measurement particularly appropriate for morphologically rich languages. For Hungarian and Mongolian, where single words may express concepts requiring multiple words in English, CER offers more meaningful performance assessment than WER.

Both metrics were computed for all models and languages, enabling complementary analysis of transcription quality.

### 3.5.3 Real-Time Factor (RTF)

Real-Time Factor quantifies processing speed relative to audio duration:

RTF = Processing Time / Audio Duration

RTF < 1.0 indicates faster than real-time processing, enabling live transcription applications. RTF = 1.0 represents real-time processing. RTF > 1.0 indicates slower than real-time, restricting deployment to batch processing scenarios.

Processing time measurement captured end-to-end transcription latency from audio input to text output, including all model operations (encoding, decoding, post-processing) but excluding file I/O.

RTF provides critical deployment guidance: systems with RTF > 1.0 cannot sustain real-time operation, regardless of transcription accuracy.

### 3.5.4 Language Identification Accuracy

LID accuracy measures correct language identification as a percentage:

LID Accuracy = Correct Predictions / Total Predictions × 100%

Additionally, a confusion matrix documents language pair confusability, revealing systematic misidentification patterns (e.g., Spanish-French confusion due to linguistic similarity).

LID accuracy analysis employed 400 samples (100 per language) in LID→ASR mode, providing statistically robust accuracy estimates with 95% confidence intervals of approximately ±10% per language.

### 3.5.5 Resource Usage Metrics

Resource consumption metrics quantify computational requirements for deployment feasibility assessment:

**CPU Utilization**: Percentage of CPU capacity consumed during transcription, measured continuously at 1-second intervals and reported as mean and peak values. CPU utilization indicates single-threaded processing efficiency and reveals whether models can share hardware with other services.

**Memory Consumption**: Peak RAM usage in gigabytes during model loading and inference. Memory requirements constrain deployment on resource-limited devices and determine hardware provisioning needs.

**GPU Utilization**: Percentage of GPU compute capacity used when models employ GPU acceleration. GPU metrics distinguish models requiring dedicated accelerators from those deployable on CPU-only systems.

Resource profiling employed 40 samples per model (10 per language) with continuous monitoring throughout transcription. The `psutil` library captured CPU and memory metrics, while `nvidia-smi` recorded GPU utilization when applicable. Measurements excluded file I/O to isolate model-specific resource consumption.

## 3.6 Experimental Setup and Reproducibility

### 3.6.1 Hardware Configuration

All experiments executed on a shared GPU server with the following specifications:

- GPU: 2× NVIDIA RTX A6000 (49GB VRAM each)
- CPU: Intel Xeon (specific model details in documentation)
- RAM: 64GB
- Storage: NVMe SSD (2TB)
- OS: Ubuntu 20.04 LTS

Whisper-small ran on CPU due to cuDNN compatibility issues with faster-whisper on this system configuration. While suboptimal for speed, CPU execution remains representative of edge deployment scenarios.

OmniLingual models executed on GPU 0, leveraging CUDA acceleration for efficient batch processing.

### 3.6.2 Software Environment

The software environment employed Conda for dependency management, ensuring reproducibility across systems. Key dependencies include:

- Python 3.10
- PyTorch 2.0+
- Transformers 4.30+
- faster-whisper 0.7+
- jiwer 3.0+
- Additional libraries documented in environment.yml

Complete environment specification enables reproduction on compatible hardware through:

```
conda env create -f environment.yml
conda activate omni
```

### 3.6.3 Execution Workflow

Experiments executed in parallel across four terminal sessions to maximize hardware utilization:

Terminal 1 ran Whisper-small transcription on CPU for all 4000 language-hinted samples plus 400 LID→ASR samples. Processing time: approximately 12-14 hours.

Terminals 2-4 ran OmniLingual variants (CTC 300M, CTC 1B, LLM 1B) on GPU concurrently, each processing 4000 language-hinted samples. Combined processing time: approximately 8-10 hours.

Results were stored in JSON format (metadata, timings, hypotheses) and plain text format (transcriptions), enabling both detailed analysis and straightforward reference comparison.

### 3.6.4 Reproducibility Measures

The evaluation implements comprehensive reproducibility measures:

Fixed Random Seed (42) ensures identical sample selection across independent runs, enabling exact reproduction of test sets.

Version Control tracks all code through Git, with specific commit hashes documented for the evaluation runs reported in this thesis.

Containerization provides an optional Docker environment replicating the exact software configuration, eliminating dependency version conflicts.

Automated Scripts implement the complete evaluation pipeline from dataset preparation through final analysis, minimizing manual steps that could introduce variance.

Comprehensive Documentation includes detailed setup instructions, script usage examples, and troubleshooting guidance in REPRODUCIBILITY_GUIDE.md.

The master execution script (run_complete_evaluation.sh) orchestrates the entire evaluation workflow:

```bash
bash scripts/run_complete_evaluation.sh \
  --data-dir data \
  --output-dir results \
  --models whisper omnilingual-ctc-300m omnilingual-ctc-1b omnilingual-llm-1b
```

This script handles dataset preparation, parallel model execution, results aggregation, metric calculation, and validation, producing publication-ready results with a single command.

All code, data preparation scripts, and documentation are publicly available in the thesis GitHub repository, enabling independent verification and extension of this work.

---

**End of Chapter 3**
