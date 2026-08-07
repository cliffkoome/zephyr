import streamlit as st
import requests

st.set_page_config(page_title="Offline Coding Tutor", layout="wide")

st.title("Offline AI Coding Tutor")
st.markdown("Grounded in *Think Python, 2nd Edition* by Allen Downey. CC-BY-NC 3.0.")

# Sidebar Configuration
with st.sidebar:
    st.header("Tutor Settings")
    language = st.radio("Explanation Language:", ["English", "Swahili (Kiswahili)"])
    lang_code = "sw" if language == "Swahili (Kiswahili)" else "en"
    
    st.divider()
    
    st.header("Execution Sandbox")
    st.markdown("Paste code here to have the tutor run it and explain the output or errors.")
    code_input = st.text_area("Python Snippet:", height=200, placeholder="print('Hello World')")

# Initialize chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input Trigger
if prompt := st.chat_input("Ask a question about Python (e.g., 'What is recursion?')..."):
    
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call Backend and show response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing and retrieving course material..."):
            try:
                payload = {
                    "prompt": prompt,
                    "code_snippet": code_input,
                    "language": lang_code
                }
                res = requests.post("http://127.0.0.1:8000/chat", json=payload)
                res.raise_for_status()
                data = res.json()
                
                response_text = data["response"]
                sources = data.get("sources", [])
                
                # Display LLM Response
                st.markdown(response_text)
                
                # Display RAG Citations
                if sources:
                    source_str = "\n".join([f"- {s.get('source', 'Unknown')} ({s.get('author', 'Unknown')})" for s in sources])
                    st.info(f"**Sources Referenced:**\n{source_str}")
                
                # Display Sandbox Status
                if data.get("sandbox_executed"):
                    st.success("Code snippet executed in local sandbox.")
                    
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except requests.exceptions.RequestException as e:
                st.error(f"Backend Server Error: Is uvicorn running? Details: {e}")