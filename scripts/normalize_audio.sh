#!/usr/bin/env bash
set -euo pipefail
in="$1"; out="$2"
mkdir -p "$(dirname "$out")"
ffmpeg -y -i "$in" -ar 16000 -ac 1 "$out"
