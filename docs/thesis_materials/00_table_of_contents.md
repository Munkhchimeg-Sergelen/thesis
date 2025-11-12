# Table of Contents

## Front Matter
- Title Page
- Declaration of Authorship
- Acknowledgments
- Abstract ......................................................... 1
- Table of Contents ................................................ 2
- List of Figures .................................................. 3
- List of Tables ................................................... 4

---

## Main Content

### Chapter 1: Introduction ........................................ 5
1.1 Motivation ..................................................... 5  
1.2 Research Questions ............................................. 6  
1.3 Thesis Contributions ........................................... 7  
1.4 Scope and Limitations .......................................... 8  
1.5 Thesis Structure ............................................... 9  
1.6 Key Findings Preview ........................................... 10

### Chapter 2: Background and Related Work ......................... 11
2.1 Automatic Speech Recognition Fundamentals ...................... 11  
   2.1.1 Task Definition ........................................... 11  
   2.1.2 Neural ASR Architectures .................................. 11  
   2.1.3 Evaluation Metrics ........................................ 12  
2.2 Multilingual ASR Challenges .................................... 13  
   2.2.1 Phonetic Diversity ........................................ 13  
   2.2.2 Data Imbalance ............................................ 13  
   2.2.3 Morphological Complexity .................................. 14  
2.3 Language Identification ........................................ 14  
   2.3.1 Approaches to LID ......................................... 14  
   2.3.2 LID in Multilingual ASR .................................. 15  
2.4 Related Work ................................................... 16  
   2.4.1 Multilingual ASR Systems .................................. 16  
   2.4.2 Comparative Studies ....................................... 17

### Chapter 3: Methods ............................................. 18
3.1 Computational Resources ........................................ 18  
   3.1.1 Evaluation Hardware (CPU) ................................. 18  
   3.1.2 GPU Evaluation Attempts (Unsuccessful) .................... 19  
   3.1.3 Acknowledgments ........................................... 19  
3.2 Automatic Speech Recognition Systems ........................... 20  
   3.2.1 OpenAI Whisper ............................................ 20  
   3.2.2 Wav2Vec2-XLSR-53 .......................................... 21  
3.3 Evaluation Methodology ......................................... 22  
   3.3.1 Evaluation Modes .......................................... 22  
   3.3.2 Languages and Dataset ..................................... 23  
   3.3.3 Metrics ................................................... 23  
   3.3.4 Experimental Protocol ..................................... 24

### Chapter 4: Results ............................................. 25
4.1 Overview of Evaluation ......................................... 25  
   4.1.1 Experimental Setup ........................................ 25  
4.2 Language Identification Accuracy (RQ1) ......................... 26  
   4.2.1 Overall LID Performance ................................... 26  
   4.2.2 Error Analysis ............................................ 27  
   4.2.3 Key Findings .............................................. 27  
4.3 Processing Efficiency Comparison (RQ2) ......................... 28  
   4.3.1 Surprising Discovery: LID is Faster! ...................... 28  
   4.3.2 Processing Time by Model and Mode ......................... 28  
   4.3.3 Hypothesis for Speed Difference ........................... 29  
   4.3.4 Key Findings .............................................. 29  
4.4 Model Size Comparison (RQ3) .................................... 30  
   4.4.1 Processing Time by Model Size ............................. 30  
   4.4.2 Model Performance by Language ............................. 30  
   4.4.3 Key Findings .............................................. 31  
4.5 Language-Specific Performance (RQ4) ............................ 32  
   4.5.1 Processing Time by Language ............................... 32  
   4.5.2 Critical Finding: Mongolian Anomaly ....................... 32  
   4.5.3 Mongolian Performance by Model ............................ 33  
   4.5.4 Hypothesis for Mongolian Slowdown ......................... 33  
   4.5.5 Key Findings .............................................. 34  
4.6 System Comparison: Whisper vs Wav2Vec2 (RQ5) ................... 35  
   4.6.1 Processing Time Comparison ................................ 35  
   4.6.2 Observations .............................................. 35  
   4.6.3 Key Findings .............................................. 35  
4.7 Summary of Key Results ......................................... 36  
4.8 Figures and Tables ............................................. 37

### Chapter 5: Discussion .......................................... 42
5.1 Interpretation of Key Findings ................................. 42  
   5.1.1 RQ1: Language Identification Accuracy ..................... 42  
   5.1.2 RQ2: LID→ASR vs Language-Hinted Processing Efficiency ..... 43  
   5.1.3 RQ3: Model Size Scaling ................................... 45  
   5.1.4 RQ4: Language-Specific Performance - Mongolian Anomaly .... 46  
   5.1.5 RQ5: System Comparison - Whisper vs Wav2Vec2 .............. 49  
5.2 Failure Modes and Edge Cases ................................... 51  
   5.2.1 LID Misclassification ..................................... 51  
   5.2.2 Mongolian Processing Timeouts ............................. 51  
   5.2.3 Limitations Not Addressed ................................. 52  
5.3 Comparison to Prior Work ....................................... 53  
   5.3.1 Whisper Paper ............................................. 53  
   5.3.2 Wav2Vec2-XLSR ............................................. 53  
   5.3.3 Multilingual ASR Surveys .................................. 53  
5.4 Threats to Validity ............................................ 54  
   5.4.1 Internal Validity ......................................... 54  
   5.4.2 External Validity ......................................... 54  
   5.4.3 Construct Validity ........................................ 55  
5.5 Practical Deployment Recommendations ........................... 55  
   5.5.1 Choosing LID vs Hinted Mode ............................... 55  
   5.5.2 Choosing Whisper Model Size ............................... 56  
   5.5.3 Handling Low-Resource Languages ........................... 56  
   5.5.4 System Selection .......................................... 56  
5.6 Lessons Learned ................................................ 57

### Chapter 6: Conclusions ......................................... 58
6.1 Summary of Findings ............................................ 58  
6.2 Key Contributions .............................................. 60  
   6.2.1 First Systematic Evaluation of Whisper's LID .............. 60  
   6.2.2 Discovery of LID Speed Advantage .......................... 60  
   6.2.3 Quantification of Low-Resource Language Gap ............... 60  
   6.2.4 Deployment-Focused Evaluation ............................. 61  
   6.2.5 Reproducible Evaluation Framework ......................... 61  
6.3 Limitations .................................................... 61  
   6.3.1 No Transcription Accuracy Metrics ......................... 61  
   6.3.2 Limited Audio Characteristics ............................. 62  
   6.3.3 CPU-Only Evaluation ....................................... 62  
   6.3.4 Limited Language Coverage ................................. 62  
   6.3.5 Sample Size ............................................... 62  
   6.3.6 Incomplete Wav2Vec2 Analysis .............................. 62  
6.4 Practical Recommendations ...................................... 63  
6.5 Future Work .................................................... 64  
   6.5.1 Immediate Extensions ...................................... 64  
   6.5.2 Advanced Research Directions .............................. 64  
   6.5.3 Broader Impact Research ................................... 65  
6.6 Closing Remarks ................................................ 66

### Bibliography .................................................. 67

---

## Back Matter

### Appendices (Optional)
A. Complete Environment Specification ............................... 70  
B. Evaluation Scripts .............................................. 71  
C. Additional Figures .............................................. 72  
D. Raw Data Tables ................................................. 73

---

<div style="page-break-after: always;"></div>

# List of Figures

**Figure 4.1**: Whisper Model Size Comparison ...................... 37  
Processing time comparison across Whisper model sizes (tiny, base, small) for all four languages.

**Figure 4.2**: System Comparison - Whisper vs Wav2Vec2 ............ 38  
Comparison of Whisper-small and Wav2Vec2-XLSR-53 systems across supported languages.

**Figure 4.3**: Language Performance Comparison .................... 39  
Whisper-small performance by language (LID→ASR mode) showing Mongolian anomaly.

**Figure 4.4**: Processing Time Distribution ....................... 40  
Distribution of processing times across all experiments, showing spread and outliers.

**Figure 4.5**: Summary Statistics Table ........................... 41  
Summary statistics showing mean processing time and standard deviation by model and language.

---

<div style="page-break-after: always;"></div>

# List of Tables

**Table 4.1**: Overall Experimental Setup Summary .................. 25  
**Table 4.2**: LID Accuracy by Language ............................ 26  
**Table 4.3**: LID Accuracy by Model Size .......................... 26  
**Table 4.4**: Processing Time by Mode Comparison .................. 28  
**Table 4.5**: Processing Time by Model Size ....................... 30  
**Table 4.6**: Model Performance by Language ....................... 30  
**Table 4.7**: Processing Time by Language ......................... 32  
**Table 4.8**: Mongolian Performance by Model ...................... 33  
**Table 4.9**: System Comparison Summary ........................... 35  

---

**End of Table of Contents**
