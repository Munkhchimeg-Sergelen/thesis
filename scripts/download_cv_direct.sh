#!/bin/bash
# Direct download from Mozilla Common Voice AWS S3
# This bypasses HuggingFace entirely

set -e

echo "======================================================"
echo "Common Voice Direct Downloader"
echo "Downloads from Mozilla AWS S3 (no HuggingFace)"
echo "======================================================"
echo ""

# Create download directory
mkdir -p ~/Downloads/cv-data

# Common Voice 13.0 direct links
BASE_URL="https://mozilla-common-voice-datasets.s3.dualstack.us-west-2.amazonaws.com/cv-corpus-13.0-2023-03-09"

echo "This will download ~42GB total:"
echo "  - Spanish: ~20GB"
echo "  - French: ~15GB"
echo "  - Hungarian: ~5GB"
echo "  - Mongolian: ~2GB"
echo ""
echo "Press CTRL+C to cancel, or wait 5 seconds to start..."
sleep 5

# Download each language
cd ~/Downloads/cv-data

echo ""
echo "======================================================"
echo "Downloading Spanish (es) - ~20GB"
echo "======================================================"
if [ ! -f "cv-corpus-13.0-2023-03-09-es.tar.gz" ]; then
    curl -L -C - -o cv-corpus-13.0-2023-03-09-es.tar.gz \
        "${BASE_URL}/cv-corpus-13.0-2023-03-09-es.tar.gz" \
        || wget -c "${BASE_URL}/cv-corpus-13.0-2023-03-09-es.tar.gz"
else
    echo "✓ Spanish already downloaded"
fi

echo ""
echo "======================================================"
echo "Downloading French (fr) - ~15GB"
echo "======================================================"
if [ ! -f "cv-corpus-13.0-2023-03-09-fr.tar.gz" ]; then
    curl -L -C - -o cv-corpus-13.0-2023-03-09-fr.tar.gz \
        "${BASE_URL}/cv-corpus-13.0-2023-03-09-fr.tar.gz" \
        || wget -c "${BASE_URL}/cv-corpus-13.0-2023-03-09-fr.tar.gz"
else
    echo "✓ French already downloaded"
fi

echo ""
echo "======================================================"
echo "Downloading Hungarian (hu) - ~5GB"
echo "======================================================"
if [ ! -f "cv-corpus-13.0-2023-03-09-hu.tar.gz" ]; then
    curl -L -C - -o cv-corpus-13.0-2023-03-09-hu.tar.gz \
        "${BASE_URL}/cv-corpus-13.0-2023-03-09-hu.tar.gz" \
        || wget -c "${BASE_URL}/cv-corpus-13.0-2023-03-09-hu.tar.gz"
else
    echo "✓ Hungarian already downloaded"
fi

echo ""
echo "======================================================"
echo "Downloading Mongolian (mn) - ~2GB"
echo "======================================================"
if [ ! -f "cv-corpus-13.0-2023-03-09-mn.tar.gz" ]; then
    curl -L -C - -o cv-corpus-13.0-2023-03-09-mn.tar.gz \
        "${BASE_URL}/cv-corpus-13.0-2023-03-09-mn.tar.gz" \
        || wget -c "${BASE_URL}/cv-corpus-13.0-2023-03-09-mn.tar.gz"
else
    echo "✓ Mongolian already downloaded"
fi

echo ""
echo "======================================================"
echo "✓ ALL DOWNLOADS COMPLETE!"
echo "======================================================"
echo ""
echo "Next steps:"
echo "  1. Extract: cd ~/thesis-asr && bash scripts/extract_cv.sh"
echo "  2. Process: python scripts/process_manual_cv.py ~/Downloads/cv-data/cv-corpus-*/"
echo ""
echo "Files saved to: ~/Downloads/cv-data/"
ls -lh ~/Downloads/cv-data/
