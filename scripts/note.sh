#!/usr/bin/env bash
set -euo pipefail
mkdir -p docs/journal
f="docs/journal/$(date +%F).md"
if [ ! -f "$f" ]; then
  echo -e "# $(date +%F)\n\n## Goals\n- \n\n## What I ran\n- \n\n## Observations\n- \n\n## Issues / Fixes\n- \n\n## Next\n- " > "$f"
fi
if [ $# -gt 0 ]; then
  {
    echo -e "\n### $(date +%T) — quick note"
    echo "- $*"
  } >> "$f"
fi
echo "Notebook → $f"
