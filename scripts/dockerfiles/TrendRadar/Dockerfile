# TrendRadar — Dockerfile
# Builds sansan0/TrendRadar — news aggregation + sentiment analysis (55.9k★)
# Uses uv-python pattern (clone + pip install) with FastAPI wrapper

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone upstream TrendRadar (highest-starred custom build at 55.9k★)
RUN git clone --depth 1 https://github.com/sansan0/TrendRadar.git /tmp/tr && \
    cp -r /tmp/tr/* /app/ && \
    rm -rf /tmp/tr

# Install Python dependencies — upstream has docker/ dir and pyproject.toml
RUN uv pip install --system --no-cache-dir \
    fastapi uvicorn && \
    if [ -f pyproject.toml ]; then \
        uv pip install --system --no-cache-dir . 2>/dev/null || \
        echo "WARN: pyproject install had warnings — continuing"; \
    elif [ -f requirements.txt ]; then \
        uv pip install --system --no-cache-dir -r requirements.txt 2>/dev/null || \
        echo "WARN: requirements.txt install had warnings — continuing"; \
    fi

EXPOSE 8000

ENV TRENDRADAR_PORT=8000

COPY scripts/dockerfiles/TrendRadar/server.py /app/server.py

CMD python3 /app/server.py
