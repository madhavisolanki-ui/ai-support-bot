import os

from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
)

from llama_index.embeddings.huggingface import (
    HuggingFaceEmbedding,
)

from llama_index.llms.groq import Groq


load_dotenv()


Settings.llm = Groq(
    model="openai/gpt-oss-120b",

    api_key=os.getenv("GROQ_API_KEY"),
)


Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


def get_index():
    data_path = "data"

    if not os.path.exists(data_path) or not os.listdir(data_path):
        return None

    documents = SimpleDirectoryReader(data_path).load_data()

    if len(documents) == 0:
        return None

    # 🔥 ALWAYS rebuild fresh index
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=Settings.embed_model
    )

    return index