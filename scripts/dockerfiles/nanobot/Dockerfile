# NanoBot — Dockerfile
# Builds HKUDS/nanobot from source

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone --depth 1 https://github.com/HKUDS/nanobot.git /tmp/nanobot && \
    cp -r /tmp/nanobot/* /app/ && \
    rm -rf /tmp/nanobot

RUN mkdir -p nanobot bridge && touch nanobot/__init__.py

RUN uv pip install --system --no-cache-dir . uvicorn fastapi

COPY scripts/dockerfiles/nanobot/server.py /app/server.py

EXPOSE 8000

ENV NANOBOT_PORT=8000

CMD python3 /app/server.py
