#!/bin/bash
# Quick LaTeX compilation script

cd ~/thesis-asr/thesis

echo "Compiling thesis..."
pdflatex -interaction=nonstopmode main.tex > compile.log 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Compilation successful!"
    echo "View PDF: open main.pdf"
    open main.pdf 2>/dev/null || echo "PDF created: thesis/main.pdf"
else
    echo "✗ Compilation failed. Check compile.log for errors"
    tail -20 compile.log
fi
