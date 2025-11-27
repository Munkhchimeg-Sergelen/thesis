# Dockerfile for reproducible ASR evaluation environment
# Optional: Use for complete containerization

FROM nvidia/cuda:12.2.0-base-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh

ENV PATH=/opt/conda/bin:$PATH

# Create working directory
WORKDIR /workspace

# Copy environment specification
COPY environment.yml .

# Create conda environment
RUN conda env create -f environment.yml && \
    conda clean -afy

# Activate environment
SHELL ["conda", "run", "-n", "omni", "/bin/bash", "-c"]

# Install additional dependencies
RUN pip install faster-whisper psutil

# Copy project files
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY REPRODUCIBILITY_GUIDE.md .
COPY run_complete_evaluation.sh .

# Make scripts executable
RUN chmod +x scripts/*.sh
RUN chmod +x run_complete_evaluation.sh

# Set default command
CMD ["conda", "run", "--no-capture-output", "-n", "omni", "bash"]

# Usage:
# docker build -t thesis-asr .
# docker run --gpus all -v $(pwd)/results:/workspace/results thesis-asr bash run_complete_evaluation.sh
