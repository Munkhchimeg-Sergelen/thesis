#!/bin/bash
# Extract downloaded Common Voice archives

set -e

echo "======================================================"
echo "Common Voice Extractor"
echo "======================================================"
echo ""

cd ~/Downloads/cv-data

echo "Extracting archives (this takes 5-10 minutes)..."
echo ""

for file in cv-corpus-*.tar.gz; do
    if [ -f "$file" ]; then
        echo "Extracting $file..."
        tar -xzf "$file"
        echo "✓ Done"
    fi
done

echo ""
echo "======================================================"
echo "✓ EXTRACTION COMPLETE!"
echo "======================================================"
echo ""
echo "Next step:"
echo "  cd ~/thesis-asr"
echo "  python scripts/process_manual_cv.py ~/Downloads/cv-data/cv-corpus-*/"
echo ""
