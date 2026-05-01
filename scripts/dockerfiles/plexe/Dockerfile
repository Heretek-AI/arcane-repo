# Plexe — Dockerfile
# Builds plexe-ai/plexe (2,565★) — ML model building from natural language prompts
# Single-service: FastAPI wrapper exposing /health and /info endpoints

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (required by smolagents dependency)
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

# Clone upstream at build time for reproducible builds
RUN git clone --depth 1 --branch v1.4.4 https://github.com/plexe-ai/plexe.git /app/plexe-src

# Install Plexe core + optional framework extras (no PySpark/Java to keep image lean)
RUN pip install --no-cache-dir \
    "/app/plexe-src[tabular,pytorch]" \
    fastapi \
    uvicorn

WORKDIR /app

# Working directories for Plexe data/results
RUN mkdir -p /data /workdir /models

EXPOSE 8000

ENV PLEXE_PORT=8000

COPY scripts/dockerfiles/plexe/server.py /app/server.py

CMD python3 /app/server.py
