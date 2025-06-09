from pathlib import Path
from llama_index import VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore
from .embeddings import STEmbedding

INDEX_PATH = Path("storage/index.faiss")
embed_model = STEmbedding()


def load_index():
    if INDEX_PATH.exists():
        store = FaissVectorStore.from_persist_dir("storage")
        return VectorStoreIndex.from_vector_store(store, embed_model=embed_model)
    return VectorStoreIndex([], embed_model=embed_model)


def retrieve(query: str, k: int = 5):
    index = load_index()
    nodes = index.as_retriever(similarity_top_k=k).retrieve(query)
    return [(n.text, n.node_id) for n in nodes]
