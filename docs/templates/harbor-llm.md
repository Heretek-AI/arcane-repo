---
title: "Harbor LLM"
description: "LLM backend orchestrator — manage Ollama, vLLM, and other LLM runtimes via Docker with a unified CLI and REST API"
---

# Harbor LLM

LLM backend orchestrator — manage Ollama, vLLM, and other LLM runtimes via Docker with a unified CLI and REST API

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/llm" class="tag-badge">llm</a> <a href="/categories/orchestration" class="tag-badge">orchestration</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/harbor-llm/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/harbor-llm/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/harbor-llm/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `harbor-llm` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `eb5f0008c4dbff4998adb2656824de28926b214151b597f901e168ebfc7fdebc` |

## Architecture

Custom Dockerfile (`scripts/dockerfiles/harbor-llm/Dockerfile`) installs Harbor + FastAPI via pip (python:3.12-slim). Image built and pushed to GHCR via CI (`.github/workflows/build-harbor-llm.yml`).

## Quick Start

1. **Start Harbor:**

   ```bash
   docker compose up -d
   ```

2. **Check health:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **Start LLM backends:**

   ```bash
   curl -X POST http://localhost:8000/harbor/up
   ```

## Configuration

| Variable          | Default | Description                       |
|-------------------|---------|-----------------------------------|
| `HARBOR_LLM_PORT` | `8000`  | Host port for the Harbor REST API |

## Troubleshooting

| Symptom                                  | Cause                   | Fix                                           |
|------------------------------------------|-------------------------|-----------------------------------------------|
| `/harbor/up` → 503                       | Socket not mounted      | Verify volume mount in docker-compose.yml     |
| `docker_socket_available: false`         | Docker not running      | Start Docker daemon on host                   |
| Command timeout (120s)                   | Slow image pull         | Pre-pull images or retry                      |

## API Endpoints

| Endpoint         | Method | Description                          |
|------------------|--------|--------------------------------------|
| `/health`        | GET    | Health check + Docker socket status  |
| `/info`          | GET    | Harbor metadata and commands         |
| `/harbor/up`     | POST   | Start LLM backends                   |
| `/harbor/down`   | POST   | Stop LLM backends                    |
| `/harbor/status` | POST   | Check backend status                 |
| `/harbor/ls`     | POST   | List configured backends             |
| `/harbor/ps`     | POST   | List running containers              |

### Error Codes

| Code | Meaning                              |
|------|--------------------------------------|
| 400  | Disallowed command                   |
| 500  | Command execution / CLI not found    |
| 503  | Docker socket not available          |
| 504  | Command timed out (120s)             |

## Upstream

- **Repository:** [av/harbor](https://github.com/av/harbor)
- **Stars:** 2.9k+
- **License:** MIT

