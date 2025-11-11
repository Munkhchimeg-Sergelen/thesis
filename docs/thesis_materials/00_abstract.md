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

**Objective**: This thesis evaluates these two multilingual ASR strategies by comparing OpenAI Whisper (unified multilingual approach) against Wav2Vec2-XLSR-53 (language-specific specialization) across four languages (Spanish, French, Hungarian, Mongolian), two hardware configurations (CPU, GPU), and two inference modes (language-hinted, automatic language identification).

**Methods**: We conducted controlled experiments using the Mozilla Common Voice v11.0 test set, evaluating transcription accuracy (Word Error Rate, Character Error Rate), efficiency (Real-Time Factor, latency), and resource utilization (CPU/GPU, memory) across [X] samples per language. Three Whisper model sizes (39M, 74M, 244M parameters) were evaluated to assess model scaling trade-offs. All experiments were performed on standardized hardware (Apple M-series CPU, NVIDIA RTX A6000 GPU) with fully reproducible evaluation scripts.

**Results**: [FILL AFTER EXPERIMENTS]
- **Multilingual vs. Specialized**: [Wav2Vec2 / Whisper / Comparable] achieved [X]% [lower/higher] WER on Spanish/French, with language-specific models requiring [X]× larger deployment footprint.
- **Model Scaling**: Whisper-small (244M) achieved [X]% lower WER than Whisper-tiny (39M) at [X]× latency cost, with [diminishing/linear] returns observed.
- **Hardware Impact**: GPU provided [X]× speedup over CPU, enabling real-time transcription (RTF < 1.0) for [models].
- **Language Diversity**: Performance degraded [linearly/non-linearly] with resource level, with low-resource Mongolian showing [X]× higher WER than high-resource Spanish.
- **LID Impact**: Automatic language identification incurred [X]% WER penalty compared to oracle mode, with LID errors occurring in [X]% of samples.

**Conclusions**: [UPDATE BASED ON RESULTS]
Unified multilingual models (Whisper) provide [comparable/inferior/superior] accuracy to language-specific models while offering significant deployment advantages: [X]× smaller footprint and 2× broader language coverage. Model scaling exhibits diminishing returns beyond [X]M parameters for the evaluated languages. GPU deployment is cost-effective for high-volume batch processing despite higher instance costs. Multilingual models provide viable transcription for low-resource languages where specialized alternatives are unavailable, though with reduced accuracy.

**Contributions**: This thesis provides (1) the first controlled comparison of multilingual vs. specialized ASR strategies on identical test conditions, (2) deployment-focused evaluation incorporating latency and resource metrics beyond traditional WER benchmarks, (3) quantification of model scaling trade-offs for multilingual ASR, and (4) fully reproducible methodology with open-source code.

**Practical Implications**: For practitioners, we recommend language-hinted mode when language is known (eliminates LID errors), GPU deployment for batch processing (lower cost per audio hour), and multilingual models for coverage-critical applications. Language-specific models may be warranted for accuracy-critical applications on high-resource languages [if results support this].

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
