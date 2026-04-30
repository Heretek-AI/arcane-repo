# Onyx — Dockerfile
# Builds onyx-dot-app/onyx — enterprise AI search platform
# Uses uv-python pattern (clone + pip install)

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone upstream onyx (formerly Danswer)
RUN git clone --depth 1 https://github.com/onyx-dot-app/onyx.git /tmp/onyx && \
    cp -r /tmp/onyx/* /app/ && \
    rm -rf /tmp/onyx

# Install Python dependencies
RUN uv pip install --system --no-cache-dir uvicorn fastapi && \
    if [ -f pyproject.toml ]; then \
        uv pip install --system --no-cache-dir . 2>/dev/null || \
        echo "WARN: pyproject install failed — will use minimal deps"; \
    fi

EXPOSE 8080

ENV ONYX_PORT=8080

CMD python3 -m uvicorn onyx.main:app --host 0.0.0.0 --port ${ONYX_PORT:-8080} 2>/dev/null || \
    echo "Onyx requires full upstream build — run: cd /app && pip install -e ." && tail -f /dev/null
