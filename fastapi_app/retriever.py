from pathlib import Path

try:
    from llama_index import VectorStoreIndex
    from llama_index.vector_stores.faiss import FaissVectorStore
    from .embeddings import STEmbedding
    _HAVE_LLAMA = True
except Exception:  # pragma: no cover - optional heavy deps
    _HAVE_LLAMA = False

INDEX_PATH = Path("storage/index.faiss")
if _HAVE_LLAMA:
    embed_model = STEmbedding()


def load_index():
    if not _HAVE_LLAMA:
        return None
    if INDEX_PATH.exists():
        store = FaissVectorStore.from_persist_dir("storage")
        return VectorStoreIndex.from_vector_store(store, embed_model=embed_model)
    return VectorStoreIndex([], embed_model=embed_model)


def retrieve(query: str, k: int = 5):
    if not _HAVE_LLAMA:
        return [("", "0")]
    index = load_index()
    nodes = index.as_retriever(similarity_top_k=k).retrieve(query)
    return [(n.text, n.node_id) for n in nodes]
