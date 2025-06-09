from llama_index import ServiceContext
from .embeddings import STEmbedding

service_context = ServiceContext.from_defaults(embed_model=STEmbedding())
