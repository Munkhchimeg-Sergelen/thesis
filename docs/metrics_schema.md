# Metrics Schema

## Recognition Quality Metrics

### Word Error Rate (WER)
- **Formula**: `WER = (S + D + I) / N` where S=substitutions, D=deletions, I=insertions, N=reference words
- **Range**: [0, ∞), lower is better; >1.0 means more errors than words
- **Preprocessing**: lowercase, remove digits & punctuation, collapse whitespace
- **Tool**: `jiwer` library via `scripts/eval_metrics.py`

### Character Error Rate (CER)
- **Formula**: `CER = (S + D + I) / N` at character level
- **Range**: [0, ∞), lower is better
- **Purpose**: More granular than WER, useful for morphologically rich languages
- **Tool**: `jiwer` library via `scripts/eval_metrics.py`

## Language Identification Metrics

### LID Accuracy
- **Formula**: `Accuracy = correct_predictions / total_samples`
- **Range**: [0, 1], higher is better
- **Method**: Argmax of Whisper's language probability distribution (first 30s of audio)
- **Tool**: `scripts/lid_accuracy.py`

### LID Confidence
- **Metric**: Median probability of predicted language
- **Range**: [0, 1], higher indicates more confident predictions
- **Threshold**: <0.60 flagged as low confidence

## Efficiency Metrics

### Real-Time Factor (RTF)
- **Formula**: `RTF = processing_time / audio_duration`
- **Range**: [0, ∞)
  - RTF < 1.0: Faster than real-time (can process live streams)
  - RTF = 1.0: Real-time
  - RTF > 1.0: Slower than real-time
- **Tool**: `scripts/measure_perf.py`

### Latency
- **Definition**: Wall-clock time to process audio (seconds)
- **Measurement**: End-to-end including loading, inference, decoding

### CPU Usage
- **Metric**: Average CPU percentage during inference
- **Tool**: `psutil` via `scripts/measure_perf.py`

### Memory (RSS)
- **Metric**: Peak Resident Set Size in MB
- **Tool**: `psutil` via `scripts/measure_perf.py`

### GPU Memory (VRAM)
- **Metric**: Peak GPU memory allocated (MB)
- **Tool**: `pynvml` (when on GPU)

## Experimental Factors

### Audio Length Buckets
- **Short**: ~10 seconds
- **Medium**: ~30 seconds  
- **Long**: ~120 seconds (2 minutes)
- **Purpose**: Test performance across different input lengths

### Languages
- **MN**: Mongolian (low-resource, Cyrillic script)
- **HU**: Hungarian (agglutinative, Latin script)
- **FR**: French (well-resourced, Latin script)
- **ES**: Spanish (well-resourced, Latin script)

### Inference Modes
1. **Language-Hinted**: Language explicitly provided (oracle/upper bound)
2. **LID→ASR**: Language automatically detected, then used for transcription

## Hardware Context
- **CPU**: Model, cores, RAM capacity
- **GPU**: Model, CUDA version, driver version, VRAM capacity
- **OS**: Linux/Windows/WSL version
