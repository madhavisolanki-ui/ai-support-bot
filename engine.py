import os
import logging
from pathlib import Path
from dotenv import load_dotenv

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Global Settings
# Note: Ensure the model exists on Groq; "llama3-70b-8192" is standard
Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

PERSIST_DIR = Path("./storage")
DATA_DIR = Path("./data")

def get_index():
    """Returns a robust, persistent index."""
    
    # 1. Check if index exists and is valid
    if PERSIST_DIR.exists() and any(PERSIST_DIR.iterdir()):
        try:
            logger.info("Loading index from persistent storage...")
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            return load_index_from_storage(storage_context)
        except Exception as e:
            logger.warning(f"Failed to load existing index: {e}. Rebuilding...")

    # 2. Build index if not found or corrupted
    if not DATA_DIR.exists() or not any(DATA_DIR.iterdir()):
        logger.error("No data found in /data directory.")
        return None

    logger.info("Building new index from /data directory...")
    
    # Use file_metadata to ensure nodes carry the filename for the UI
    def get_meta(file_path):
        return {"file_name": os.path.basename(file_path)}

    documents = SimpleDirectoryReader(
        DATA_DIR, 
        file_metadata=get_meta
    ).load_data()
    
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=Settings.embed_model,
        show_progress=True
    )
    
    # 3. Persist
    PERSIST_DIR.mkdir(exist_ok=True)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    logger.info("Index built and persisted successfully.")
    
    return index