# Memvid — Dockerfile
# Builds memvid/memvid — single-file memory layer for AI agents
# Uses uv-python pattern (clone + pip install memvid-sdk)

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install memvid-sdk from PyPI with document processing extras
RUN uv pip install --system --no-cache-dir \
    memvid-sdk \
    fastapi uvicorn

EXPOSE 8000

ENV MEMVID_PORT=8000
ENV MEMVID_DATA_DIR=/app/data
ENV MEMVID_FILE=default.mv2
ENV MEMVID_EMBED_MODE=local
ENV MEMVID_LOG_LEVEL=info

COPY scripts/dockerfiles/memvid/server.py /app/server.py

CMD python3 /app/server.py
