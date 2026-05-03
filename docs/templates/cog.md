---
title: "Cog"
description: "ML container packaging tool — build and run reproducible ML models in containers with cog build, predict, and push"
---

# Cog

ML container packaging tool — build and run reproducible ML models in containers with cog build, predict, and push

## Tags

<a href="/categories/ai" class="tag-badge">ai</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cog/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cog/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cog/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cog` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `838ef9cca30fbff8af1f8bb9f704b9ff7db2bbf99047bd5436060cb81b0ef1f2` |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/cog/Dockerfile`) that `pip install`s Cog alongside FastAPI. The FastAPI wrapper provides REST access to the CLI tool, with 300s timeout for predictions and 600s for builds.

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

## Upstream

- **Repository:** [replicate/cog](https://github.com/replicate/cog)
- **License:** Apache-2.0

