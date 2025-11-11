# Methods: ASR Systems Evaluated

## For Thesis

### 3.2 Automatic Speech Recognition Systems

This study evaluates two contrasting approaches to multilingual ASR: (1) a unified multilingual model (Whisper) that handles all languages with a single system, and (2) language-specific specialized models (Wav2Vec2-XLSR-53) that are fine-tuned for individual languages. This comparison enables analysis of the trade-offs between multilingual convenience and language-specific optimization.

#### 3.2.1 OpenAI Whisper

**Architecture**: Transformer-based encoder-decoder (sequence-to-sequence)

**Description**: Whisper [Radford et al., 2022] is a supervised multilingual ASR system trained on 680,000 hours of labeled audio data. The model employs an encoder-decoder architecture with cross-attention mechanisms, enabling robust performance across diverse acoustic conditions and languages.

**Key Characteristics**:
- **Training Paradigm**: Supervised learning on weakly-supervised internet audio
- **Multilingual Support**: 99 languages including the target languages (MN, HU, FR, ES)
- **Built-in Language Identification**: Integrated LID as part of the inference pipeline
- **Decoding**: Autoregressive beam search with language modeling

**Model Variants Evaluated**:

To assess the impact of model capacity on both accuracy and computational requirements, three Whisper variants were evaluated:

| Model | Parameters | Layers | Width | Use Case |
|-------|-----------|---------|-------|----------|
| Whisper-tiny | 39M | 4 encoder + 4 decoder | 384 | Resource-constrained devices |
| Whisper-base | 74M | 6 encoder + 6 decoder | 512 | Balanced performance |
| Whisper-small | 244M | 12 encoder + 12 decoder | 768 | Primary evaluation model |

- **Whisper-tiny**: Serves as a baseline for minimal-resource scenarios. Despite its small size, it demonstrates surprisingly robust performance on high-resource languages.

- **Whisper-base**: Represents a middle ground between efficiency and accuracy, suitable for edge deployment scenarios.

- **Whisper-small**: Primary evaluation model, offering strong multilingual performance while remaining computationally feasible for CPU evaluation.

**Rationale for Model Selection**: Larger variants (medium, large) were excluded due to CPU inference time constraints exceeding practical thresholds (>5× real-time). The selected range (39M-244M parameters) spans a practical deployment spectrum from embedded systems to server-based applications.

**Implementation**: `faster-whisper` Python library (CTranslate2 backend) with custom evaluation wrappers (`scripts/run_whisper.py`) for standardized inference and metrics collection.

**Language Identification**: Whisper's built-in LID analyzes the first 30 seconds of audio using the encoder's internal representations. The model outputs probability distributions over all supported languages, from which we extract:
- Predicted language (argmax)
- Confidence score (probability of predicted language)
- Full distribution for confusion analysis

---

#### 3.2.2 Wav2Vec2-XLSR-53 (Language-Specific Models)

**Architecture**: Convolutional encoder + Transformer layers with CTC (Connectionist Temporal Classification) decoder

**Description**: Wav2Vec2-XLS-R [Babu et al., 2021] is a cross-lingual speech representation model trained via self-supervised learning on 436,000 hours of unlabeled multilingual speech across 128 languages. Unlike Whisper's unified multilingual approach, the XLSR-53 checkpoint serves as a foundation that is then fine-tuned for specific languages, resulting in specialized single-language models.

**Key Characteristics**:
- **Training Paradigm**: Self-supervised pre-training (masked prediction) + supervised fine-tuning per language
- **Architecture**: Non-autoregressive CTC decoding (parallel processing, faster inference)
- **Language Coverage**: Separate fine-tuned models per language (not a single multilingual model)
- **No Built-in LID**: Language must be known a priori (matches language-hinted evaluation mode)

**Language-Specific Models Evaluated**:

Due to availability constraints, only high-resource languages with reliable fine-tuned models were included:

| Language | Model ID | Parameters | Training Data |
|----------|----------|-----------|---------------|
| Spanish (ES) | `facebook/wav2vec2-large-xlsr-53-spanish` | 317M | Spanish Common Voice |
| French (FR) | `facebook/wav2vec2-large-xlsr-53-french` | 317M | French Common Voice |

**Note on Language Coverage**:
- Hungarian and Mongolian: No reliable fine-tuned models available on HuggingFace
- These languages are evaluated using Whisper only
- This limitation itself provides insight: multilingual models (Whisper) offer broader language coverage than relying on language-specific fine-tuning availability

**Rationale for Language-Specific Approach**:
Fine-tuning on language-specific data can yield higher accuracy for that language by specializing phoneme representations, word-piece vocabularies, and decoding strategies. However, this comes at the cost of:
1. **Deployment complexity**: Must deploy separate models for each language
2. **Resource requirements**: ~1.2GB per language model vs. 250MB for multilingual Whisper-small
3. **Coverage gaps**: Only languages with available fine-tuned models supported

**Implementation**: HuggingFace `transformers` library with custom evaluation wrapper (`scripts/run_wav2vec2.py`) matching the interface of `run_whisper.py` for fair comparison.

---

### 3.2.3 Inference Modes

Two inference modes were evaluated to assess the impact of language information on transcription quality and efficiency:

#### A. Language-Hinted Mode (Oracle Scenario)

In this mode, the correct target language is explicitly provided to the ASR system before inference. This represents an "oracle" scenario where perfect language identification is assumed.

**Implementation**:
```python
result = model.transcribe(
    audio_path,
    language="es",  # Explicitly specified
    task="transcribe"
)
```

**Use Case**: Applications where language context is known a priori (e.g., call center routing, language-specific services).

**Advantage**: Eliminates language identification errors, providing an upper bound on system performance.

#### B. LID→ASR Mode (Automatic Language Detection)

In this mode, the system first performs language identification on the audio, then uses the detected language for transcription.

**Implementation**:
```python
# Step 1: Language detection
detected_lang, confidence = model.detect_language(audio_path)

# Step 2: Transcription with detected language
if confidence >= threshold:
    result = model.transcribe(audio_path, language=detected_lang)
else:
    # Fallback to multilingual mode
    result = model.transcribe(audio_path, language=None)
```

**Use Case**: Real-world scenarios where language is unknown (e.g., multilingual customer support, media transcription).

**Challenge**: LID errors can cascade into transcription errors, potentially degrading overall system performance.

---

### 3.2.4 Evaluation Scope

**Primary Comparisons**:
1. **System Architectures**: Whisper (multilingual) vs. Wav2Vec2 (language-specific) on ES/FR
2. **Model Scaling**: Impact of model size (tiny → base → small) on Whisper performance
3. **Hardware Configurations**: CPU vs. GPU deployment scenarios
4. **Inference Modes**: Oracle (hinted) vs. automatic (LID→ASR) for Whisper
5. **Language Diversity**: High-resource (ES, FR) vs. medium-resource (HU) vs. low-resource (MN)

**Comparison Matrix**:

| Language | Whisper (tiny/base/small) | Wav2Vec2 (specialized) |
|----------|---------------------------|------------------------|
| Spanish (ES) | ✓ All 3 sizes | ✓ Language-specific model |
| French (FR) | ✓ All 3 sizes | ✓ Language-specific model |
| Hungarian (HU) | ✓ All 3 sizes | ✗ No model available |
| Mongolian (MN) | ✓ All 3 sizes | ✗ No model available |

**Research Questions Addressed**:
1. **Multilingual vs. Specialized**: Do language-specific models (Wav2Vec2-ES/FR) outperform a unified multilingual model (Whisper) on accuracy for high-resource languages?
2. **Model Scaling**: How does Whisper's accuracy and speed scale with model size (39M → 74M → 244M parameters)?
3. **Deployment Trade-offs**: What are the practical implications (memory, latency, coverage) of choosing multilingual vs. language-specific approaches?
4. **Resource Level**: How does Whisper's multilingual approach handle varying language resource levels (high/medium/low)?

---

## Supporting Data

**References**:
- Whisper paper: Radford et al. (2022) "Robust Speech Recognition via Large-Scale Weak Supervision"
- Wav2Vec2-XLS-R paper: Babu et al. (2021) "XLS-R: Self-supervised Cross-lingual Speech Representation Learning at Scale"
- Model cards: 
  - https://github.com/openai/whisper
  - https://huggingface.co/facebook/wav2vec2-large-xlsr-53-spanish
  - https://huggingface.co/facebook/wav2vec2-large-xlsr-53-french

**Code**:
- `scripts/run_whisper.py` - Whisper evaluation wrapper
- `scripts/run_wav2vec2.py` - Wav2Vec2 evaluation wrapper
- `scripts/lid_from_whisper.py` - Language identification using Whisper

---

## Key Points

✅ **Two contrasting approaches**: Multilingual (Whisper) vs. Language-specific (Wav2Vec2)  
✅ **Different architectures**: Encoder-decoder (seq2seq) vs. Encoder-CTC  
✅ **Contrasting training**: Supervised (680K hrs) vs. self-supervised + fine-tuned (436K hrs)  
✅ **Speed-accuracy trade-off**: Autoregressive vs. parallel decoding  
✅ **LID handling**: Built-in (Whisper) vs. not needed (Wav2Vec2 is language-specific)  
✅ **Coverage vs. specialization**: 4 languages (Whisper) vs. 2 languages (Wav2Vec2)  
✅ **Deployment complexity**: 1 model (Whisper) vs. N models (Wav2Vec2)  

**This comparison addresses the core thesis requirement of evaluating different multilingual ASR approaches!**

---

## Notes for Writing

- Emphasize the **multilingual strategy comparison**: unified vs. specialized
- This is more interesting than just "two popular models" - it's a fundamental design choice
- The limitation (only ES/FR for Wav2Vec2) actually strengthens the multilingual argument
- Cite original papers properly
- Link to implementation details in appendix
- Keep descriptions concise but complete

---

## TODO
- [x] Specify which Wav2Vec2 models used (language-specific ES/FR)
- [x] Clarify language coverage (Whisper: 4 langs, Wav2Vec2: 2 langs)
- [ ] Add proper citations to bibliography
- [ ] Add model download links to appendix
- [ ] Include model sizes in MB for deployment discussion
