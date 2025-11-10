# Thesis Writing Materials

**Purpose**: Pre-written content and data for thesis chapters  
**Update**: After every major experiment or milestone  
**Usage**: Copy sections directly into thesis during Week 2

---

## 📁 Structure

This folder contains **thesis-ready** content organized by chapter:

```
thesis_materials/
├── README.md                    # This file
├── 01_methods_hardware.md       # Hardware/software specs
├── 02_methods_systems.md        # System descriptions
├── 03_methods_evaluation.md     # Evaluation methodology
├── 04_results_baseline.md       # Baseline results (CPU)
├── 05_results_comparison.md     # System comparison
├── 06_results_gpu.md            # GPU vs CPU (if completed)
├── 07_discussion_findings.md    # Key findings interpretation
├── 08_discussion_failures.md    # Failure mode analysis
├── 09_conclusions.md            # Conclusions draft
├── figures/                     # All plots (with captions)
└── tables/                      # All tables (CSV + formatted)
```

---

## ✍️ How to Use During Writing

### Week 2 Writing Schedule

**Nov 17-18**: Methods & Experiments
- Copy from: `01_methods_*.md`, `03_methods_evaluation.md`
- Adapt structure to your university template
- Add transitions and context

**Nov 19**: Results
- Copy from: `04_results_*.md`, `05_results_comparison.md`, `06_results_gpu.md`
- Insert figures from `figures/`
- Insert tables from `tables/`

**Nov 20**: Discussion
- Copy from: `07_discussion_*.md`, `08_discussion_failures.md`
- Add interpretation and connect to related work

**Nov 21**: Conclusions
- Start with: `09_conclusions.md`
- Add limitations and future work

---

## 📊 Figures & Tables

### Figures (with captions)

Place all plots in `figures/` with descriptive names:
```
figures/
├── fig1_wer_by_language_whisper_baseline.png
├── fig1_caption.txt
├── fig2_rtf_cpu_vs_gpu.png
├── fig2_caption.txt
├── fig3_system_comparison_hinted_vs_lid.png
├── fig3_caption.txt
└── ...
```

### Tables (CSV + formatted)

Place all tables in `tables/` with both CSV and markdown:
```
tables/
├── table1_hardware_specs.csv
├── table1_hardware_specs.md
├── table2_wer_cer_summary.csv
├── table2_wer_cer_summary.md
└── ...
```

---

## 🔄 Update Checklist

After every experiment:
- [ ] Update relevant `*_results_*.md` file
- [ ] Save new plots to `figures/`
- [ ] Save new tables to `tables/`
- [ ] Add figure/table captions
- [ ] Commit to GitHub

After analysis:
- [ ] Write interpretation in `*_discussion_*.md`
- [ ] Document failure modes
- [ ] Update conclusions

---

## 📝 Writing Templates

Each `.md` file follows this structure:

```markdown
# [Section Title]

## For Thesis
[Ready-to-use text, formatted]

## Supporting Data
[References to figures/tables]

## Key Points
[Bullet points of main takeaways]

## Notes
[Context for later editing]
```

---

## 🎯 Goal

By Nov 16, all files should be **80% complete**, so Week 2 is just:
1. Copy content
2. Adjust formatting
3. Add transitions
4. Proofread

**No scrambling for data or re-running experiments during writing week!**
