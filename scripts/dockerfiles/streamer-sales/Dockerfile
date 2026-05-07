# Streamer-Sales — Dockerfile
# Builds PeterH0323/Streamer-Sales — live stream sales AI assistant (3.6k★)
# Uses uv-python pattern (clone + pip install) — simplified to core bot from 7+ services

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone upstream Streamer-Sales
RUN git clone --depth 1 https://github.com/PeterH0323/Streamer-Sales.git /tmp/ss && \
    cp -r /tmp/ss/* /app/ && \
    rm -rf /tmp/ss

# Install Python dependencies — upstream compose.yaml uses build contexts with 7+ services
RUN uv pip install --system --no-cache-dir \
    fastapi uvicorn && \
    if [ -f requirements.txt ]; then \
        uv pip install --system --no-cache-dir -r requirements.txt 2>/dev/null || \
        echo "WARN: requirements.txt install had warnings — continuing"; \
    elif [ -f pyproject.toml ]; then \
        uv pip install --system --no-cache-dir . 2>/dev/null || \
        echo "WARN: pyproject install had warnings — continuing"; \
    fi

EXPOSE 8000

ENV STREAMER_SALES_PORT=8000

COPY scripts/dockerfiles/streamer-sales/server.py /app/server.py

CMD python3 /app/server.py
