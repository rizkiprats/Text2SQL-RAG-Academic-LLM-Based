FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# 1. Basic setup
RUN apt-get update && apt-get install -y \
    git wget curl python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# 2. Install vLLM
RUN pip install --upgrade pip
RUN pip install vllm==0.8.5.post1

# 3. Optional: Hugging Face cache
ENV HF_HOME=/models/hf_cache

# 4. Default command -> Run VLLM API server
ENTRYPOINT ["python3", "-m", "vllm.entrypoints.api_server"]