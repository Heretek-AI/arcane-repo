# TradingAgents — Dockerfile
# Builds TauricResearch/TradingAgents (57,924★) — multi-agent LLM financial trading framework
# Single-service: FastAPI wrapper exposing /health and /info endpoints

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone upstream at build time for reproducible builds
RUN git clone --depth 1 --branch v0.2.4 https://github.com/TauricResearch/TradingAgents.git /app/tradingagents-src

# Install TradingAgents and FastAPI deps
RUN pip install --no-cache-dir \
    /app/tradingagents-src \
    fastapi \
    uvicorn

WORKDIR /app

EXPOSE 8000

ENV TRADINGAGENTS_PORT=8000

COPY scripts/dockerfiles/tradingagents/server.py /app/server.py

CMD python3 /app/server.py
