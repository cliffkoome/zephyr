from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
import requests
import traceback
from sandbox import execute_code

app = FastAPI(title="Offline Coding Tutor API")

# Initialize ChromaDB connection
chroma_client = chromadb.PersistentClient(path="./chroma_db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_collection(name="think_python", embedding_function=sentence_transformer_ef)

class ChatRequest(BaseModel):
    prompt: str
    code_snippet: str = ""
    language: str = "en"  # 'en' or 'sw'

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    # 1. RAG Retrieval
    try:
        results = collection.query(
            query_texts=[request.prompt],
            n_results=2
        )
        retrieved_text = "\n".join(results['documents'][0])
        sources = results['metadatas'][0]
    except Exception as e:
        print(f"RAG Retrieval Notice: {e}")
        retrieved_text = ""
        sources = []

    # 2. Sandbox Execution (if code is provided)
    sandbox_result = ""
    if request.code_snippet:
        print("Executing provided code snippet in sandbox...")
        execution = execute_code(request.code_snippet)
        sandbox_result = f"\n\n[System Sandbox Execution Output]:\n{execution['output']}"

    # 3. Construct System Prompt
    system_instruction = (
        "You are an offline coding tutor for CS students. Your goal is to teach, explain errors, and guide the student. "
        "CRITICAL RULE: You must NEVER write complete solutions for graded assignments. Refuse direct requests to just solve the problem. "
        "Use the provided textbook reference to ground your explanation."
    )
    
    if request.language == "sw":
        system_instruction += " You must provide your final technical explanation strictly in Swahili. Ensure programming terminology remains accurate."

    context_prompt = (
        f"Textbook Reference (Think Python): {retrieved_text}\n"
        f"{sandbox_result}\n\n"
        f"Student Query: {request.prompt}"
    )

    # 4. Call Local Llama.cpp Server with extended timeout
    try:
        response = requests.post(
            "http://127.0.0.1:8080/v1/chat/completions",
            json={
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": context_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 384
            },
            timeout=120  # Extended from 30 to 120 seconds
        )
        response.raise_for_status()
        llm_output = response.json()['choices'][0]['message']['content']
        
        return {
            "response": llm_output,
            "sources": sources,
            "sandbox_executed": bool(request.code_snippet)
        }

    except Exception as e:
        print("Backend Server Error Details:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"LLM Server Error: {str(e)}")