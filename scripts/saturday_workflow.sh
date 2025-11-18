#!/bin/bash
# Saturday Workflow: Download ES+FR, Upload to GPU, Start Experiment
# Run this when you have fast ethernet connection!

set -e

echo "=========================================="
echo "📅 SATURDAY ES+FR WORKFLOW"
echo "=========================================="
echo ""

# Configuration
GPU_SERVER="mugi@bistromat.tmit.bme.hu"
GPU_PORT="15270"
LOCAL_DATA="data/wav"
ARCHIVE_NAME="cv_es_fr_$(date +%Y%m%d).tar.gz"

# Step 1: Download MN+HU Results from GPU Server
echo "=========================================="
echo "Step 1: Download MN+HU Results"
echo "=========================================="
echo ""
echo "Downloading results from GPU server..."
echo "Command: scp -P ${GPU_PORT} -r ${GPU_SERVER}:~/results/ ~/thesis-asr/results_gpu/"
echo ""
read -p "Press Enter to download results (or Ctrl+C to skip)..."

scp -P ${GPU_PORT} -r ${GPU_SERVER}:~/results/ ~/thesis-asr/results_gpu/

echo "✅ Results downloaded to ~/thesis-asr/results_gpu/"
echo ""

# Step 2: Guide for Common Voice Download
echo "=========================================="
echo "Step 2: Download ES+FR from Common Voice"
echo "=========================================="
echo ""
echo "Run the download helper script:"
echo "  python scripts/download_cv_batch.py --langs es fr --num-samples 1000"
echo ""
read -p "Press Enter when ES+FR files are ready in data/wav/es and data/wav/fr..."

# Verify files exist
ES_COUNT=$(find data/wav/es -name "*.mp3" 2>/dev/null | wc -l | tr -d ' ')
FR_COUNT=$(find data/wav/fr -name "*.mp3" 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "Found:"
echo "  - Spanish: ${ES_COUNT} files"
echo "  - French: ${FR_COUNT} files"
echo ""

if [ "$ES_COUNT" -lt 50 ] || [ "$FR_COUNT" -lt 50 ]; then
    echo "⚠️  WARNING: Less than 50 files per language!"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 3: Create archive
echo "=========================================="
echo "Step 3: Create Archive"
echo "=========================================="
echo ""
echo "Creating ${ARCHIVE_NAME}..."

tar -czf ${ARCHIVE_NAME} data/wav/es data/wav/fr scripts/

ARCHIVE_SIZE=$(du -h ${ARCHIVE_NAME} | cut -f1)
echo "✅ Archive created: ${ARCHIVE_NAME} (${ARCHIVE_SIZE})"
echo ""

# Step 4: Upload to GPU server
echo "=========================================="
echo "Step 4: Upload to GPU Server"
echo "=========================================="
echo ""
echo "Uploading archive to GPU server..."
echo "This may take a few minutes..."

scp -P ${GPU_PORT} ${ARCHIVE_NAME} ${GPU_SERVER}:~/

echo "✅ Uploaded to GPU server"
echo ""

# Step 5: Extract and run on GPU server
echo "=========================================="
echo "Step 5: Run Experiment on GPU Server"
echo "=========================================="
echo ""
echo "Now SSH into the GPU server and run:"
echo ""
echo "  ssh -p ${GPU_PORT} ${GPU_SERVER}"
echo ""
echo "Then on the server:"
echo "  cd ~"
echo "  tar -xzf ${ARCHIVE_NAME}"
echo "  nohup ./scripts/run_comparison_batch.sh small cpu > experiment_es_fr.txt 2>&1 &"
echo "  sleep 30"
echo "  ./scripts/check_experiment_status.sh"
echo ""
read -p "Press Enter to SSH into server now..."

ssh -p ${GPU_PORT} ${GPU_SERVER}

echo ""
echo "=========================================="
echo "✅ WORKFLOW COMPLETE!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Monitor progress: ssh -p ${GPU_PORT} ${GPU_SERVER} './scripts/check_experiment_status.sh'"
echo "  2. Wait for completion (~12-24 hours)"
echo "  3. Download final results"
echo "  4. Run analysis and create plots"
echo ""
