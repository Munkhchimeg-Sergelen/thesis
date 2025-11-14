# Manual Common Voice Download Instructions

## Option 1: Direct Download from Mozilla (RECOMMENDED)

### Step 1: Download from Mozilla Common Voice Website
Visit: https://commonvoice.mozilla.org/en/datasets

**Languages needed:**
- Spanish (es)
- French (fr) 
- Hungarian (hu)
- Mongolian (mn)

**For each language:**
1. Go to https://commonvoice.mozilla.org/en/datasets
2. Find the language
3. Download the "Delta Segment" or full dataset (TSV + MP3 files)
4. Save to `~/Downloads/cv-corpus-{version}-{lang}/`

### Step 2: Extract Test Split
Each download contains:
- `validated.tsv` - All validated recordings
- `test.tsv` - Official test split (USE THIS!)
- `train.tsv`, `dev.tsv` - Training splits
- `clips/` - MP3 audio files

### Step 3: Process with Our Script
Once downloaded, run:
```bash
python scripts/process_manual_cv.py ~/Downloads/cv-corpus-*/
```

---

## Option 2: Try HuggingFace with Authentication

```bash
# Login to HuggingFace
huggingface-cli login

# Accept Terms for Common Voice
# Visit: https://huggingface.co/datasets/mozilla-foundation/common_voice_13_0
# Click "Agree and Access Repository"

# Then retry download
python scripts/download_cv_streaming.py
```

---

## Option 3: Use wget/curl for Direct Dataset Access

Mozilla provides direct download links (large files!):

```bash
# Example for Spanish (replace with actual version URL)
wget https://mozilla-common-voice-datasets.s3.dualstack.us-west-2.amazonaws.com/cv-corpus-13.0-2023-03-09/cv-corpus-13.0-2023-03-09-es.tar.gz

# Extract
tar -xzf cv-corpus-13.0-2023-03-09-es.tar.gz
```

---

## Our Recommended Approach

**EASIEST**: Manual download from Mozilla website
- Takes 30-60 min total
- Guaranteed to work
- No authentication issues
- Get official test splits

**File sizes per language:**
- Spanish: ~20 GB
- French: ~15 GB
- Hungarian: ~5 GB
- Mongolian: ~2 GB
- **Total: ~40-50 GB**

We only need the `test.tsv` and corresponding MP3 files from `clips/` folder.
