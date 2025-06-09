# Mortada

An Arabic legal Retrieval-Augmented-Generation MVP built with FastAPI and LlamaIndex.

## Setup

```
poetry install
cp .env.example .env
poetry run python scripts/ingest.py data/legal
poetry run uvicorn fastapi_app.main:app --reload
```

## Tests

```
poetry run pytest
```

