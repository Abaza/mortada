# Mortada

An Arabic legal Retrieval-Augmented-Generation MVP built with FastAPI and LlamaIndex.

## Setup

```
poetry install
cp .env.example .env
poetry run python scripts/ingest.py data/legal
poetry run uvicorn fastapi_app.main:app --reload
```

### Populating `data/legal`

Place your source documents in the `data/legal/` directory prior to running the
ingest step. The script accepts `.pdf` and `.docx` files and produces a FAISS
index saved under `storage/`.

## Tests

```
poetry run pytest
```

