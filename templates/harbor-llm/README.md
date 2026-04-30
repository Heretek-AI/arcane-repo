# Harbor LLM — LLM Backend Orchestrator

[Harbor](https://github.com/av/harbor) (2.9k+ ★) is a Docker-based LLM backend orchestrator providing a unified CLI (`harbor up/down/status`) for managing LLM runtimes — Ollama, vLLM, llama.cpp, and others. This template wraps Harbor as a REST API.

## Docker-in-Docker Pattern

> **Important:** Harbor manages LLM backends by spawning Docker containers. From within its own container, it needs access to the host's Docker daemon via the Docker socket.

### How it works

The `docker-compose.yml` mounts the host's Docker socket:

```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

Harbor uses the host's Docker daemon directly — not true Docker-in-Docker (dind) — to manage sibling containers.

### Security Considerations

Mounting the Docker socket grants **full daemon control** (effectively root). For personal/dev use this is fine. For production, consider Docker authorization plugins or rootless Docker.

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

## Architecture

Custom Dockerfile (`scripts/dockerfiles/harbor-llm/Dockerfile`) installs Harbor + FastAPI via pip (python:3.12-slim). Image built and pushed to GHCR via CI (`.github/workflows/build-harbor-llm.yml`).

## Troubleshooting

| Symptom                                  | Cause                   | Fix                                           |
|------------------------------------------|-------------------------|-----------------------------------------------|
| `/harbor/up` → 503                       | Socket not mounted      | Verify volume mount in docker-compose.yml     |
| `docker_socket_available: false`         | Docker not running      | Start Docker daemon on host                   |
| Command timeout (120s)                   | Slow image pull         | Pre-pull images or retry                      |

## Upstream

- **Repository:** [av/harbor](https://github.com/av/harbor)
- **Stars:** 2.9k+
- **License:** MIT
