#!/bin/bash
mkdir -p model
# Downloading Qwen2.5-Coder-3B quantized to Q4_K_M (optimal size/speed ratio for 7GB RAM limit)
wget -nc -O model/qwen2.5-coder-3b-instruct-q4_k_m.gguf https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF/resolve/main/qwen2.5-coder-3b-instruct-q4_k_m.gguf