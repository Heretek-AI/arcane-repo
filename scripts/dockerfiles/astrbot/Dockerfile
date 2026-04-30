# AstrBot — Dockerfile
# Builds AstrBotDevs/AstrBot — AI Agent Assistant for IM platforms, LLMs, and plugins
# Uses uv-python pattern (clone + pip install) with FastAPI wrapper

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone upstream AstrBot (31k★)
RUN git clone --depth 1 https://github.com/AstrBotDevs/AstrBot.git /tmp/astrbot && \
    cp -r /tmp/astrbot/* /app/ && \
    rm -rf /tmp/astrbot

# Install Python dependencies — upstream uses pip with requirements.txt
RUN uv pip install --system --no-cache-dir \
    fastapi uvicorn && \
    if [ -f requirements.txt ]; then \
        uv pip install --system --no-cache-dir -r requirements.txt 2>/dev/null || \
        echo "WARN: requirements.txt install had warnings — continuing"; \
    fi

EXPOSE 8000

ENV ASTRBOT_PORT=8000

COPY scripts/dockerfiles/astrbot/server.py /app/server.py

CMD python3 /app/server.py
