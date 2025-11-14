# 🎯 Action Plan: Download 1000 Samples Per Language

**Goal**: Get ~1000 samples for ES, FR, HU, MN to complete thesis evaluation  
**Timeline**: 1-2 days (mostly download time)

---

## 🚀 OPTION 1: Manual Download (RECOMMENDED - MOST RELIABLE)

### Step 1: Download from Mozilla (30-60 minutes)

Visit: **https://commonvoice.mozilla.org/en/datasets**

**For each language:**
1. Find language in the list
2. Click "Download" 
3. Select version (e.g., Common Voice Corpus 13.0 or later)
4. Download the `.tar.gz` file (large! ~2-20 GB per language)

**Save to**: `~/Downloads/`

**Languages needed:**
- ✅ Spanish (es) - ~20 GB
- ✅ French (fr) - ~15 GB  
- ✅ Hungarian (hu) - ~5 GB
- ✅ Mongolian (mn) - ~2 GB

**Total download**: ~40-50 GB  
**Time**: 30-60 minutes depending on internet speed

### Step 2: Extract (5-10 minutes)

```bash
cd ~/Downloads

# Extract all
tar -xzf cv-corpus-*-es.tar.gz
tar -xzf cv-corpus-*-fr.tar.gz
tar -xzf cv-corpus-*-hu.tar.gz
tar -xzf cv-corpus-*-mn.tar.gz

# Or extract all at once
tar -xzf cv-corpus-*.tar.gz
```

### Step 3: Process with Our Script (10-15 minutes)

```bash
cd ~/thesis-asr

# Process all languages at once
python scripts/process_manual_cv.py ~/Downloads/cv-corpus-*/

# This will:
# - Extract 1000 samples from test.tsv for each language
# - Copy audio files to data/wav/{lang}/
# - Save transcripts to data/ref/{lang}/
# - Total: 4000 files
```

### Step 4: Verify (1 minute)

```bash
# Count files (should be ~4000)
find data/wav -name '*.mp3' -o -name '*.wav' | wc -l

# Check per language (should be ~1000 each)
for lang in es fr hu mn; do
  count=$(find data/wav/$lang -name '*.mp3' -o -name '*.wav' | wc -l)
  echo "$lang: $count files"
done
```

### Step 5: Run Experiments (1-2 days)

```bash
# Start experiments in background
nohup ./scripts/run_comparison_batch.sh > experiment_log.txt 2>&1 &

# Monitor progress
tail -f experiment_log.txt
```

---

## 🔧 OPTION 2: HuggingFace with Authentication (FASTER IF IT WORKS)

### Step 1: Create HuggingFace Account

Visit: **https://huggingface.co/join**
- Sign up (free)
- Verify email

### Step 2: Accept Common Voice Terms

Visit: **https://huggingface.co/datasets/mozilla-foundation/common_voice_13_0**
- Click "Agree and Access Repository"
- Accept terms of use

### Step 3: Login via CLI

```bash
# Install CLI
pip install "huggingface_hub"

# Login (will open browser)
python -c "from huggingface_hub import login; login()"

# Enter your token when prompted
```

### Step 4: Retry Download

```bash
cd ~/thesis-asr
python scripts/download_cv_streaming.py
```

If this works, it will download 1000 samples automatically!

---

## 🎯 OPTION 3: Check What You Already Have

Maybe you have previous Common Voice downloads?

```bash
# Search for Common Voice data
find ~ -name "cv-corpus-*" -type d 2>/dev/null
find ~/Downloads -name "*.tar.gz" | grep common
find ~/Downloads -name "test.tsv" 2>/dev/null
```

If you find old CV downloads, use Option 1 Step 3 to process them!

---

## 📊 What Happens After Download

### Immediate (same day):
1. ✅ 4000 audio files in `data/wav/`
2. ✅ 4000 reference texts in `data/ref/`
3. 🚀 Start experiments running overnight

### Next 1-2 days:
4. ⏳ Experiments run (~12,000 evaluations)
5. 📊 Results accumulate in `results/transcripts/`

### Day 3:
6. ✅ Run statistical analysis
7. ✅ Generate updated figures
8. ✅ Email supervisor with validated results
9. 📝 Start writing thesis with strong data!

---

## 💾 Disk Space Requirements

**Check free space:**
```bash
df -h ~
```

**You need:**
- Downloads: ~50 GB (can delete after extracting)
- Extracted: ~50 GB (can delete after processing)
- Processed: ~4 GB (keep this!)
- Results: ~1 GB
- **Total needed**: ~10 GB after cleanup

**To free space after processing:**
```bash
# Delete downloaded .tar.gz files
rm ~/Downloads/cv-corpus-*.tar.gz

# Delete extracted directories
rm -rf ~/Downloads/cv-corpus-*/
```

---

## ⏱️ Complete Timeline

| Step | Time | Can Run Overnight? |
|------|------|-------------------|
| Download datasets | 30-60 min | ✅ Yes |
| Extract archives | 5-10 min | ✅ Yes |
| Process to samples | 10-15 min | ✅ Yes |
| **Setup complete** | **~1 hour** | - |
| Run experiments | 1-2 days | ✅ Yes (must!) |
| Statistical analysis | 10 min | No |
| Generate figures | 5 min | No |
| **Total** | **~2-3 days** | - |

---

## 🎯 RECOMMENDED: Do Option 1 (Manual Download)

**Why:**
- ✅ Most reliable (always works)
- ✅ Official Mozilla source
- ✅ Guaranteed test split independence
- ✅ No authentication issues

**Steps:**
1. **Today**: Download & process (1 hour active work)
2. **Tonight**: Start experiments running
3. **Tomorrow**: Let experiments run
4. **Day 3**: Analysis, figures, email supervisor

---

## 🚨 If Download Is Too Slow / No Space

**Alternative**: Start with smaller sample size and ask supervisor

```
"I'm encountering practical constraints with downloading 50GB of 
Common Voice data (40GB download + 50GB extracted). 

Options:
1. Download full dataset over next 2-3 days
2. Start with n=100-300 per language (statistically valid, faster)
3. Use alternative dataset (FLEURS, MLS)

What do you recommend given the timeline?"
```

---

## ✅ What To Do RIGHT NOW

**Choose your option:**

**A. Manual download** (recommended):
```bash
# Open browser
open https://commonvoice.mozilla.org/en/datasets

# Start downloading ES, FR, HU, MN
# While downloading, continue with other thesis work
```

**B. Try HuggingFace**:
```bash
# Sign up and authenticate
open https://huggingface.co/join

# Then retry automated download
```

**C. Ask me**: "I'm blocked on X, what should I do?"

---

**Which option do you want to try?** 🤔
