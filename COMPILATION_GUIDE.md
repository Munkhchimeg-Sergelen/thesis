# Thesis Compilation Guide

## 📄 How to Compile Your Thesis to PDF

### Option 1: Using Pandoc (Recommended)

#### Install Pandoc
```bash
# macOS
brew install pandoc

# Linux
sudo apt-get install pandoc

# Or download from: https://pandoc.org/installing.html
```

#### Install LaTeX (for PDF generation)
```bash
# macOS
brew install --cask mactex

# Linux
sudo apt-get install texlive-full
```

#### Compile Thesis
```bash
cd ~/thesis-asr/docs/thesis_materials

# Combine all chapters in order
pandoc \
  00_title_page.md \
  00_table_of_contents.md \
  00_abstract.md \
  07_introduction.md \
  06_background.md \
  01_methods_hardware.md \
  02_methods_systems.md \
  03_methods_evaluation.md \
  03_results.md \
  05_discussion.md \
  06_conclusions.md \
  10_bibliography.bib \
  -o ../../thesis_final.pdf \
  --pdf-engine=xelatex \
  --toc \
  --number-sections \
  -V geometry:margin=1in \
  -V fontsize=12pt \
  -V documentclass=report
```

---

### Option 2: Using LaTeX Directly

#### Create Main LaTeX File

Create `thesis.tex`:

```latex
\documentclass[12pt,a4paper]{report}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{biblatex}

\title{Analysis of Multilingual Automatic Speech Recognition Approaches}
\author{Munkhchimeg Sergelen}
\date{November 2025}

\begin{document}

\maketitle

\chapter*{Abstract}
\input{00_abstract.tex}

\tableofcontents
\listoffigures
\listoftables

\chapter{Introduction}
\input{07_introduction.tex}

\chapter{Background and Related Work}
\input{06_background.tex}

\chapter{Methods}
\input{01_methods_hardware.tex}
\input{02_methods_systems.tex}
\input{03_methods_evaluation.tex}

\chapter{Results}
\input{03_results.tex}

\chapter{Discussion}
\input{05_discussion.tex}

\chapter{Conclusions}
\input{06_conclusions.tex}

\bibliography{10_bibliography}

\end{document}
```

#### Compile
```bash
pdflatex thesis.tex
bibtex thesis
pdflatex thesis.tex
pdflatex thesis.tex
```

---

### Option 3: Using Online Tools

#### Overleaf (Easiest)
1. Go to [overleaf.com](https://www.overleaf.com)
2. Create new project
3. Upload all `.md` files
4. Convert markdown to LaTeX (or use directly with pandoc)
5. Compile to PDF

---

## 📋 Pre-Compilation Checklist

Before compiling, verify:

- [ ] All chapters are in correct order
- [ ] Figures are in `figures/` directory
- [ ] All figure paths are correct (`figures/xxx.png`)
- [ ] Bibliography file exists (`10_bibliography.bib`)
- [ ] Page breaks are where you want them
- [ ] Table of contents is accurate
- [ ] All cross-references work

---

## 🎨 Formatting Tips

### Page Layout
```yaml
Margins: 1 inch (2.54 cm) on all sides
Font: 12pt Times New Roman or Computer Modern
Line spacing: 1.5 or double
Page numbering: Bottom center, starting from Introduction
```

### Chapter Formatting
```yaml
Chapter titles: 18pt, bold, centered
Section titles: 14pt, bold, left-aligned
Subsection titles: 12pt, bold, left-aligned
Body text: 12pt, justified
```

### Figures
```yaml
Position: Center-aligned
Caption: Below figure, 10pt
Reference: "Figure X.Y" in text
Numbering: Chapter.Number (e.g., Figure 4.1)
```

### Tables
```yaml
Position: Center-aligned
Caption: Above table, 10pt
Reference: "Table X.Y" in text
Numbering: Chapter.Number (e.g., Table 4.1)
```

---

## 🔧 Troubleshooting

### "Figures not found"
- Check figure paths are correct
- Use relative paths: `figures/xxx.png`
- Ensure figures are in correct directory

### "Bibliography not rendering"
- Check `.bib` file format
- Run bibtex/biber after first compilation
- Compile multiple times (2-3 times)

### "Table of contents missing"
- Add `--toc` flag to Pandoc
- Or include `\tableofcontents` in LaTeX
- Compile twice to generate TOC

### "Unicode characters not showing"
- Use `--pdf-engine=xelatex` instead of `pdflatex`
- Add `\usepackage{fontspec}` in LaTeX
- Ensure UTF-8 encoding

---

## 📤 File Order for Compilation

Compile in this exact order:

1. `00_title_page.md` - Title, declaration, acknowledgments
2. `00_table_of_contents.md` - TOC, list of figures/tables
3. `00_abstract.md` - Abstract
4. `07_introduction.md` - Chapter 1
5. `06_background.md` - Chapter 2
6. `01_methods_hardware.md` - Chapter 3.1
7. `02_methods_systems.md` - Chapter 3.2
8. `03_methods_evaluation.md` - Chapter 3.3
9. `03_results.md` - Chapter 4
10. `05_discussion.md` - Chapter 5
11. `06_conclusions.md` - Chapter 6
12. `10_bibliography.bib` - References

---

## ✅ Final Checks After Compilation

### Visual Inspection:
- [ ] Title page looks professional
- [ ] Page numbers are correct
- [ ] All figures appear correctly
- [ ] Tables are properly formatted
- [ ] Text is readable (not too small)
- [ ] Margins are consistent
- [ ] No orphaned headings (heading at bottom of page)
- [ ] Chapter starts on new page

### Content Checks:
- [ ] Table of contents matches actual content
- [ ] All figure numbers match references
- [ ] All table numbers match references
- [ ] All section numbers are correct
- [ ] Bibliography is complete
- [ ] No "TODO" or placeholder text remains

### Final Quality:
- [ ] Total page count reasonable (40-60 pages typical for BSc)
- [ ] File size reasonable (<10 MB)
- [ ] PDF opens correctly
- [ ] All links work (if hyperref used)
- [ ] Searchable text (not scanned images)

---

## 📊 Expected Output

**File**: `thesis_final.pdf`  
**Pages**: ~55-65 pages  
**Size**: 2-5 MB (with figures)  

**Structure**:
- Front matter: 5 pages (title, TOC, abstract)
- Introduction: 5 pages
- Background: 8 pages
- Methods: 7 pages
- Results: 10 pages
- Discussion: 12 pages
- Conclusions: 6 pages
- Bibliography: 2 pages
- **Total**: ~55 pages

---

## 🚀 Quick Compilation Command

**One-liner for quick PDF**:
```bash
cd ~/thesis-asr/docs/thesis_materials && \
pandoc 00_title_page.md 00_table_of_contents.md 00_abstract.md \
       07_introduction.md 06_background.md \
       01_methods_hardware.md 02_methods_systems.md 03_methods_evaluation.md \
       03_results.md 05_discussion.md 06_conclusions.md \
       -o ../../thesis_final.pdf \
       --pdf-engine=xelatex \
       --toc --number-sections \
       -V geometry:margin=1in -V fontsize=12pt \
       -V documentclass=report
```

---

## 📧 Submission Format

When sending to supervisor:

**Email Subject**: BSc Thesis - Analysis of Multilingual ASR - Munkhchimeg Sergelen

**Attachments**:
1. `Sergelen_Munkhchimeg_Thesis_2025.pdf` (renamed thesis)
2. Link to GitHub repository (optional)

**Email Body**:
```
Dear Dr. Mihajlik Péter,

Please find attached my BSc thesis titled "Analysis of Multilingual 
Automatic Speech Recognition Approaches" for your review.

The thesis evaluates 312 experiments comparing LID→ASR and language-hinted 
approaches across 4 languages, with key findings including 99.31% LID accuracy 
and a surprising 2.76× speed advantage for LID mode.

All code and data are available at: [GitHub URL]

I would appreciate your feedback and am available to discuss any questions.

Best regards,
Munkhchimeg Sergelen
```

---

**Good luck with compilation!** 🎓
