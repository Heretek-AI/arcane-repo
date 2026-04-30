# OpenSpiel — Multi-stage Dockerfile
# Builds Google DeepMind's OpenSpiel game theory framework

FROM python:3.12-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir open-spiel

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN pip install --no-cache-dir uvicorn fastapi

COPY scripts/dockerfiles/openspiel/server.py /app/server.py

EXPOSE 8080

ENV OPENSPIEL_PORT=8080

CMD python3 /app/server.py
