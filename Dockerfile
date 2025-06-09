FROM python:3.11-slim as base
WORKDIR /app
COPY pyproject.toml .
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn","fastapi_app.main:app","--host","0.0.0.0","--port","8000"]
