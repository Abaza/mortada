from llama_index.embeddings import BaseEmbedding
from sentence_transformers import SentenceTransformer

class STEmbedding(BaseEmbedding):
    def __init__(self):
        self.model = SentenceTransformer("intfloat/multilingual-e5-base")

    def embed(self, text: str):
        return self.model.encode(text)
