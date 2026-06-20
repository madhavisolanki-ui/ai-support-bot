import streamlit as st
from engine import get_index

st.title("IT Support AI 🤖")

# Index load karna
index = get_index()
chat_engine = index.as_chat_engine(chat_mode="context")

# Chat history handle karna
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask about company policy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Response generate karna
    response = chat_engine.chat(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": str(response)})

index = get_index()
if index is None:
    st.error("Data folder is empty! Please add some PDF or TXT files to the 'data' folder.")
    st.stop() # App ko yahi rok dega