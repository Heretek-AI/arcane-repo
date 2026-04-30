# Cog — ML Container Packaging Tool

[Cog](https://github.com/replicate/cog) from Replicate is a CLI tool for packaging machine learning models into reproducible, production-ready containers. This template exposes Cog via a REST API — build ML model containers and run predictions through HTTP endpoints.

> **Note:** Cog is not a traditional server — it's a model packaging tool. The FastAPI wrapper exposes `/predict` and `/build` endpoints that shell out to the `cog` CLI. Use this for CI/CD model packaging pipelines or as a remote model builder.

## Quick Start

1. **Start Cog:**

   ```bash
   docker compose up -d
   ```

2. **Check health:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **Build a model image** (requires a Cog model repo at the specified path):

   ```bash
   curl -X POST http://localhost:8000/build \
     -H "Content-Type: application/json" \
     -d '{"model_path": "/app/model", "image_name": "my-model"}'
   ```

4. **Run a prediction:**

   ```bash
   curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"model_path": "/app/model", "input_data": {"text": "hello"}}'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable   | Default | Description                  |
|------------|---------|------------------------------|
| `COG_PORT` | `8000`  | Host port for the Cog API    |

## API Endpoints

| Endpoint   | Method | Description                             |
|------------|--------|-----------------------------------------|
| `/health`  | GET    | Health check                            |
| `/info`    | GET    | Cog tool and upstream info              |
| `/predict` | POST   | Run `cog predict` on a model            |
| `/build`   | POST   | Run `cog build` to containerize a model |

### `/predict` Request

```json
{
  "model_path": "/app/model",
  "input_data": { "prompt": "hello" }
}
```

### `/build` Request

```json
{
  "model_path": "/app/model",
  "image_name": "my-model-name"
}
```

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/cog/Dockerfile`) that `pip install`s Cog alongside FastAPI. The FastAPI wrapper provides REST access to the CLI tool, with 300s timeout for predictions and 600s for builds.

## Upstream

- **Repository:** [replicate/cog](https://github.com/replicate/cog)
- **License:** Apache-2.0
