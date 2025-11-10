# Methods: Hardware & Software Configuration

## For Thesis

### Computational Resources

This evaluation was conducted on two hardware configurations to assess the practical deployment characteristics of multilingual ASR systems.

#### CPU Configuration (Baseline)

**Hardware**:
- **Processor**: [TODO: Fill from `docs/gpu_hardware_info.txt` or system info]
- **RAM**: [TODO: e.g., 16 GB DDR4]
- **Operating System**: [TODO: e.g., Ubuntu 22.04 LTS via WSL2 on Windows 11]

**Software Environment**:
- **Python**: 3.10.18
- **PyTorch**: 2.5.1 (CPU-only build)
- **Transformers**: 4.56.2
- **Key Libraries**: 
  - `faster-whisper` / `openai-whisper`
  - `torchaudio` 2.5.1
  - `jiwer` 4.0.0 (for WER/CER computation)
  - `librosa` 0.11.0 (for audio preprocessing)

**Reproducibility**:
The complete environment specification is provided in `env/asr-env-wsl.yml` (Conda) and `env/asr-env-freeze.txt` (pip freeze), ensuring full reproducibility of results.

#### GPU Configuration (Extended Evaluation)

**Hardware**:
- **GPU**: [TODO: e.g., NVIDIA RTX 4090, 24GB VRAM]
- **CUDA Version**: [TODO: e.g., 12.1]
- **Driver**: [TODO: e.g., 535.129.03]
- **Host CPU**: [TODO]
- **Host RAM**: [TODO]

**Software Environment**:
- Same Python/library versions as CPU configuration
- **PyTorch**: 2.5.1 with CUDA 12.1 support
- **Additional**: `pynvml` for GPU memory monitoring

**Access**: GPU evaluation was conducted on [TODO: university/lab server name] provided by [supervisor name].

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
