# OpenFang — Federated Learning Attack Platform
# Upstream: RightNow-AI/openfang — multi-stage Rust binary
# Builds the Rust binary via rust:1-slim-bookworm, then wraps in FastAPI on python:3.12-slim
#
# Pattern: Rust builder → python:3.12-slim runtime with FastAPI wrapper
# The upstream binary (openfang) is built at docker build time; runtime uses python:3.12-slim

FROM rust:1-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libssl-dev \
    perl \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Clone upstream OpenFang (agent operating system, federated learning attacks)
RUN git clone --depth 1 https://github.com/RightNow-AI/openfang.git /tmp/openfang && \
    cp -r /tmp/openfang/* /build/ && \
    rm -rf /tmp/openfang

# Build release binary
ENV CARGO_PROFILE_RELEASE_LTO=true \
    CARGO_PROFILE_RELEASE_CODEGEN_UNITS=1
RUN cargo build --release --bin openfang

# ─── Production runtime ────────────────────────────────────────────────
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the compiled Rust binary from builder
COPY --from=builder /build/target/release/openfang /usr/local/bin/openfang

# Copy agents directory (referenced by openfang at runtime)
COPY --from=builder /build/agents /opt/openfang/agents

# Install FastAPI + uvicorn for the wrapper
RUN pip install --no-cache-dir fastapi uvicorn

# Copy our FastAPI wrapper server
COPY scripts/dockerfiles/openfang/server.py /app/server.py

# Health check via FastAPI wrapper
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

ENV OPENFANG_PORT=8000
ENV OPENFANG_HOME=/data
ENV PYTHONUNBUFFERED=1

VOLUME /data

CMD ["python3", "/app/server.py"]
