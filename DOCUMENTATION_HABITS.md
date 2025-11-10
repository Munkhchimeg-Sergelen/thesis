# 📝 Documentation Habits for Thesis Success

**Purpose**: Ensure all experimental work is captured for thesis writing  
**Philosophy**: Document as you go, not after the fact  
**Goal**: Week 2 writing should be copy-paste, not reconstruction

---

## 🎯 Core Principle

**"If it's not documented, it didn't happen"**

Every experiment, result, and finding must be captured **immediately** so you have thesis-ready materials when writing begins.

---

## ⚡ Quick Habits (Do After EVERY Work Session)

### 1. After Running Experiments (5 min)

```bash
# 1. Copy command to appendix
echo "$(date): <command you ran>" >> docs/appendix_commands.md

# 2. Note what you did
./scripts/document_milestone.sh "Brief description of what you accomplished"

# Example:
./scripts/document_milestone.sh "Completed Whisper-small GPU evaluation on all 4 languages"
```

### 2. After Generating Results (10 min)

**Immediately create/update thesis materials**:

```bash
# For new results, update the relevant file:
nano docs/thesis_materials/04_results_baseline.md
# Add: 
# - What you tested
# - Key numbers (WER, RTF, etc.)
# - Initial observations

# For new plots:
cp results/plots/wer_comparison.png docs/thesis_materials/figures/
echo "Figure X: WER comparison across..." > docs/thesis_materials/figures/wer_comparison_caption.txt
```

### 3. End of Day (15 min)

**Daily checkpoint**:

1. **Update progress log**:
   ```bash
   # Automatically done by document_milestone.sh, but review:
   cat docs/progress_log.md
   ```

2. **Commit everything**:
   ```bash
   git add -A
   git commit -m "[$(date +%Y-%m-%d)] Daily checkpoint: <summary>"
   git push
   ```

3. **Update tomorrow's plan**:
   ```bash
   # Edit NEXT_STEPS.md or create tomorrow.md
   echo "## Nov X Plan" >> docs/daily_plans.md
   echo "- [ ] Task 1" >> docs/daily_plans.md
   echo "- [ ] Task 2" >> docs/daily_plans.md
   ```

---

## 📊 What to Document When

### After Each Experiment Type

#### ASR Run (Whisper/Wav2Vec2)
- [ ] Command used → `docs/appendix_commands.md`
- [ ] Output files location → note in progress log
- [ ] Any errors/warnings → `docs/issues_log.md`
- [ ] Approximate runtime → for efficiency discussion

#### Evaluation (WER/CER)
- [ ] Results CSV saved → `results/metrics/`
- [ ] Summary statistics → add to `docs/thesis_materials/04_results_*.md`
- [ ] Notable findings → jot in progress log
- [ ] Comparison to expectations → discussion notes

#### GPU Runs
- [ ] Hardware specs captured → `docs/gpu_hardware_info.txt`
- [ ] Performance logs → `results/gpu/metrics/`
- [ ] Speed comparison → add to `docs/thesis_materials/06_results_gpu.md`
- [ ] VRAM usage → note for deployment discussion

#### Analysis/Plots
- [ ] Plot saved → `docs/thesis_materials/figures/`
- [ ] Caption written → `*_caption.txt` next to plot
- [ ] Interpretation noted → in relevant `*_results_*.md` file
- [ ] Source data → CSV in `docs/thesis_materials/tables/`

---

## 📁 File Organization Rules

### Results Always Go In
```
results/
├── transcripts/         # All ASR outputs
├── metrics/            # All evaluation CSVs
└── plots/              # Raw plots (before selecting for thesis)
```

### Thesis Materials Always Go In
```
docs/thesis_materials/
├── figures/            # FINAL plots for thesis
├── tables/             # FINAL tables (CSV + MD)
└── *.md                # Pre-written thesis sections
```

### Logs and Notes Go In
```
docs/
├── progress_log.md           # Auto-generated milestone log
├── appendix_commands.md      # All commands run
├── issues_log.md             # Problems encountered
└── analysis_notes.md         # Observations and insights
```

---

## 🔄 Git Commit Schedule

### Minimum (Required)
- **After major experiments**: `./scripts/document_milestone.sh "..."`
- **End of day**: Manual commit with summary
- **After plots/analysis**: Commit with "Added plots/analysis for X"

### Recommended
- After every successful experiment
- After writing any thesis material section
- Before switching tasks (so you can rollback if needed)

### Commit Message Format
```
[YYYY-MM-DD] <Brief description>

Examples:
[2025-11-10] Added Wav2Vec2 implementation + comparison tools
[2025-11-12] Completed GPU evaluation - Whisper small/base
[2025-11-13] Generated all comparison plots for thesis
[2025-11-19] Drafted Methods chapter sections 1-3
```

---

## 📝 Templates for Common Tasks

### Document a New Experiment

**Template**: `docs/experiment_YYYY-MM-DD.md`
```markdown
# Experiment: [Brief Title]
**Date**: YYYY-MM-DD
**Goal**: [What you're testing]

## Setup
- System: [Whisper/Wav2Vec2]
- Model: [tiny/small/base]
- Device: [CPU/GPU]
- Languages: [MN/HU/FR/ES]
- Audio: [data/wav/...]

## Commands
```bash
# Copy actual commands here
```

## Results
- WER: [numbers]
- RTF: [numbers]
- Key findings: [bullet points]

## For Thesis
- Section: [Results/Discussion]
- What to highlight: [key points]
- Figures needed: [list]

## Issues
- [Any problems encountered]
```

### Document a Plot

**Template**: `docs/thesis_materials/figures/figX_caption.txt`
```
Figure X: [Descriptive title]

[Description paragraph: What the plot shows, key patterns, what to look for]

Data source: [Path to CSV or script that generated it]
```

### Document Failure Modes

**Add to**: `docs/thesis_materials/08_discussion_failures.md`
```markdown
### Failure Mode: [Brief Title]

**Observation**: [What went wrong]
**Frequency**: [How often it happened]
**Affected**: [Languages/systems/conditions]
**Cause**: [Hypothesis about why]
**Impact**: [WER delta or other metric]
**Example**: [Specific case reference]

For Thesis:
- Discuss in: Discussion section
- Relate to: [Prior work or expected behavior]
```

---

## 🚨 Warning Signs You're Not Documenting Enough

- ❌ Can't remember what you ran 2 days ago
- ❌ Looking for that "one result" but don't know where it is
- ❌ Re-running experiments because you lost the output
- ❌ Don't have captions for your plots
- ❌ Not sure which command produced which result
- ❌ Can't explain why you made a particular choice

**If any of these apply → STOP and document retroactively before continuing!**

---

## ✅ Checklist: Ready for Writing Week?

By Nov 16 (before writing starts), verify:

### Experimental Data
- [ ] All results CSVs committed to git
- [ ] All plots generated and saved
- [ ] All key numbers extracted and tabulated
- [ ] Commands used documented in appendix

### Thesis Materials Folder
- [ ] Hardware specs written (`01_methods_hardware.md`)
- [ ] System descriptions written (`02_methods_systems.md`)
- [ ] At least 50% of results sections drafted
- [ ] All figures with captions prepared
- [ ] All tables in CSV and markdown format

### Analysis Complete
- [ ] WER/CER summarized
- [ ] RTF/efficiency analyzed
- [ ] System comparison complete
- [ ] Failure modes documented
- [ ] Key findings written down

### Git Repository
- [ ] All code committed and pushed
- [ ] Progress log up-to-date
- [ ] Command appendix complete
- [ ] No uncommitted changes

---

## 🎯 Benefits of Good Documentation

### During Experiments
- ✅ Never lose track of what you've done
- ✅ Can reproduce results if needed
- ✅ Easy to share progress with supervisor
- ✅ Clear audit trail for methods section

### During Writing (Week 2)
- ✅ Copy-paste from thesis_materials/ → save hours
- ✅ All figures/tables ready → no scrambling
- ✅ All commands in appendix → methods section writes itself
- ✅ Can focus on narrative, not data collection

### After Submission
- ✅ Easy to respond to examiner questions
- ✅ Can reference exact setup if needed
- ✅ Reproducible for future work
- ✅ Portfolio piece for job applications

---

## 💡 Pro Tips

1. **Document in parallel**: Keep `nano docs/thesis_materials/XX.md` open while running experiments

2. **Use templates**: Copy-paste from templates above, don't start from blank

3. **Screenshot errors**: If something fails, screenshot the error and save it

4. **Name files descriptively**: `wer_whisper_small_gpu_2025-11-13.csv` not `results.csv`

5. **Commit often**: 10 small commits > 1 giant "end of week" commit

6. **Write captions immediately**: You'll forget context later

7. **Use TODO markers**: `[TODO: Verify this number]` if you need to come back

---

## 🚀 Bottom Line

**Good documentation = Easy thesis writing**

Spending 15 minutes after each experiment documenting:
- Saves hours during writing week
- Prevents missing critical details
- Makes your thesis reproducible
- Impresses examiners

**Make it a habit, not a chore!**
