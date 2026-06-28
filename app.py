import streamlit as st
import time
import logging
from pathlib import Path
from engine import get_index
from llama_index.core import Settings

# --- CONFIG & LOGGING ---
st.set_page_config(page_title="Enterprise IT Support AI", page_icon="🤖", layout="wide")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .chat-message { border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    div[data-testid="stChatMessage"] { background-color: #1e293b; }
    .stSpinner { text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "query_count" not in st.session_state: st.session_state.query_count = 0

# --- ENGINE ---
@st.cache_resource(show_spinner=True)
def get_engine():
    try:
        index = get_index()
        # Use chat_engine for better conversational memory
        return index.as_chat_engine(chat_mode="context", llm=Settings.llm) if index else None
    except Exception as e:
        logger.error(f"Engine Init Error: {e}")
        return None

chat_engine = get_engine()

# --- SIDEBAR ANALYTICS ---
with st.sidebar:
    st.title("📊 Control Panel")
    st.metric("Total Queries", st.session_state.query_count)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN UI ---
st.title("🏢 Enterprise IT Support AI")
st.markdown("---")

# Render History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Logic
if prompt := st.chat_input("Ask about company policy..."):
    if not chat_engine:
        st.error("Engine not initialized. Check 'data/' folder.")
        st.stop()

    st.session_state.query_count += 1
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Response with Streaming Effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Using stream_chat for better performance/UX
            response = chat_engine.stream_chat(prompt)
            
            for token in response.response_gen:
                full_response += token
                message_placeholder.markdown(full_response + "▌")
            
            # Append source metadata
            sources = list(set([node.metadata.get("file_name", "Unknown") for node in response.source_nodes]))
            full_response += f"\n\n---\n📚 **Sources:** {', '.join(sources)}"
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            logger.error(f"Inference error: {e}")
            st.error("Processing failed.")