# Overleaf Free Tier Timeout Fix

## Problem
Your comprehensive Results chapter (04_results_merged.tex) is too large for Overleaf's free tier compile timeout.

## Solutions

### Option 1: Use Minimal Version (FASTEST - Do This Now!)

**In Overleaf:**

1. **Rename your main.tex**:
   - Right-click `main.tex` → Rename to `main_full.tex`

2. **Rename minimal version**:
   - Right-click `main_minimal.tex` → Rename to `main.tex`

3. **Click Recompile**

This will compile a shorter Results chapter (just key sections + 4 plots) that fits in the free tier timeout.

---

### Option 2: Use Simplified Version (Medium)

Uses `main_simplified.tex` - includes only Results chapter but full version.

**In Overleaf:**
1. Rename `main.tex` → `main_full.tex`
2. Rename `main_simplified.tex` → `main.tex`
3. Make sure it references `04_results_merged.tex`
4. Recompile

May still timeout, but worth trying.

---

### Option 3: Upgrade Overleaf (Recommended for Final Version)

**Overleaf Premium Benefits:**
- 10× longer compile timeout
- More collaborators
- Track changes
- Document history
- ~$12-15/month

**Worth it for thesis writing!**

Go to: https://www.overleaf.com/user/subscription/plans

---

### Option 4: Work Locally (Free but Requires Setup)

**Install MacTeX** (if not already):
```bash
brew install --cask mactex
```

**Then compile locally:**
```bash
cd ~/thesis-asr/thesis
pdflatex main.tex
```

Takes ~5GB space but no timeout limits.

---

## What's in Each Version?

### main_minimal.tex (FASTEST - Recommended Now)
- ✅ Compiles in ~30 seconds
- ✅ Key findings with 4 plots
- ✅ Summary statistics
- ❌ Missing detailed analysis
- ❌ Missing 14 plots
- **Use for**: Quick preview, showing progress

### main_simplified.tex (Medium)
- ✅ Abstract only
- ✅ Full Results chapter (all plots)
- ❌ No other chapters yet
- **May timeout** on free tier

### main.tex / main_full.tex (Complete)
- ✅ All chapters
- ✅ All 18 plots
- ✅ Full analysis
- ❌ **Will timeout** on free tier
- **Use with**: Overleaf Premium or local LaTeX

---

## Recommended Workflow

### Phase 1: Now (Free Tier)
1. Use `main_minimal.tex`
2. Get it compiling successfully
3. Show your supervisor / review progress
4. Write other chapters in separate documents

### Phase 2: When Ready to Assemble (Upgrade or Local)
1. Either:
   - Upgrade to Overleaf Premium ($12-15/month), OR
   - Install MacTeX locally (free, 5GB)
2. Switch to `main_full.tex` with all chapters
3. Compile complete thesis

---

## Quick Commands

**In Overleaf, open Menu (≡) and run:**
```
# Check current main file
ls -l main.tex

# Switch to minimal version
# (do this by renaming in Overleaf UI)
```

**Locally (if you install MacTeX):**
```bash
cd ~/thesis-asr/thesis
pdflatex main_minimal.tex  # Fast preview
pdflatex main.tex          # Full version
```

---

## Current File Sizes

```
main_minimal.tex          # ~2 KB  → Compiles in 30s
chapters/04_results_quick.tex   # ~3 KB  → Fast
chapters/04_results_merged.tex  # ~20 KB → May timeout
```

---

## My Recommendation

**For TODAY:**
1. ✅ Use `main_minimal.tex` (rename to main.tex)
2. ✅ Get it compiling
3. ✅ See your thesis taking shape!
4. ✅ Share preview with supervisor

**For TOMORROW:**
1. 💰 Upgrade Overleaf to Premium (~$12/month)
   - Worth it for thesis writing!
   - No more timeouts
   - Can work with full document
2. OR 💻 Install MacTeX locally (free but 5GB)

**Don't waste time fighting free tier limits** - your thesis deserves the full tools! The $12 is worth your time and sanity. 😊

---

## Files Created for You

- `main_minimal.tex` - Quick version (use this now!)
- `chapters/04_results_quick.tex` - Shortened Results
- `main_simplified.tex` - Medium version
- This guide

**Action**: In Overleaf, rename `main_minimal.tex` → `main.tex` and recompile!
