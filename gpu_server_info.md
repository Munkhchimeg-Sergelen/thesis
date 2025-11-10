# GPU Server Information

**Server**: bistromat.tmit.bme.hu  
**Port**: 15270  
**Username**: mugi  
**Password**: [STORED SECURELY - NOT IN GIT]

**Hardware**: 2x NVIDIA RTX A6000 (49GB VRAM each) 🔥

---

## Quick Connection Test

```bash
# Connect
ssh -p 15270 mugi@bistromat.tmit.bme.hu

# Verify GPU
nvidia-smi

# Check conda
conda --version

# Exit
exit
```

---

## Full Setup (For Tomorrow)

See: `gpu_quick_setup.sh`

```bash
# On server, after connecting:
bash gpu_quick_setup.sh
```

---

## Notes
- Password stored in: [your password manager]
- SSH key setup: [optional, for later]
- First connection: May need to accept host key
