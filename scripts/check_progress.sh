#!/bin/bash
# Quick progress checker for experiments

echo "=========================================="
echo "📊 Experiment Progress Monitor"
echo "=========================================="
echo ""

# Count completed transcripts
COMPLETED=$(find results/transcripts/hinted/whisper-small -name "*.txt" 2>/dev/null | wc -l | tr -d ' ')
TOTAL=2002

echo "Completed: $COMPLETED / $TOTAL files"

# Calculate percentage
PERCENT=$(echo "scale=2; ($COMPLETED / $TOTAL) * 100" | bc)
echo "Progress: ${PERCENT}%"
echo ""

# Estimate time remaining (rough estimate)
if [ "$COMPLETED" -gt 5 ]; then
    # Get runtime so far
    if [ -f "experiment_log.txt" ]; then
        START_TIME=$(stat -f %B experiment_log.txt)
        NOW=$(date +%s)
        ELAPSED=$((NOW - START_TIME))
        
        # Calculate average time per file
        AVG_TIME=$((ELAPSED / COMPLETED))
        
        # Estimate remaining
        REMAINING_FILES=$((TOTAL - COMPLETED))
        REMAINING_SECONDS=$((REMAINING_FILES * AVG_TIME))
        
        # Convert to hours
        REMAINING_HOURS=$(echo "scale=1; $REMAINING_SECONDS / 3600" | bc)
        
        echo "Estimated time remaining: ~${REMAINING_HOURS} hours"
    fi
fi

echo ""
echo "=========================================="
echo "Last 5 files processed:"
find results/transcripts/hinted/whisper-small -name "*.txt" 2>/dev/null | tail -5 | xargs -n1 basename
echo ""
echo "To watch live: tail -f experiment_log.txt"
echo "=========================================="
