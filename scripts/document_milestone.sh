#!/bin/bash
# Document and commit a milestone

set -e

echo "======================================"
echo "📝 Document Milestone & Commit to Git"
echo "======================================"
echo

# Get milestone description from user
if [ -z "$1" ]; then
    echo "Usage: ./scripts/document_milestone.sh \"Brief description\""
    echo
    echo "Examples:"
    echo "  ./scripts/document_milestone.sh \"Completed Wav2Vec2 implementation\""
    echo "  ./scripts/document_milestone.sh \"Finished GPU evaluation runs\""
    echo "  ./scripts/document_milestone.sh \"Generated comparison plots\""
    exit 1
fi

DESCRIPTION="$1"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
DATE=$(date +"%Y-%m-%d")

echo "Milestone: $DESCRIPTION"
echo "Timestamp: $TIMESTAMP"
echo

# Append to progress log
PROGRESS_LOG="docs/progress_log.md"

if [ ! -f "$PROGRESS_LOG" ]; then
    echo "# Thesis Progress Log" > "$PROGRESS_LOG"
    echo >> "$PROGRESS_LOG"
    echo "Automatic log of milestones and progress." >> "$PROGRESS_LOG"
    echo >> "$PROGRESS_LOG"
fi

echo "## $TIMESTAMP" >> "$PROGRESS_LOG"
echo >> "$PROGRESS_LOG"
echo "**Milestone**: $DESCRIPTION" >> "$PROGRESS_LOG"
echo >> "$PROGRESS_LOG"

# List changed files
echo "### Changed Files" >> "$PROGRESS_LOG"
echo '```' >> "$PROGRESS_LOG"
git status --short >> "$PROGRESS_LOG"
echo '```' >> "$PROGRESS_LOG"
echo >> "$PROGRESS_LOG"

# Add separator
echo "---" >> "$PROGRESS_LOG"
echo >> "$PROGRESS_LOG"

echo "✓ Updated progress log"

# Show what will be committed
echo
echo "Files to be committed:"
git status --short
echo

# Ask for confirmation
read -p "Commit and push to GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Add all files
    git add -A
    
    # Commit with milestone description
    git commit -m "[$DATE] $DESCRIPTION"
    
    # Push to GitHub
    echo
    echo "Pushing to GitHub..."
    git push
    
    echo
    echo "✅ Milestone documented and pushed!"
    echo
else
    echo
    echo "⚠️  Changes NOT committed. Run manually when ready:"
    echo "   git add -A"
    echo "   git commit -m \"$DESCRIPTION\""
    echo "   git push"
    echo
fi
