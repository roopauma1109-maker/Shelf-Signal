FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/home/appuser/.cache/huggingface

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data/processed/faiss.index ./data/processed/faiss.index
COPY data/processed/chunks_metadata.jsonl ./data/processed/chunks_metadata.jsonl

RUN useradd --create-home appuser \
    && mkdir -p /app/logs /home/appuser/.cache/huggingface \
    && chown -R appuser:appuser /app /home/appuser/.cache

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]