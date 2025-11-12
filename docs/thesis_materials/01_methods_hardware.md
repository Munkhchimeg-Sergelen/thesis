# Methods: Hardware & Software Configuration

## For Thesis

### 3.1 Computational Resources

This evaluation was conducted on CPU hardware due to GPU compatibility issues encountered during setup. All 312 experiments were performed on a research server provided by the Department of Telecommunications and Media Informatics, Budapest University of Technology and Economics.

#### 3.1.1 Evaluation Hardware (CPU)

**Hardware Specification**:
- **Server**: bistromat.tmit.bme.hu (department research server)
- **Processor**: Intel Xeon CPU (x86_64 architecture)
- **RAM**: Sufficient for loading all models (exact specs not critical for CPU evaluation)
- **Operating System**: Linux (CentOS/Rocky Linux)

**Software Environment**:
- **Python**: 3.10.18
- **PyTorch**: 2.5.1 (CPU-optimized build)
- **Transformers**: 4.56.2
- **Audio Processing Libraries**: 
  - `torchaudio` 2.5.1 (audio I/O and preprocessing)
  - `soundfile` 0.13.1 (WAV file handling)
  - `librosa` 0.11.0 (audio feature extraction)
- **Evaluation Libraries**:
  - `jiwer` 4.0.0 (Word Error Rate and Character Error Rate computation)
  - `datasets` 4.4.1 (data loading and management)

**Rationale**: CPU evaluation represents a cost-effective, widely accessible deployment scenario suitable for edge devices, batch processing, and environments without GPU resources. While slower than GPU, CPU evaluation provides realistic performance metrics for resource-constrained deployments.

**Reproducibility**: The complete environment specification is maintained in a Conda environment file, ensuring full reproducibility of results. All dependencies are version-pinned to prevent compatibility issues.

**Conda Environment**:
```bash
conda create -n asr-env python=3.10
conda activate asr-env
pip install faster-whisper transformers torch librosa soundfile numpy pandas matplotlib seaborn
```

#### 3.1.2 GPU Evaluation Attempts (Unsuccessful)

**Issue Encountered**: Initial attempts to run evaluation on GPU hardware (NVIDIA RTX A6000) failed due to cuDNN compatibility issues between PyTorch 2.5.1, CUDA 12.1, and the Transformers library.

**Error Details**:
- cuDNN version mismatch errors when loading Whisper models
- Incompatibility between faster-whisper and GPU backend
- Time constraints prevented resolution of these technical issues

**Decision**: Proceed with CPU-only evaluation to meet thesis deadline. This limitation is acknowledged in the Introduction (Section 1.4) and Discussion (Section 5.3).

**Impact**: CPU evaluation provides valid comparative results (model size scaling, LID accuracy, mode comparison) but with higher absolute processing times than GPU would achieve. Real-time capability (RTF < 1.0) assessment is limited to CPU performance.

**Future Work**: GPU evaluation with resolved dependencies would provide complementary speedup measurements and enable real-time performance analysis.

---

## Supporting Data

**Verification Commands**:
```bash
# Verify Python environment
python --version  # 3.10.18

# Verify PyTorch
python -c "import torch; print(f'PyTorch: {torch.__version__}')"  # 2.5.1

# Verify key libraries
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"  # 4.56.2
python -c "import whisper; print('Whisper available')"

# List conda environment
conda list
```

---

### 3.1.3 Acknowledgments

**Computational Resources**: Server access provided by the Department of Telecommunications and Media Informatics, Budapest University of Technology and Economics.

**Supervisor**: Dr. Mihajlik Péter provided guidance on experimental design and access to evaluation infrastructure.

---

**End of Section 3.1: Computational Resources**
