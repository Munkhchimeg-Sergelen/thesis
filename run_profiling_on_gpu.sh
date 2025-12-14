#!/bin/bash
# Run resource profiling on GPU server

echo "=================================================="
echo "RESOURCE PROFILING ON GPU SERVER"
echo "=================================================="
echo ""
echo "This will:"
echo "  - Profile CPU/GPU/Memory usage"
echo "  - 10 samples per language × 4 languages × 4 models = 160 runs"
echo "  - Save to results/resource_profiling.csv"
echo "  - Run in background (you can close terminal)"
echo ""
echo "Estimated time: 30-60 minutes"
echo ""
echo "=================================================="

ssh -p 15270 mugi@bistromat.tmit.bme.hu << 'ENDSSH'
cd ~/thesis-asr

# Check if script exists
if [ ! -f scripts/profile_resource_usage.py ]; then
    echo "ERROR: profile_resource_usage.py not found!"
    exit 1
fi

# Check if psutil is installed
python -c "import psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing psutil..."
    pip install psutil
fi

# Run profiling in background
echo "Starting resource profiling..."
nohup python scripts/profile_resource_usage.py \
    --samples-per-lang 10 \
    --output results/resource_profiling.csv \
    > profile.log 2>&1 &

PID=$!
echo "Profiling started! PID: $PID"
echo ""
echo "To check progress:"
echo "  ssh -p 15270 mugi@bistromat.tmit.bme.hu"
echo "  tail -f ~/thesis-asr/profile.log"
echo ""
echo "To check results:"
echo "  wc -l ~/thesis-asr/results/resource_profiling.csv"
echo ""
ENDSSH

echo ""
echo "=================================================="
echo "✓ Command sent to GPU server"
echo "=================================================="
echo ""
echo "The profiling is now running in the background."
echo "You can continue working on your thesis!"
echo ""
