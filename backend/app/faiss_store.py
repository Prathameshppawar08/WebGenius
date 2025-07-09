import os
import pickle
from typing import List

from langchain_core.documents import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# 📂 Where the index will be saved
FAISS_DIR = "faiss_index"
FAISS_INDEX_FILE = os.path.join(FAISS_DIR, "index.faiss")
FAISS_PICKLE_FILE = os.path.join(FAISS_DIR, "index.pkl")

# 🧠 Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def create_vector_store(chunks: List[Document]):
    """Create FAISS vector store from chunks and save it to disk."""
    if not os.path.exists(FAISS_DIR):
        os.makedirs(FAISS_DIR)

    print("[FAISS] Creating vector store...")
    vector_store = FAISS.from_documents(chunks, embedding_model)

    print("[FAISS] Saving vector store to disk...")
    vector_store.save_local(FAISS_DIR)
    print("[FAISS] Vector store saved successfully!")


def load_vector_store() -> FAISS:
    """Load FAISS vector store from disk."""
    print("[FAISS] Loading vector store from disk...")
    return FAISS.load_local(FAISS_DIR, embedding_model)


def search_similar_documents(query: str, k: int = 3) -> List[Document]:
    """Search top-k documents similar to the query."""
    vector_store = load_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return results
