# RD-Agent — Dockerfile
# Builds microsoft/RD-Agent — automated research & development agent
# Uses uv-python pattern (clone + pip install) with FastAPI wrapper

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone upstream RD-Agent
RUN git clone --depth 1 https://github.com/microsoft/RD-Agent.git /tmp/rd-agent && \
    cp -r /tmp/rd-agent/* /app/ && \
    rm -rf /tmp/rd-agent

# Install FastAPI stack only (server.py wraps the upstream CLI, no full source needed)
RUN uv pip install --system --no-cache-dir fastapi uvicorn

EXPOSE 8000

ENV RDAGENT_PORT=8000

COPY scripts/dockerfiles/rd-agent/server.py /app/server.py

CMD python3 /app/server.py
