import streamlit as st
import time
import os
import traceback
from engine import get_index
from llama_index.core import Settings

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Enterprise IT Support AI",
    page_icon="🤖",
    layout="wide",
)

# ---------------------------------
# SESSION STATE
# ---------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0

if "response_times" not in st.session_state:
    st.session_state.response_times = []

# ---------------------------------
# CUSTOM CSS
# ---------------------------------
st.markdown("""
<style>
.stApp{
background:linear-gradient(135deg,#020617,#08111f,#0f172a);
}
.block-container{max-width:1250px;padding-top:1rem;}
.title{text-align:center;font-size:56px;font-weight:800;color:white;}
.subtitle{text-align:center;color:#94a3b8;margin-bottom:25px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# HEADER
# ---------------------------------
st.markdown("""
<div class='title'>🏢 Enterprise IT Support AI</div>
<div class='subtitle'>Smart RAG Assistant for Policies • IT Support • HR Docs</div>
""", unsafe_allow_html=True)

# ---------------------------------
# LOAD INDEX
# ---------------------------------
@st.cache_resource
def load_index():
    return get_index()

try:
    index = load_index()
    query_engine = index.as_query_engine(llm=Settings.llm)
except Exception as e:
    st.error(f"Index load failed: {e}")
    st.stop()

# ---------------------------------
# SIDEBAR
# ---------------------------------
with st.sidebar:
    st.title("📌 Control Panel")

    uploaded_file = st.file_uploader(
        "📤 Upload PDF Document",
        type=["pdf"]
    )

    if uploaded_file:
        os.makedirs("data", exist_ok=True)

        save_path = os.path.join("data", uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())   # ✅ FIXED INDENTATION

        st.success(f"Uploaded: {uploaded_file.name}")

        # Reload index after upload
        try:
            index = get_index()
            query_engine = index.as_query_engine(llm=Settings.llm)
            st.success("Index updated 🚀")
        except Exception as e:
            st.error(f"Failed to update index: {e}")

    st.markdown("---")

    st.subheader("📊 Analytics")

    total_docs = len(os.listdir("data")) if os.path.exists("data") else 0

    st.metric("Documents", total_docs)
    st.metric("Queries", st.session_state.query_count)

    if st.session_state.response_times:
        avg_time = sum(st.session_state.response_times) / len(st.session_state.response_times)
        st.metric("Avg Response (sec)", f"{avg_time:.2f}")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.session_state.response_times = []
        st.rerun()

# ---------------------------------
# WELCOME SCREEN
# ---------------------------------
if len(st.session_state.messages) == 0:
    st.markdown("""
### 👋 Welcome to Enterprise AI Assistant

Try asking:

🧾 Leave policy details  
🔐 How to reset password  
💻 Software installation rules  
📶 WiFi access process  
""")

# ---------------------------------
# CHAT HISTORY
# ---------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if "source" in msg and msg["source"]:
            st.caption(f"📄 Source: {msg['source']}")

# ---------------------------------
# CHAT INPUT
# ---------------------------------
prompt = st.chat_input("Ask anything about company docs...")

if prompt:
    st.session_state.query_count += 1
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        start = time.time()

        try:
            with st.spinner("Searching knowledge base..."):
                response = query_engine.query(prompt)
                answer = str(response)

                source = None
                if hasattr(response, "source_nodes") and response.source_nodes:
                    source = response.source_nodes[0].metadata.get("file_name")

                elapsed = time.time() - start
                st.session_state.response_times.append(elapsed)

                st.markdown(answer)

                if source:
                    st.caption(f"📄 Source: {source}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "source": source
                })

        except Exception as e:
            st.error(f"Error: {e}")
            st.code(traceback.format_exc())

# ---------------------------------
# FOOTER
# ---------------------------------
st.markdown("""
---
<div style='text-align:center;color:#94a3b8'>
Built with RAG • Streamlit • LlamaIndex • Groq 🚀
</div>
""", unsafe_allow_html=True)