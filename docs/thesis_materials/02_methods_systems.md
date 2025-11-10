# Methods: ASR Systems Evaluated

## For Thesis

### 3.2 Automatic Speech Recognition Systems

Two state-of-the-art multilingual ASR systems with contrasting architectures were evaluated to provide a comprehensive analysis of multilingual speech recognition approaches.

#### 3.2.1 System 1: OpenAI Whisper

**Architecture**: Transformer-based encoder-decoder (sequence-to-sequence)

**Description**: Whisper [Radford et al., 2022] is a supervised multilingual ASR system trained on 680,000 hours of labeled audio data. The model employs an encoder-decoder architecture with cross-attention mechanisms, enabling robust performance across diverse acoustic conditions and languages.

**Key Characteristics**:
- **Training Paradigm**: Supervised learning on weakly-supervised internet audio
- **Multilingual Support**: 99 languages including the target languages (MN, HU, FR, ES)
- **Built-in Language Identification**: Integrated LID as part of the inference pipeline
- **Decoding**: Autoregressive beam search with language modeling

**Model Variants Evaluated**:
- **Whisper-tiny**: 39M parameters (baseline, CPU-feasible)
- **Whisper-small**: 244M parameters (primary comparison model)
- **Whisper-base**: 74M parameters (GPU evaluation) [if tested]

**Implementation**: `openai-whisper` Python library, with custom wrappers (`scripts/run_whisper.py`) for standardized evaluation.

**Language Identification**: Whisper's built-in LID analyzes the first 30 seconds of audio using the encoder's internal representations. The model outputs probability distributions over all supported languages, from which we extract:
- Predicted language (argmax)
- Confidence score (probability of predicted language)
- Full distribution for confusion analysis

---

#### 3.2.2 System 2: Wav2Vec2-XLS-R

**Architecture**: Self-supervised encoder with CTC (Connectionist Temporal Classification) decoder

**Description**: Wav2Vec2-XLS-R [Babu et al., 2021] is a cross-lingual speech representation model pre-trained using self-supervised learning on 436,000 hours of unlabeled multilingual speech. The model uses a convolutional encoder followed by transformer layers, with a CTC head for alignment-free decoding.

**Key Characteristics**:
- **Training Paradigm**: Self-supervised pre-training + supervised fine-tuning
- **Multilingual Support**: 128 languages (largest coverage among evaluated systems)
- **Language Identification**: Not built-in; requires external LID or language hints
- **Decoding**: Non-autoregressive CTC, enabling parallel processing

**Model Evaluated**:
- **Wav2Vec2-XLS-R-300M**: 300M parameters

**Implementation**: Hugging Face `transformers` library with custom wrapper (`scripts/asr_wav2vec2.py`) matching Whisper's interface for fair comparison.

**Language Identification Approach**: 
Since Wav2Vec2-XLS-R lacks built-in LID, two strategies were employed:
1. **Hinted Mode**: Language explicitly provided (oracle scenario)
2. **LID→ASR Mode**: [Specify approach: Whisper's LID reused OR filename inference]

---

### 3.3 Architectural Comparison

| Aspect | Whisper | Wav2Vec2-XLS-R |
|--------|---------|----------------|
| **Architecture** | Encoder-Decoder | Encoder-CTC |
| **Training** | Supervised (labeled data) | Self-supervised + fine-tuned |
| **Decoding** | Autoregressive (sequential) | Non-autoregressive (parallel) |
| **LID Support** | Built-in | External required |
| **Parameters** | 244M (small) | 300M |
| **Training Data** | 680K hours (labeled) | 436K hours (unlabeled) |
| **Speed** | Slower (sequential decode) | Faster (parallel decode) |

**Rationale for Selection**:
These systems represent different design philosophies in multilingual ASR:
- **Whisper**: End-to-end supervised approach optimized for accuracy
- **Wav2Vec2**: Self-supervised representations optimized for efficiency and fine-tunability

This diversity enables analysis of trade-offs between accuracy, speed, and resource requirements relevant to practical deployment scenarios.

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
