import os
import requests
from bs4 import BeautifulSoup
import chromadb
from chromadb.utils import embedding_functions

# 1. Initialize local vector database
print("Initializing ChromaDB...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Create or reset the collection
try:
    chroma_client.delete_collection(name="think_python")
except:
    pass
collection = chroma_client.create_collection(name="think_python", embedding_function=sentence_transformer_ef)

# 2. Download and parse the textbook
print("Downloading Think Python textbook...")
url = "https://greenteapress.com/thinkpython2/html/index.html"
# For this accelerated build, we will ingest a key foundational chapter (Chapter 5: Conditionals and Recursion)
# to prove the cross-disciplinary load-bearing RAG integration.
chapter_url = "https://greenteapress.com/thinkpython2/html/thinkpython2006.html"

response = requests.get(chapter_url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract text blocks
print("Chunking and embedding text...")
paragraphs = soup.find_all(['p', 'pre'])
chunks = []
current_chunk = ""

for p in paragraphs:
    text = p.get_text().strip()
    if text:
        current_chunk += text + "\n\n"
        # Split at roughly 400 characters to keep embeddings focused
        if len(current_chunk) > 400:
            chunks.append(current_chunk)
            current_chunk = ""

if current_chunk:
    chunks.append(current_chunk)

# 3. Load into ChromaDB
documents = chunks
ids = [f"chap5_chunk_{i}" for i in range(len(chunks))]
metadatas = [{"source": "Think Python, 2nd Edition - Chapter 5", "author": "Allen Downey"} for _ in range(len(chunks))]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"Successfully embedded {len(chunks)} chunks into the local vector store.")
print("RAG database initialization complete.")