# Background and Related Work

## For Thesis

### Chapter 2: Background and Related Work

This chapter provides the foundational concepts necessary to understand the multilingual ASR evaluation presented in this thesis. We first introduce automatic speech recognition fundamentals (Section 2.1), then discuss the specific challenges of multilingual ASR systems (Section 2.2), cover language identification approaches (Section 2.3), and conclude with a review of related work (Section 2.4).

---

## 2.1 Automatic Speech Recognition Fundamentals

### 2.1.1 Task Definition

Automatic Speech Recognition (ASR) is the computational task of converting spoken language audio into written text. Formally, given an acoustic signal $\mathbf{X} = (x_1, x_2, ..., x_T)$ representing an utterance, the goal is to produce the most likely word sequence $\mathbf{W} = (w_1, w_2, ..., w_N)$ that corresponds to the spoken content.

In probabilistic terms, ASR seeks to find:

$$\hat{\mathbf{W}} = \arg\max_{\mathbf{W}} P(\mathbf{W} | \mathbf{X})$$

Using Bayes' rule, this can be decomposed into:

$$P(\mathbf{W} | \mathbf{X}) = \frac{P(\mathbf{X} | \mathbf{W}) P(\mathbf{W})}{P(\mathbf{X})}$$

where:
- $P(\mathbf{X} | \mathbf{W})$ is the **acoustic model** (likelihood of audio given text)
- $P(\mathbf{W})$ is the **language model** (prior probability of word sequence)
- $P(\mathbf{X})$ is a normalization constant (can be ignored during maximization)

---

### 2.1.2 Neural ASR Architectures

Modern ASR systems are predominantly neural network-based, having largely replaced traditional Hidden Markov Model (HMM)-Gaussian Mixture Model (GMM) pipelines. Two major architectural paradigms dominate:

#### A. Encoder-Decoder (Sequence-to-Sequence) Models

**Architecture**: An encoder processes the acoustic input into a sequence of hidden representations, which a decoder then converts into text via autoregressive generation.

**Key Components**:
- **Encoder**: Typically a stack of Transformer layers or convolutional neural networks (CNNs) that extract acoustic features
- **Decoder**: Autoregressive model (e.g., Transformer decoder) that generates text tokens sequentially
- **Attention Mechanism**: Allows the decoder to focus on relevant parts of the encoded audio

**Example**: OpenAI Whisper [Radford et al., 2022] uses a Transformer encoder-decoder architecture.

**Advantages**:
- Implicit language modeling (decoder learns linguistic structure)
- Strong performance on diverse languages and conditions
- Can handle tasks beyond transcription (translation, timestamps)

**Disadvantages**:
- Slower inference (sequential decoding)
- Higher computational cost
- Prone to hallucination (generating plausible but incorrect text)

---

#### B. Connectionist Temporal Classification (CTC) Models

**Architecture**: An encoder maps audio to frame-level character/phoneme predictions, with a special "blank" token allowing variable-length alignment.

**Key Innovation**: CTC introduces a many-to-one mapping where multiple encoder timesteps can map to the same output token or to "blank" (silence/non-speech). This eliminates the need for pre-aligned training data.

**Example**: Wav2Vec2 [Baevski et al., 2020] uses a CTC decoder atop a self-supervised encoder.

**Advantages**:
- Non-autoregressive (parallel decoding is possible)
- Faster inference
- Simpler training (no external language model required initially)

**Disadvantages**:
- Limited implicit language modeling (purely frame-wise predictions)
- Often requires external language model for competitive accuracy
- Less flexible (typically transcription-only)

---

### 2.1.3 Evaluation Metrics

#### Word Error Rate (WER)

The standard metric for ASR evaluation, computed as the edit distance (Levenshtein distance) between hypothesis and reference at the word level:

$$\text{WER} = \frac{S + D + I}{N} \times 100\%$$

where $S$ = substitutions, $D$ = deletions, $I$ = insertions, $N$ = total reference words.

**Interpretation**: Lower is better. WER = 0% indicates perfect transcription. WER can exceed 100% if insertions are excessive.

**Limitations**:
- Insensitive to semantic equivalence (e.g., "don't" vs. "do not" counts as error)
- Word-based (problematic for morphologically rich languages)
- Requires normalized text (case, punctuation handling affects results)

#### Character Error Rate (CER)

Similar to WER but computed at the character level. More appropriate for:
- Morphologically rich languages (e.g., Hungarian, Turkish)
- Languages without clear word boundaries (e.g., Chinese, Japanese)
- Providing partial credit for near-correct words

#### Real-Time Factor (RTF)

Measures inference speed relative to audio duration:

$$\text{RTF} = \frac{\text{Processing Time}}{\text{Audio Duration}}$$

- RTF < 1.0: Faster than real-time (suitable for live transcription)
- RTF = 1.0: Real-time processing
- RTF > 1.0: Slower than real-time (batch-only scenarios)

---

## 2.2 Multilingual ASR Challenges

### 2.2.1 Motivation for Multilingual Systems

**Language Diversity**: The world's ~7,000 languages represent diverse phonological systems, writing scripts, and grammatical structures. Monolingual ASR systems are impractical at scale.

**Resource Inequality**: High-resource languages (English, Mandarin, Spanish) have abundant training data, while low-resource languages (Mongolian, Maori, many indigenous languages) lack sufficient data for monolingual training.

**Deployment Efficiency**: Multilingual models reduce deployment complexity by handling multiple languages with a single model, crucial for global applications (e.g., video subtitling, multilingual customer support).

---

### 2.2.2 Technical Challenges

#### A. Phonetic and Phonological Variation

Different languages use different sound inventories:
- **English**: ~44 phonemes
- **Hawaiian**: ~13 phonemes  
- **!Xóõ (Khoisan language)**: ~160 phonemes (including clicks)

A multilingual ASR system must learn representations that generalize across this diversity.

#### B. Orthographic Variation

Writing systems vary widely:
- **Alphabetic**: Latin, Cyrillic, Arabic scripts
- **Logographic**: Chinese characters
- **Syllabic**: Japanese Kana, Cherokee syllabary
- **Abjad**: Hebrew, Arabic (vowels often omitted)

This complicates text tokenization and output representation.

#### C. Morphological Complexity

Languages exhibit varying morphological typologies:
- **Analytic** (e.g., Mandarin): Minimal inflection, meaning conveyed by word order
- **Agglutinative** (e.g., Hungarian, Turkish): Extensive suffixing/prefixing
- **Fusional** (e.g., Spanish, Russian): Inflections encode multiple grammatical features

Word-based metrics like WER are less meaningful for highly agglutinative languages, where a single word might encode information equivalent to an English sentence.

#### D. Data Imbalance

Training data is highly skewed toward major languages:
- **English**: Tens of thousands of hours of transcribed speech
- **Low-resource languages**: Often fewer than 10 hours

Naive multilingual training can result in high-resource languages dominating the learned representations, degrading low-resource language performance.

---

### 2.2.3 Multilingual Modeling Approaches

#### A. Joint Multilingual Training

Train a single model on pooled data from all languages.

**Advantages**:
- Cross-lingual transfer: Low-resource languages benefit from high-resource data
- Shared phonetic representations (e.g., /p/ sound is similar across languages)

**Challenges**:
- High-resource languages may dominate learning
- Negative transfer: Conflicting phoneme-grapheme mappings across languages

**Mitigation Strategies**:
- Data upsampling/downsampling for balanced language representation
- Language-specific output layers or adapters
- Multi-task learning with auxiliary language identification

#### B. Language-Specific Fine-Tuning

Pre-train a multilingual model, then fine-tune separate models per language.

**Example**: Wav2Vec2-XLS-R [Babu et al., 2021] provides a pre-trained multilingual encoder, which is then fine-tuned with CTC heads for specific languages.

**Advantages**:
- Specialized models can achieve higher per-language accuracy
- Avoids negative transfer

**Disadvantages**:
- Increased deployment complexity (N models for N languages)
- Higher storage/memory requirements
- No cross-lingual generalization at inference time

---

## 2.3 Language Identification for ASR

### 2.3.1 Task Definition

Language Identification (LID) is the task of determining which language is spoken in an audio segment. For multilingual ASR, LID serves two purposes:

1. **Pre-processing**: Route audio to the appropriate language-specific ASR system
2. **Conditioning**: Inform a multilingual ASR system which language to expect

---

### 2.3.2 LID Approaches

#### A. Standalone LID Models

Dedicated classifiers trained to predict language from acoustic features.

**Traditional Approach**: Extract acoustic features (MFCCs, i-vectors) and train classifiers (GMM, SVM).

**Neural Approach**: Train CNNs or RNNs on spectrograms to predict language labels.

**Advantages**:
- Decoupled from ASR (can optimize LID independently)
- Lightweight (small models suffice for LID)

**Disadvantages**:
- Requires separate LID training data
- Potential mismatch between LID and ASR acoustic processing

#### B. Joint LID-ASR Models

Integrate LID as an auxiliary task during ASR training.

**Example**: Whisper [Radford et al., 2022] includes LID as part of its encoder, predicting language from the same representations used for transcription.

**Advantages**:
- Shared representations (LID benefits from ASR training data)
- No separate LID model needed
- Consistent acoustic processing

**Disadvantages**:
- LID accuracy depends on ASR model quality
- May not be optimized for LID task specifically

---

### 2.3.3 LID Error Propagation

In a LID→ASR pipeline, LID errors cascade into transcription errors:

**Case 1: Correct LID**
```
Audio (Spanish) → LID: Spanish ✓ → ASR(Spanish) → Correct transcript
```

**Case 2: Incorrect LID**
```
Audio (Spanish) → LID: French ✗ → ASR(French) → Garbled transcript
```

**Mitigation Strategies**:
1. **Confidence thresholding**: Only use LID prediction if confidence exceeds threshold; otherwise fall back to multilingual mode
2. **N-best LID**: Consider top-N language predictions and select ASR output with best internal score
3. **Code-switching handling**: Allow ASR to switch languages mid-utterance (advanced)

---

## 2.4 Related Work

### 2.4.1 OpenAI Whisper (2022)

**Key Innovation**: Large-scale weak supervision. Trained on 680,000 hours of multilingual audio scraped from the internet with noisy labels.

**Architecture**: Transformer encoder-decoder (74M to 1.5B parameters).

**Multilingual Approach**: Single model handles 99 languages via language-conditioned decoding.

**Findings** [Radford et al., 2022]:
- Competitive with state-of-the-art on English benchmarks (LibriSpeech)
- Strong zero-shot transfer to other languages
- Robust to acoustic variations (noise, accents, recording conditions)

**Limitations**:
- Hallucination: Can generate plausible but incorrect text, especially on silence or music
- Lower accuracy on low-resource languages compared to language-specific models
- Slower inference due to autoregressive decoding

**Relevance to This Work**: Whisper represents the **multilingual convenience** approach—one model handles all languages with minimal deployment complexity.

---

### 2.4.2 Wav2Vec2-XLS-R (2021)

**Key Innovation**: Self-supervised cross-lingual speech representation learning at scale.

**Architecture**: Convolutional encoder + Transformer layers, trained with masked prediction objective on 436,000 hours of unlabeled multilingual speech.

**Multilingual Approach**: Pre-trained multilingual encoder + language-specific CTC fine-tuning.

**Findings** [Babu et al., 2021]:
- Pre-training on multiple languages improves low-resource language performance via cross-lingual transfer
- Fine-tuned models achieve state-of-the-art results on BABEL and Common Voice benchmarks
- Self-supervised pre-training reduces labeled data requirements

**Limitations**:
- Requires fine-tuning for each target language (deployment complexity)
- CTC decoder limits flexibility (transcription-only, no language modeling)
- Pre-trained model is large (~300M parameters), and each fine-tuned model adds ~300M more

**Relevance to This Work**: Wav2Vec2-XLS-R represents the **language-specific specialization** approach—higher per-language accuracy at the cost of deployment complexity.

---

### 2.4.3 Comparative Studies

#### Multilingual vs. Monolingual Models

**[Pratap et al., 2020]**: Multilingual models benefit low-resource languages but may underperform monolinguals on high-resource languages.

**[Conneau et al., 2020]**: Cross-lingual transfer is most effective when pre-training languages share phonological or typological features.

#### LID Integration Strategies

**[Li et al., 2013]**: Explicit LID as a pre-processing step introduces latency and error propagation.

**[Watanabe et al., 2017]**: End-to-end multilingual models with implicit LID achieve comparable accuracy with lower latency.

#### Hardware and Deployment

**[Kim et al., 2021]**: Autoregressive models (encoder-decoder) have 3-5× higher latency than non-autoregressive (CTC) models on CPU, but the gap narrows on GPU.

**[Pratap et al., 2020]**: Quantization and model distillation can reduce multilingual model size by 4× with <5% WER degradation.

---

### 2.4.4 Research Gaps Addressed by This Thesis

Despite extensive prior work, several practical questions remain underexplored:

1. **Multilingual Convenience vs. Specialized Accuracy**: Most studies compare architectures within a single multilingual approach. Direct comparison of unified multilingual models (Whisper) against language-specific fine-tuned models (Wav2Vec2) on the **same** hardware and test set is limited.

2. **Model Scaling on Multilingual Tasks**: While Whisper paper reports accuracy across model sizes, the speed-accuracy trade-off for multilingual deployment (especially on consumer hardware) lacks detailed analysis.

3. **LID Impact Quantification**: The performance gap between oracle (language-hinted) and automatic (LID→ASR) modes is often mentioned but rarely rigorously quantified across diverse languages.

4. **Deployment-Oriented Evaluation**: Academic benchmarks focus on WER; practical deployment requires holistic evaluation including latency, memory, and coverage trade-offs.

**This thesis addresses these gaps** by providing a controlled, reproducible comparison of multilingual ASR approaches with deployment-relevant metrics.

---

## Key Takeaways

✅ **ASR is a mature field** with neural methods now dominant  
✅ **Multilingual ASR is essential** due to language diversity and resource inequality  
✅ **Two paradigms exist**: Unified multilingual models vs. language-specific specialization  
✅ **LID integration** is critical but introduces complexity and potential errors  
✅ **Prior work** has established strong baselines but leaves deployment trade-offs underexplored  

**This thesis contributes** a rigorous, deployment-focused comparison of these approaches.

---

## References

- Radford, A., et al. (2022). "Robust Speech Recognition via Large-Scale Weak Supervision." *arXiv:2212.04356*.
- Babu, A., et al. (2021). "XLS-R: Self-supervised Cross-lingual Speech Representation Learning at Scale." *arXiv:2111.09296*.
- Baevski, A., et al. (2020). "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations." *NeurIPS 2020*.
- Pratap, V., et al. (2020). "Massively Multilingual ASR: 50 Languages, 1 Model, 1 Billion Parameters." *Interspeech 2020*.
- Conneau, A., et al. (2020). "Unsupervised Cross-lingual Representation Learning for Speech Recognition." *Interspeech 2020*.
- Li, H., et al. (2013). "An Overview of Spoken Language Recognition: From GMM-UBM to Deep Neural Networks." *arXiv:1303.1609*.
- Watanabe, S., et al. (2017). "Language Independent End-to-End Architecture for Joint Language Identification and Speech Recognition." *ASRU 2017*.
- Kim, S., et al. (2021). "Comparison of Neural Speech Recognition Architectures for Edge Deployment." *ICASSP 2021*.

---

## TODO
- [ ] Add full citations to bibliography
- [ ] Verify all statistics (training hours, parameter counts)
- [ ] Add figure: ASR architecture comparison diagram
- [ ] Add figure: Multilingual training data distribution
- [ ] Cross-reference with Methods chapter sections
