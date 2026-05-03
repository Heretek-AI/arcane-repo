---
title: "MLflow"
description: "Open-source MLflow tracking server — experiment tracking, model registry, and deployment management for machine learning workflows"
---

# MLflow

Open-source MLflow tracking server — experiment tracking, model registry, and deployment management for machine learning workflows

## Tags

<a href="/categories/ai" class="tag-badge">ai</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mlflow/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mlflow/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mlflow/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mlflow` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6c2984d25a03e728c6f4f31aebc42452115056084e719dad5bb63b6d31b56fec` |

## Quick Start

1. **Start the MLflow server:**

   ```bash
   docker compose up -d
   ```

2. **Access the MLflow UI:**

   Open [http://localhost:5000](http://localhost:5000) in your browser.

3. **Log your first experiment (Python):**

   ```python
   import mlflow

   mlflow.set_tracking_uri("http://localhost:5000")
   mlflow.set_experiment("my-first-experiment")

   with mlflow.start_run():
       mlflow.log_param("alpha", 0.5)
       mlflow.log_metric("accuracy", 0.92)
       mlflow.log_artifact("model.pkl")
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                   | Default                | Description                                          |
|----------------------------|------------------------|------------------------------------------------------|
| `MLFLOW_PORT`              | `5000`                 | Host port for the MLflow tracking server             |
| `MLFLOW_BACKEND_STORE_URI` | `/app/mlruns`          | Backend store URI (filesystem or database)           |
| `MLFLOW_ARTIFACT_ROOT`     | `/app/mlartifacts`     | Artifact root URI (filesystem or S3/GCS)             |

## Troubleshooting

| Symptom                                    | Likely Cause                        | Fix                                              |
|--------------------------------------------|-------------------------------------|--------------------------------------------------|
| Connection refused on port 5000            | Container still starting            | Wait 30-60 seconds for first build               |
| Experiment logging fails with 404          | Wrong tracking URI                  | Set `MLFLOW_TRACKING_URI=http://localhost:5000`  |
| Volume permission errors                   | Filesystem permissions              | Ensure volumes are writable by the container     |
| Slow startup                               | Building from source on first run   | Expected — packages install during build         |

## API Endpoints

MLflow exposes a REST API on port 5000:

| Endpoint                    | Method | Description                       |
|-----------------------------|--------|-----------------------------------|
| `/api/2.0/mlflow/runs/create` | POST | Create a new run                  |
| `/api/2.0/mlflow/runs/log-parameter` | POST | Log a parameter          |
| `/api/2.0/mlflow/runs/log-metric` | POST | Log a metric              |
| `/api/2.0/mlflow/runs/log-artifact` | POST | Log an artifact          |
| `/api/2.0/mlflow/experiments/create` | POST | Create an experiment     |
| `/api/2.0/mlflow/registered-models/create` | POST | Register a model |

## Health Check

```bash
curl http://localhost:5000/health
```

A healthy server returns a 200 response.

