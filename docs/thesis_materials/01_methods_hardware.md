# Methods: Hardware & Software Configuration

## For Thesis

### 3.1 Computational Resources

This evaluation was conducted on two hardware configurations to assess the practical deployment characteristics of multilingual ASR systems across different computing environments.

#### 3.1.1 CPU Configuration (Baseline Evaluation)

**Hardware Specification**:
- **Processor**: Apple M-series (ARM64 architecture)
- **RAM**: 16 GB unified memory
- **Operating System**: macOS 14.x

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

**Rationale**: The CPU configuration represents a cost-effective, widely accessible deployment scenario suitable for batch processing applications where real-time constraints are relaxed.

**Reproducibility**: The complete environment specification is provided in `environment.yml` (Conda environment file), ensuring full reproducibility of results. All dependencies are version-pinned to prevent compatibility issues.

#### 3.1.2 GPU Configuration (Accelerated Evaluation)

**Hardware Specification**:
- **GPU**: 2× NVIDIA RTX A6000 (49 GB VRAM each, 98 GB total)
- **CUDA Version**: 12.1
- **Driver Version**: 535.113.01
- **Host System**: Remote GPU server (bistromat.tmit.bme.hu)
- **Architecture**: Ampere (compute capability 8.6)

**Software Environment**:
- **Python**: 3.10.18 (matching CPU configuration)
- **PyTorch**: 2.5.1+cu121 (CUDA 12.1 support)
- **Transformers**: 4.57.1 (with GPU acceleration)
- **GPU Monitoring**: `pynvml` for VRAM and utilization tracking
- All other libraries identical to CPU configuration

**Rationale**: The GPU configuration represents a high-performance deployment scenario suitable for real-time or high-throughput applications. The dual RTX A6000 setup provides enterprise-grade compute capacity, enabling evaluation of larger models and concurrent processing.

**Access**: GPU resources were provided by the Department of Telecommunications and Media Informatics, Budapest University of Technology and Economics.

**Note on Shared Resources**: The GPU server is a shared multi-user environment. During evaluation, GPU utilization from concurrent users ranged from 85-98%, which may have influenced absolute timing measurements. However, relative comparisons (e.g., model size scaling) remain valid as all models were evaluated under similar load conditions.

---

## Supporting Data

**Environment Files**:
- Full specification: `env/asr-env-wsl.yml`
- Frozen dependencies: `env/asr-env-freeze.txt`
- Hardware info: `docs/gpu_hardware_info.txt` (if GPU used)

**Verification Commands** (included in appendix):
```bash
# Verify PyTorch + CUDA
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Check GPU
nvidia-smi

# Environment info
conda env export > environment.yml
```

---

## Key Points

✅ **Reproducible**: Conda environment fully specified  
✅ **Dual Hardware**: CPU (cost-effective) and GPU (high-performance)  
✅ **Standard Tools**: PyTorch, Hugging Face Transformers  
✅ **Version Controlled**: All dependencies pinned

---

## Notes for Writing

- Add actual hardware specs before final submission
- Include GPU details only if GPU evaluation completed
- Reference the conda environment file in the appendix
- Mention supervisor/institution for GPU access
- Emphasize reproducibility (key for BSc thesis)

---

## TODO
- [ ] Fill in CPU specs (processor model, RAM)
- [ ] Fill in GPU specs (if used)
- [ ] Add OS version details
- [ ] Verify all version numbers match `env/asr-env-freeze.txt`
- [ ] Add institution/supervisor acknowledgment for GPU
