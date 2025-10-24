# Background: Automatic Speech Recognition and Language Identification

## 1. Overview
Automatic Speech Recognition (ASR) converts speech waveforms into text. 
Modern ASR systems rely on deep neural architectures trained on massive multilingual datasets. 
They commonly process 16 kHz mono audio and output time-aligned tokens.

## 2. Language Identification (LID)
LID predicts the language of an input segment. 
Accurate LID enables selecting or constraining the ASR model’s language head, improving recognition quality and reducing hallucinations. 
Whisper, for example, jointly predicts a language token before transcription.

## 3. Multilingual Strategies
Typical strategies:
- **Unified multilingual model** — one shared model for all languages (e.g., Whisper, XLS-R).
- **Cascade (LID → ASR)** — a light LID model selects which ASR to use.
- **Hinted / oracle mode** — language is given by metadata.
- **Adaptive decoding** — dynamic switching when code-switching is detected.

## 4. Metrics
Core metrics in this work:
- **Word Error Rate (WER)** and **Character Error Rate (CER)** for quality.
- **LID accuracy** for language prediction reliability.
- **Real-Time Factor (RTF)**, **CPU %**, and **memory (RSS/VRAM)** for efficiency.

## 5. Relevance to Thesis
This study compares LID→ASR vs Hinted modes across four languages (MN, HU, FR, ES) using Whisper and NeMo.  
The goal is to quantify the trade-offs between automatic language detection and oracle language forcing, 
and evaluate the performance impact on low-resource and typologically diverse languages.
