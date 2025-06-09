# Mortada

An Arabic legal Retrieval-Augmented-Generation MVP built with FastAPI and LlamaIndex.

## Setup

```
poetry install
cp .env.example .env
poetry run python scripts/ingest.py data/legal
poetry run uvicorn fastapi_app.main:app --reload
```

## Running on Codespaces

To run the app in GitHub Codespaces, forward **port 8000** and use the default
API key provided in `.env.example`. Once the environment is ready you can start
the server with the usual commands above. Alternatively, you can use Docker by
running:

```bash
docker-compose up
```

## Tests

```
poetry run pytest
```

