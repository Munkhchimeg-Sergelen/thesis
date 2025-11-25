# Run French Wav2Vec2 on GPU

## SSH to GPU:
```bash
ssh -p 15270 mugi@bistromat.tmit.bme.hu
cd ~/thesis-asr
```

## Create batch script on GPU:
```bash
cat > run_fr_wav2vec2.sh << 'EOF'
#!/bin/bash
echo "Processing French with Wav2Vec2..."
count=0
for file in data/wav/fr/*.mp3; do
    python scripts/run_wav2vec2.py \
        --infile "$file" \
        --hint-lang fr \
        --device cpu \
        --save-json \
        --outdir results/transcripts/hinted/wav2vec2
    
    count=$((count + 1))
    if [ $((count % 50)) -eq 0 ]; then
        echo "Processed $count files..."
    fi
done
echo "✅ Completed $count files"
EOF

chmod +x run_fr_wav2vec2.sh
```

## Run in background:
```bash
nohup bash run_fr_wav2vec2.sh > fr_wav2vec2.log 2>&1 &

# Check progress:
tail -f fr_wav2vec2.log

# Or check later:
ps aux | grep run_fr_wav2vec2
```

## When done, download results (from Mac):
```bash
rsync -avz -e "ssh -p 15270" \
  mugi@bistromat.tmit.bme.hu:~/thesis-asr/results/transcripts/hinted/wav2vec2/fr/ \
  results/transcripts/hinted/wav2vec2/fr/
```

## Then re-run analysis on Mac:
```bash
python scripts/analyze_results.py
python scripts/create_plots.py
```
