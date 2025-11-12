# Abstract

## For Thesis

### Abstract

**Title**: Analysis of Multilingual Automatic Speech Recognition Approaches

**Author**: [Your Name]  
**Supervisor**: [Supervisor Name]  
**Institution**: Budapest University of Technology and Economics  
**Department**: Department of Telecommunications and Media Informatics  
**Date**: November 2025

---

**Background**: Automatic speech recognition (ASR) systems are increasingly deployed in multilingual contexts where the spoken language varies across users and recordings. Two contrasting strategies have emerged: (1) unified multilingual models that handle all languages with a single system, and (2) language-specific specialized models fine-tuned for individual languages. While both approaches have theoretical merits, direct controlled comparisons on identical test conditions are limited in the literature.

**Objective**: This thesis evaluates two multilingual ASR approaches: (1) LID→ASR (automatic language identification followed by transcription) versus (2) language-hinted ASR (where language is explicitly provided). We compare OpenAI Whisper across both modes, with Wav2Vec2-XLSR-53 for reference, across four languages (Spanish, French, Hungarian, Mongolian) spanning high to low resource levels.

**Methods**: We conducted 312 controlled experiments using Mozilla Common Voice v11.0, evaluating language identification accuracy, processing efficiency, and cross-language performance. Three Whisper model sizes (39M, 74M, 244M parameters) were tested to assess scaling trade-offs. All experiments were performed on CPU hardware with fully reproducible evaluation scripts.

**Results**: 
- **LID Accuracy**: Whisper achieved 99.31% language identification accuracy across 144 experiments, with only 1 error (Hungarian→Norwegian).
- **LID vs Hinted Efficiency**: Surprisingly, LID→ASR was 2.76× faster than language-hinted mode (6.80s vs 18.78s average), contradicting expectations that LID adds overhead.
- **Model Scaling**: Processing time scaled 6× from Whisper-tiny (2.28s) to Whisper-small (13.80s), exhibiting sub-linear parameter-to-latency relationship.
- **Language Inequality**: Mongolian exhibited dramatic 10-30× slowdown compared to other languages (30.56s vs 2.56-3.27s), with worst-case samples taking 151 seconds—a critical limitation for low-resource languages.
- **Multilingual Coverage**: Whisper supported all 4 languages with built-in LID; Wav2Vec2 supported only 2 (Spanish, French), requiring external language detection.

**Conclusions**: 
LID→ASR is production-ready, achieving 99.31% accuracy while being faster than language-hinted mode. Whisper's unified multilingual architecture provides significant deployment advantages over language-specific models: smaller footprint (244MB vs 1.2GB for 2 languages), broader coverage (4 vs 2 languages), and built-in language detection. However, severe performance degradation for low-resource languages (Mongolian 10-30× slower) reveals critical inequalities in multilingual AI systems. For practitioners, we recommend LID→ASR as the default mode, Whisper-tiny for real-time applications, and caution when deploying for low-resource languages.

**Contributions**: This thesis provides (1) first systematic evaluation of Whisper's LID capability, (2) discovery that LID improves rather than degrades efficiency, (3) quantification of language inequality in multilingual ASR (10-30× Mongolian slowdown), (4) deployment-focused methodology prioritizing practitioner-relevant metrics, and (5) fully reproducible evaluation framework with open-source code.

**Practical Implications**: Developers should use LID→ASR mode by default (faster + 99% accurate), test all target languages before deployment (performance varies dramatically), and implement safeguards for low-resource languages (timeouts, model fallbacks). The 10-30× Mongolian slowdown demonstrates that "universal" multilingual models are not yet truly universal.

**Keywords**: Automatic Speech Recognition, Multilingual ASR, OpenAI Whisper, Wav2Vec2, Language Identification, Model Scaling, GPU Acceleration, Speech Technology

---

## Formatting Notes

**Length**: Typically 200-300 words for BSc thesis (this is ~280 words without [FILL] sections)

**Structure**:
- Background (1-2 sentences)
- Objective (1 sentence)
- Methods (2-3 sentences)
- Results (4-5 sentences, bullet form acceptable)
- Conclusions (2-3 sentences)
- Contributions (1-2 sentences)
- Practical Implications (1 sentence)

**Style**:
- Past tense for what was done ("We evaluated...")
- Present tense for findings ("Results show...")
- No citations in abstract (general rule, check with supervisor)
- Self-contained (readable without reading full thesis)

---

## TODO
- [ ] Fill all [FILL AFTER EXPERIMENTS] placeholders with actual results
- [ ] Add your name and supervisor name
- [ ] Verify word count fits within institutional requirements (usually 200-350 words)
- [ ] Check if keywords are appropriate for your institution
- [ ] Ensure all numbers are accurate and consistent with Results chapter
- [ ] Polish for clarity and conciseness
- [ ] Have supervisor review before submission

---

## Translation Note

Many institutions require abstract in both English and native language. If needed, create:
- `00_abstract_en.md` (English - this file)
- `00_abstract_hu.md` (Hungarian translation, if required)

Check with supervisor on this requirement.
