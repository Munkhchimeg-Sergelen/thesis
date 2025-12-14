#!/bin/bash
# Fix numpy/pandas compatibility and run profiling

echo "=================================================="
echo "FIXING ENVIRONMENT & RUNNING PROFILING"
echo "=================================================="

ssh -p 15270 mugi@bistromat.tmit.bme.hu << 'ENDSSH'
cd ~/thesis-asr

echo "Fixing numpy/pandas compatibility..."
pip install --upgrade pandas numpy psutil --quiet

# Verify installation
python -c "import pandas; import numpy; import psutil; print('✓ All modules OK')"

if [ $? -eq 0 ]; then
    echo ""
    echo "Starting resource profiling..."
    nohup python scripts/profile_resource_usage.py \
        --samples-per-lang 10 \
        --output results/resource_profiling.csv \
        > profile.log 2>&1 &
    
    PID=$!
    echo "✓ Profiling started! PID: $PID"
    echo ""
    echo "Monitor with: tail -f ~/thesis-asr/profile.log"
    echo "Check progress: wc -l ~/thesis-asr/results/resource_profiling.csv"
else
    echo "ERROR: Module installation failed"
    exit 1
fi
ENDSSH

echo ""
echo "=================================================="
echo "✓ Profiling is now running on GPU server"
echo "=================================================="
