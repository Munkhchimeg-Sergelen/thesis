# Methods: ASR Systems Evaluated

## For Thesis

### 3.2 Automatic Speech Recognition System

This study evaluates OpenAI Whisper, a state-of-the-art multilingual ASR system, across multiple model sizes and hardware configurations to assess the trade-offs between accuracy, speed, and resource requirements in multilingual speech recognition.

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

### 3.2.2 Inference Modes

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

### 3.3 Evaluation Scope

**Primary Comparisons**:
1. **Model Scaling**: Impact of model size (tiny → base → small) on accuracy and efficiency
2. **Hardware Configurations**: CPU vs. GPU deployment scenarios
3. **Inference Modes**: Oracle (hinted) vs. automatic (LID→ASR) language handling
4. **Language Diversity**: High-resource (ES, FR) vs. medium-resource (HU) vs. low-resource (MN)

**Rationale**: Rather than comparing different ASR architectures, this study provides an in-depth analysis of a single state-of-the-art system (Whisper) across multiple dimensions relevant to practical deployment. This approach yields actionable insights for system designers choosing appropriate configurations for specific use cases.

---

## Supporting Data

**References**:
- Whisper paper: Radford et al. (2022) "Robust Speech Recognition via Large-Scale Weak Supervision"
- Wav2Vec2-XLS-R paper: Babu et al. (2021) "XLS-R: Self-supervised Cross-lingual Speech Representation Learning at Scale"
- Model cards: 
  - https://github.com/openai/whisper
  - https://huggingface.co/facebook/wav2vec2-xls-r-300m

**Code**:
- `scripts/run_whisper.py` - Whisper evaluation wrapper
- `scripts/asr_wav2vec2.py` - Wav2Vec2 evaluation wrapper
- `scripts/lid_from_whisper.py` - Language identification using Whisper

---

## Key Points

✅ **Two systems**: Different architectures (encoder-decoder vs encoder-CTC)  
✅ **Contrasting training**: Supervised vs self-supervised  
✅ **Speed-accuracy trade-off**: Autoregressive vs parallel decoding  
✅ **LID handling**: Built-in vs external  
✅ **Comparable scale**: ~250-300M parameters

---

## Notes for Writing

- Cite original papers properly
- Emphasize architectural diversity (satisfies thesis requirement for comparison)
- Explain why these two systems (not just "popular models")
- Link to implementation details in appendix
- Keep descriptions concise but complete

---

## TODO
- [ ] Add proper citations to bibliography
- [ ] Specify which Wav2Vec2 fine-tuned model used (if language-specific)
- [ ] Clarify LID approach for Wav2Vec2 (Whisper reuse vs filename)
- [ ] Add model download links to appendix
- [ ] Include model sizes in MB for deployment discussion
