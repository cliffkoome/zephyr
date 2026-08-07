# Zephyr — Offline AI Coding Tutor

> **ADTC 2026 Submission** | Track: `coding_assistants` | Model: `Qwen2.5-Coder-3B-Instruct-Q4_K_M`

Zephyr is a 100% offline, pedagogical AI coding assistant built for Computer Science students in resource-constrained environments across Africa. It runs on consumer laptop hardware (8 GB RAM, CPU-only) and combines a 3B code-specialized LLM with Retrieval-Augmented Generation (RAG) and an isolated execution sandbox.

---

## 🌟 Key Capabilities

- **Pedagogical Refusal Design (FR6):** Engineered strictly as a tutor. Zephyr guides students through concepts, identifies logical bugs, and explains terminal output, but refuses direct requests to solve graded assignments.
- **Textbook-Grounded RAG (FR5):** Grounded in _Think Python, 2nd Edition_ by Allen Downey (CC-BY-NC 3.0) via a lightweight local ChromaDB vector index (`all-MiniLM-L6-v2`).
- **Isolated Subprocess Sandbox (FR4):** Executes student code snippets in a separate Python environment with a 3-second hard timeout to capture real execution errors without risking host stability.
- **Bilingual Support (Swahili / Kiswahili):** Includes native support for technical explanations in Swahili, claiming the African Alpha Use Case Bonus.

---

## 📁 Repository Structure

```text
offline-coding-tutor/
├── metadata.json          # Official ADTC submission metadata & test prompts
├── download_model.sh      # Idempotent downloader for Qwen2.5-Coder GGUF weights
├── REPORT.md              # Technical design report, constraint analysis & benchmarks
├── requirements.txt       # Python dependencies (FastAPI, Streamlit, ChromaDB, etc.)
├── rag_ingest.py          # Vector store ingestion script for textbook grounding
├── sandbox.py             # Isolated 3-second Python execution sandbox
├── backend.py             # FastAPI orchestration server & RAG retriever
├── app.py                 # Streamlit frontend with Swahili bilingual interface
├── model/                 # Local directory for model weights (ignored in git)
├── chroma_db/             # Local directory for vector storage (ignored in git)
└── .gitignore             # Version control exclusions (*.gguf, model/, chroma_db/)

```

---

## 🚀 Quickstart & Reproduction

### 1. Prerequisites & Environment Setup

Ensure you are running Python 3.11 on Ubuntu 22.04 LTS:

```bash
python3.11 -m venv ~/adtc-venv
source ~/adtc-venv/bin/activate
pip install -r requirements.txt

```

### 2. Download Model Weights

Download the quantized GGUF weights (`~2.4 GB`) locally:

```bash
chmod +x download_model.sh
./download_model.sh

```

### 3. Initialize Vector Database (RAG)

Build the local ChromaDB index from the _Think Python_ textbook:

```bash
python rag_ingest.py

```

---

## 🛠️ Running the Application Stack

To run the interactive application, start the three components across separate terminal tabs (with `adtc-venv` active):

**Tab 1: Start `llama.cpp` Inference Engine**

```bash
~/llama.cpp/build/bin/llama-server -m model/qwen2.5-coder-3b-instruct-q4_k_m.gguf --port 8080 -c 4096

```

**Tab 2: Start FastAPI Backend Router**

```bash
uvicorn backend:app --port 8000

```

**Tab 3: Launch Streamlit Frontend**

```bash
streamlit run app.py

```

Access the interface at `http://localhost:8501`.

---

## 📊 Benchmark Execution

To evaluate Zephyr using the official ADTC profiler harness:

```bash
pip install "git+[https://github.com/Africa-Deep-Tech-Foundation/adtc-profiler.git](https://github.com/Africa-Deep-Tech-Foundation/adtc-profiler.git)"

adtc-profiler run \
  --submission . \
  --mode participant \
  --output submission.json

```

### Measured Performance Summary

| Metric                 | Measured Value | Threshold / Limit  | Status                     |
| ---------------------- | -------------- | ------------------ | -------------------------- |
| **Generation Speed**   | 17.92 t/s      | ≥ 15.0 t/s         | ✅ Passed (Max Score)      |
| **Peak RAM Footprint** | 3.45 GB        | < 7.0 GB           | ✅ Passed (>3.5 GB Margin) |
| **Thermal Throttling** | False          | No Throttling      | ✅ Passed                  |
| **Execution Mode**     | 100% Offline   | Zero Network Calls | ✅ Passed                  |

---

## 📜 License & Attributions

- **Model Weights:** Qwen2.5-Coder-3B-Instruct by Alibaba Cloud (Apache 2.0).
- **Textbook Material:** _Think Python, 2nd Edition_ by Allen Downey (CC-BY-NC 3.0).
- **Submission License:** Licensed under the terms of the GNU GPL v3 License.

```

```
