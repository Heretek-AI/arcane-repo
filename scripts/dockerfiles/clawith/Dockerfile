# Clawith — Multi-service AI workflow builder (backend + frontend)
# Upstream: dataelement/Clawith — enterprise digital employee platform
# Builds backend (FastAPI + pip) and frontend (React/Vite + nginx) into a single image
#
# Pattern: uv-python multi-stage with node-alpine frontend build
# Upstream has per-service Dockerfiles; we consolidate into our custom-build pattern.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS backend-builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Clone upstream Clawith (2.3k★, enterprise agent orchestration)
RUN git clone --depth 1 https://github.com/dataelement/Clawith.git /tmp/clawith && \
    cp -r /tmp/clawith/backend/* /build/ && \
    rm -rf /tmp/clawith

# Install Python dependencies from pyproject.toml
RUN uv pip install --system --no-cache-dir .

# ─── Frontend build ────────────────────────────────────────────────────
FROM node:lts-alpine AS frontend-builder

WORKDIR /frontend

RUN apk add --no-cache git

RUN git clone --depth 1 https://github.com/dataelement/Clawith.git /tmp/clawith && \
    cp -r /tmp/clawith/frontend/* /frontend/ && \
    rm -rf /tmp/clawith

RUN npm ci && npm run build

# ─── Production runtime ────────────────────────────────────────────────
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed Python packages from backend build
COPY --from=backend-builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=backend-builder /usr/local/bin/ /usr/local/bin/

# Copy built frontend assets
COPY --from=frontend-builder /frontend/dist/ /app/static/

# Copy application code from backend build
COPY --from=backend-builder /build/ /app/

# Copy our FastAPI wrapper server (serves API + static frontend)
COPY scripts/dockerfiles/clawith/server.py /app/server.py

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

EXPOSE 8000

ENV CLAWITH_PORT=8000
ENV PYTHONUNBUFFERED=1

CMD ["python3", "/app/server.py"]
