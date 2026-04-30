# Cog — Dockerfile
# Builds replicate/cog — ML container packaging tool
# CLI tool pattern with FastAPI wrapper exposing /predict endpoint

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Cog CLI and FastAPI deps
RUN pip install --no-cache-dir \
    cog \
    fastapi \
    uvicorn

EXPOSE 8000

ENV COG_PORT=8000

COPY scripts/dockerfiles/cog/server.py /app/server.py

CMD python3 /app/server.py
