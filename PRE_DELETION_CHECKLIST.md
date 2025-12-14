# ⚠️ Pre-Deletion Checklist

**BEFORE deleting ANY source data (audio files, raw data, etc.), COMPLETE THIS CHECKLIST!**

---

## ✅ Results Verification

- [ ] **Download all results** from remote server to local machine
- [ ] **Verify file counts:**
  ```bash
  # Expected: 2 * num_audio_files (one per system)
  find results/transcripts -name "*.json" | wc -l
  ```
- [ ] **Check both systems present:**
  ```bash
  ls results/transcripts/hinted/
  # Should see: whisper-small/ and wav2vec2/
  ```

---

## ✅ Metadata Completeness

- [ ] **Inspect JSON structure:**
  ```bash
  # Check Whisper JSON
  cat results/transcripts/hinted/whisper-small/[LANG]/[FILE].json
  
  # Check Wav2Vec2 JSON  
  cat results/transcripts/hinted/wav2vec2/[LANG]/[FILE].json
  ```

- [ ] **Required fields present:**
  - `text` or transcript ✅
  - `language_used` ✅
  - `elapsed_sec` or `processing_time_sec` ✅
  - `duration_sec` ✅
  - `rtf` ✅
  - `model` or `system` ✅
  - `mode` ✅

---

## ✅ Analysis Pipeline Test

- [ ] **Run full analysis:**
  ```bash
  python scripts/analyze_results.py
  ```

- [ ] **Check for errors/warnings** in output

- [ ] **Verify statistics generated:**
  ```bash
  ls results/analysis/
  # Should have: summary.txt, overall_statistics.csv, etc.
  ```

---

## ✅ Plot Generation Test

- [ ] **Generate all plots:**
  ```bash
  python scripts/create_plots.py
  ```

- [ ] **Open and inspect plots:**
  ```bash
  open docs/thesis_materials/figures/
  ```

- [ ] **Verify NO empty/NaN plots:**
  - Whisper model comparison has data ✅
  - System comparison has data ✅
  - Language comparison has data ✅
  - Processing time distribution has data ✅

- [ ] **Check plot legends** show both systems (Whisper + Wav2Vec2)

---

## ✅ Backup Verification

- [ ] **Results backed up locally:**
  ```bash
  ls ~/thesis-asr/results_[EXPERIMENT_NAME]/
  ```

- [ ] **Committed to Git:**
  ```bash
  git status
  git add results/analysis/
  git commit -m "Complete [EXPERIMENT] results"
  git push
  ```

---

## ✅ Final Confirmation

- [ ] **Can regenerate ALL thesis figures** from current data
- [ ] **No missing fields** in analysis output
- [ ] **Both systems** (Whisper + Wav2Vec2) detected correctly
- [ ] **All languages** present in results

---

## 🗑️ ONLY AFTER ALL ABOVE ✅ → DELETE SOURCE FILES

```bash
# On GPU server
rm -rf data/wav/[LANG]/

# On local machine (optional - if already backed up)
rm -rf ~/thesis-asr/data/wav/[LANG]/
```

---

## 🚨 WHAT WE LEARNED:

**Mistake:** Deleted MN+HU audio before verifying Whisper JSONs had `duration_sec` and `rtf` fields.

**Cost:** Had to re-download 2000 audio files and re-run entire experiment.

**Prevention:** This checklist! Use it religiously.

---

**Remember:** Disk space is cheap. Time is not. Always verify before deleting! ⏰
