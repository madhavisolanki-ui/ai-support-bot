import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding # Ye line add karein

load_dotenv()

# 1. Grok LLM setup
llm = OpenAI(
    model="grok-beta",
    api_key=os.getenv("XAI_API_KEY"),
    api_base="https://api.x.ai/v1"
)

# 2. Local Embedding Model setup (OpenAI ki zaroorat nahi padegi)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Settings mein dono set karein
Settings.llm = llm
Settings.embed_model = embed_model

def get_index():
    if not os.path.exists("data") or not os.listdir("data"):
        return None
    
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index