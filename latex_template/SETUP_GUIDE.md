# BME LaTeX Template Setup Guide

## ✅ What's Already Done

1. ✅ Template extracted to `latex_template/`
2. ✅ Your information configured:
   - **Author**: Munkhchimeg Sergelen
   - **Supervisor**: Dr. Mihajlik Péter
   - **Title**: Analysis of Multilingual Automatic Speech Recognition Approaches
3. ✅ Language set to English
4. ✅ Chapter structure configured
5. ✅ List of figures/tables enabled

---

## 📁 Template Structure

```
latex_template/
├── thesis.tex          ← Main file (configured!)
├── content/            ← Your thesis chapters go here
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── background.tex
│   ├── methods.tex
│   ├── results.tex
│   ├── discussion.tex
│   ├── conclusions.tex
│   └── acknowledgement.tex
├── figures/            ← Your figures go here
├── bib/
│   └── mybib.bib       ← Your bibliography
└── include/            ← Template files (don't edit)
```

---

## 🚀 Next Steps

### Step 1: Copy Your Figures
```bash
cp ~/thesis-asr/docs/thesis_materials/figures/*.png ~/thesis-asr/latex_template/figures/
cp ~/thesis-asr/docs/thesis_materials/figures/*.pdf ~/thesis-asr/latex_template/figures/
```

### Step 2: I'll Convert Your Markdown to LaTeX
I'll help you convert each chapter from Markdown to LaTeX format.

### Step 3: Compile the Thesis
```bash
cd ~/thesis-asr/latex_template
xelatex thesis.tex
bibtex thesis
xelatex thesis.tex
xelatex thesis.tex
```

Or use the Makefile:
```bash
cd ~/thesis-asr/latex_template
make
```

---

## 📝 What I'll Do Next

I'll create LaTeX versions of your chapters:
1. Abstract
2. Introduction
3. Background
4. Methods
5. Results
6. Discussion
7. Conclusions
8. Acknowledgements
9. Bibliography

**Ready to continue?** Let me know and I'll start converting!
