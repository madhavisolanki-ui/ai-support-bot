import os
import logging
from pathlib import Path
from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
)
logger = logging.getLogger("Enterprise_RAG_Engine")

class IndexManager:
    def __init__(self, persist_dir: str = "./storage", data_dir: str = "./data"):
        self.persist_dir = Path(persist_dir)
        self.data_dir = Path(data_dir)
        self._setup_settings()

    def _setup_settings(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not set in the environment.")

        Settings.llm = Groq(
            model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
            api_key=api_key,
        )
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        Settings.chunk_size = 512
        Settings.chunk_overlap = 50

    def _build_index(self) -> VectorStoreIndex:
        if not self.data_dir.exists() or not any(self.data_dir.iterdir()):
            raise FileNotFoundError(f"Knowledge base empty at {self.data_dir}")

        logger.info("Building new vector index from source documents...")
        documents = SimpleDirectoryReader(
            self.data_dir,
            file_metadata=lambda file_path: {"file_name": Path(file_path).name},
        ).load_data()

        index = VectorStoreIndex.from_documents(
            documents,
            show_progress=True,
        )

        self.persist_dir.mkdir(parents=True, exist_ok=True)
        index.storage_context.persist(persist_dir=self.persist_dir)
        logger.info(f"Index successfully persisted to {self.persist_dir}")
        return index

    def get_index(self) -> VectorStoreIndex:
        if self.persist_dir.exists() and any(self.persist_dir.iterdir()):
            try:
                logger.info("Loading existing index from disk.")
                storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
                return load_index_from_storage(storage_context)
            except Exception as e:
                logger.error(f"Index load failure: {e}. Rebuilding...")

        return self._build_index()

_manager = IndexManager()

def get_index():
    return _manager.get_index()
