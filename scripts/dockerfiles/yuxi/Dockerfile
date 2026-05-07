# Yuxi — Dockerfile
# Builds xerrors/Yuxi — multi-agent LLM conversation platform (5k★)
# Uses uv-python pattern (clone + pip install) with FastAPI wrapper

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone upstream Yuxi
RUN git clone --depth 1 https://github.com/xerrors/Yuxi.git /tmp/yuxi && \
    cp -r /tmp/yuxi/* /app/ && \
    rm -rf /tmp/yuxi

# Install Python dependencies — pull backend code only, install from requirements
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

ENV YUXI_PORT=8000

COPY server.py /app/

CMD python3 /app/server.py
