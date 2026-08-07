# Technical Report — Offline AI Coding Tutor

**Team ID:** mega-team
**Domain:** coding_assistants  
**Model:** Qwen2.5-Coder-3B-Instruct-Q4_K_M

---

## Problem

Computer Science students in African university environments face high data costs and intermittent internet connectivity, making cloud-based coding assistants (like GitHub Copilot) inaccessible. Furthermore, standard LLMs tend to directly solve assignments, violating academic integrity rather than teaching the underlying concepts. Our application solves this by providing a 100% offline, bilingual (English/Swahili) coding tutor that refuses direct solutions and instead explains concepts using localized pedagogical grounding.

---

## Design Decisions

- **Base model:** Qwen2.5-Coder-3B-Instruct. Code-specialized models drastically outperform generalist models at the <4B parameter scale, which is necessary to stay under the strict hardware constraints.
- **Quantization:** Q4_K_M was chosen for an optimal balance of coding accuracy and a low memory footprint (~2.4 GB), leaving ample room in the system for the backend servers and vector database.
- **Alternatives considered:** We evaluated 7B/8B parameter models, but they exceeded the 7.0 GB memory ceiling when running concurrently with the FastAPI server, ChromaDB, and Streamlit frontend. We also rejected relying purely on standard LLM generation; instead, we integrated a RAG pipeline (grounded in _Think Python_) and an isolated Python subprocess sandbox (with a 3-second timeout) to ensure the assistant evaluates real execution output and acts as a tutor rather than an assignment solver.

---

## Constraints

- Target: Strict 7.0 GB usable RAM ceiling, pure CPU inference via `llama.cpp` on Ubuntu 22.04 LTS.
- Connectivity: 100% offline requirement. We utilized the `all-MiniLM-L6-v2` embedding model to keep the ChromaDB vector store strictly local and lightweight.
- Thermal Safety: To avoid the thermal penalty, we restricted the `llama.cpp` context window to 4096 tokens, ensuring sustained inference does not push the CPU into thermal throttling.

---

## Benchmarks

| Metric              | Value                              |
| ------------------- | ---------------------------------- |
| Machine             | AMD Ryzen 7 5700X 8-Core Processor |
| RAM at peak         | 3.45 GB                            |
| Time to first token | 7102 ms                            |
| Generation speed    | 17.92 t/s                          |
| Thermal throttling  | None observed                      |

These are self-reported development benchmarks. Official scores are measured by the ADTC profiler on the standard evaluation machine.
