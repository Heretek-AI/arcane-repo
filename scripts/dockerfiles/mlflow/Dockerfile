# MLflow — Dockerfile
# Builds mlflow/mlflow — MLflow tracking server
# Uses uv-python pattern (clone + pip install)

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone upstream mlflow
RUN git clone --depth 1 https://github.com/mlflow/mlflow.git /tmp/mlflow && \
    cp -r /tmp/mlflow/* /app/ && \
    rm -rf /tmp/mlflow

# Install MLflow with standard extras
RUN uv pip install --system --no-cache-dir \
    "mlflow[extras]" \
    uvicorn

EXPOSE 5000

ENV MLFLOW_PORT=5000
ENV MLFLOW_TRACKING_URI=http://0.0.0.0:${MLFLOW_PORT:-5000}

# Start the MLflow tracking server
CMD mlflow server \
    --host 0.0.0.0 \
    --port ${MLFLOW_PORT:-5000} \
    --backend-store-uri ${MLFLOW_BACKEND_STORE_URI:-/app/mlruns} \
    --default-artifact-root ${MLFLOW_ARTIFACT_ROOT:-/app/mlartifacts}
