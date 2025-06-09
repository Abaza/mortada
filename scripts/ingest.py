import sys
from pathlib import Path
from pdfminer.high_level import extract_text
from docx import Document
from llama_index import VectorStoreIndex, Document as LlamaDoc
from fastapi_app.embeddings import STEmbedding

CHUNK=500
OVERLAP=50
folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('data/legal')
texts = []
for p in folder.rglob('*'):
    if p.suffix == '.pdf':
        texts.append(extract_text(p))
    elif p.suffix == '.docx':
        texts.append('\n'.join(par.text for par in Document(p).paragraphs))
segments = [
    ' '.join(t.split()[i:i+CHUNK])
    for t in texts
    for i in range(0, len(t.split()), CHUNK-OVERLAP)
]
docs = [LlamaDoc(text=s) for s in segments]
index = VectorStoreIndex.from_documents(docs, embed_model=STEmbedding())
index.storage_context.vector_store.persist('storage')
