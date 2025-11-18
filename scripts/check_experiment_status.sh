#!/bin/bash
# Quick experiment status checker

echo "=========================================="
echo "📊 Experiment Status Check"
echo "=========================================="
echo ""

# Check if process is running
if ps aux | grep -q "[r]un_comparison_batch.sh"; then
    echo "✅ Experiment is RUNNING"
else
    echo "⚠️  Experiment is NOT running (completed or crashed?)"
fi
echo ""

# Count files
TOTAL=$(find results/transcripts/hinted -name "*.txt" 2>/dev/null | wc -l | tr -d ' ')
WHISPER=$(find results/transcripts/hinted/whisper-small -name "*.txt" 2>/dev/null | wc -l | tr -d ' ')
WAV2VEC=$(find results/transcripts/hinted/wav2vec2 -name "*.txt" 2>/dev/null | wc -l | tr -d ' ')

echo "Total transcripts: $TOTAL"
echo "  Whisper: $WHISPER"
echo "  Wav2Vec2: $WAV2VEC"
echo ""

# By language
HU_WHISPER=$(find results/transcripts/hinted/whisper-small/hu -name "*.txt" 2>/dev/null | wc -l | tr -d ' ')
MN_WHISPER=$(find results/transcripts/hinted/whisper-small/mn -name "*.txt" 2>/dev/null | wc -l | tr -d ' ')
HU_WAV2VEC=$(find results/transcripts/hinted/wav2vec2/hu -name "*.txt" 2>/dev/null | wc -l | tr -d ' ')
MN_WAV2VEC=$(find results/transcripts/hinted/wav2vec2/mn -name "*.txt" 2>/dev/null | wc -l | tr -d ' ')

echo "By Language:"
echo "  Hungarian:"
echo "    Whisper: $HU_WHISPER / 1001"
echo "    Wav2Vec2: $HU_WAV2VEC / 1001"
echo "  Mongolian:"
echo "    Whisper: $MN_WHISPER / 1001"
echo "    Wav2Vec2: $MN_WAV2VEC / 1001"
echo ""

# Progress percentage
TOTAL_NEEDED=2002  # 1001 MN + 1001 HU
AUDIO_PROCESSED=$((WHISPER > WAV2VEC ? WHISPER : WAV2VEC))
PERCENT=$((AUDIO_PROCESSED * 100 / TOTAL_NEEDED))

echo "Progress: $AUDIO_PROCESSED / $TOTAL_NEEDED audio files ($PERCENT%)"
echo ""

# Last processed
echo "Last 3 files processed:"
find results/transcripts/hinted -name "*.txt" -type f 2>/dev/null | xargs ls -lt | head -6 | tail -3 | awk '{print "  " $9}'
echo ""

echo "=========================================="
echo "To view live log: tail -f experiment_restart.txt"
echo "=========================================="
