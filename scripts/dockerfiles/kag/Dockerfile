# KAG — Dockerfile
# Builds OpenSPG/KAG — knowledge-augmented generation framework
# Uses uv-python pattern (clone + pip install) with FastAPI wrapper

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone upstream KAG
RUN git clone --depth 1 https://github.com/OpenSPG/KAG.git /tmp/kag && \
    cp -r /tmp/kag/* /app/ && \
    rm -rf /tmp/kag

# Install Python dependencies
RUN uv pip install --system --no-cache-dir \
    . \
    fastapi uvicorn

EXPOSE 8000

ENV KAG_PORT=8000

COPY scripts/dockerfiles/kag/server.py /app/server.py

CMD python3 /app/server.py
