#!/usr/bin/env python3
import os, shutil, glob, time, pathlib
SRC = {
  "run_summary": "results/metrics/run_summary.csv",
  "lid_acc":     "results/metrics/lid_accuracy.csv",
  "perf":        "results/metrics/perf.csv",
  "manifests":   "results/manifests/*.csv",
  "env_yaml":    "env/asr-env-wsl.yml",
  "env_freeze":  "env/asr-env-freeze.txt",
  "exp_design":  "docs/exp_design.md",
  "metrics_doc": "docs/metrics_schema.md",
  "commands":    "docs/appendix_commands.md",
}
OUTDIR = "results/most_relevant"; os.makedirs(OUTDIR, exist_ok=True)
def copy_if_exists(src):
    if "*" in src:
        for fp in glob.glob(src):
            if os.path.isfile(fp): shutil.copy2(fp, os.path.join(OUTDIR, os.path.basename(fp)))
    elif os.path.isfile(src):
        shutil.copy2(src, os.path.join(OUTDIR, os.path.basename(src)))
for v in SRC.values(): copy_if_exists(v)
def count_rows(p): 
    try: return max(0, sum(1 for _ in open(p, encoding="utf-8"))-1)
    except: return 0
idx = pathlib.Path(OUTDIR) / "INDEX.md"
idx.write_text(f"# Most Relevant (auto-assembled)\n_Last updated:_ {time.strftime('%F %T')}\n\n"
               "## Contents\n- run_summary.csv\n- lid_accuracy.csv\n- perf.csv\n- manifests *.csv\n"
               "- asr-env-wsl.yml / asr-env-freeze.txt\n- exp_design.md / metrics_schema.md\n- appendix_commands.md\n\n"
               f"## Quick stats\n- run_summary rows: {count_rows('results/metrics/run_summary.csv')}\n"
               f"- lid_accuracy rows: {count_rows('results/metrics/lid_accuracy.csv')}\n"
               f"- perf rows: {count_rows('results/metrics/perf.csv')}\n", encoding="utf-8")
print(f"most relevant → {OUTDIR}")
