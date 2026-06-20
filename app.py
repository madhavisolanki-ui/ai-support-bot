import streamlit as st
from engine import get_index
from llama_index.core import Settings
import engine
import traceback

print("Engine file:", engine.__file__)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="IT Support AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 IT Support AI")
st.caption("Ask questions about company policies, documents, and procedures.")

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Load Index
# -----------------------------
@st.cache_resource
def load_index():
    return get_index()

try:
    index = load_index()

    if index is None:
        st.error(
            "⚠️ Data folder empty hai ya files available nahi hain."
        )
        st.stop()

    query_engine = index.as_query_engine(
    llm=Settings.llm
)

except Exception as e:
    st.error(f"❌ Failed to load index: {e}")
    st.stop()

# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input(
    "Ask a question..."
)

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = query_engine.query(prompt)

                answer = str(response)

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"❌ Error: {e}"
                )
                
                st.code(traceback.format_exc())
                
                
                
