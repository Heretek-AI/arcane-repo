---
title: "SimStudio AI"
description: "3D simulation and AI agent environment platform — create, train, and evaluate AI agents in photorealistic 3D virtual worlds for reinforcement learning and embodied AI research"
---

# SimStudio AI

3D simulation and AI agent environment platform — create, train, and evaluate AI agents in photorealistic 3D virtual worlds for reinforcement learning and embodied AI research

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/simstudioai/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/simstudioai/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/simstudioai/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `simstudioai` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `178e59208722e6be4a06cfc2bf012fc94eb7d7080809c554fd2871ab29ba2c1d` |

## Quick Start

1. **Start the API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **Get usage guidance:**

   ```bash
   curl http://localhost:8000/guide
   ```

## Configuration

| Variable            | Default     | Description                                    |
|---------------------|-------------|------------------------------------------------|
| `SIMSTUDIOAI_PORT`  | `8000`      | Host port for the informational API            |

## Troubleshooting

| Symptom                              | Likely Cause                     | Fix                                                    |
|--------------------------------------|----------------------------------|--------------------------------------------------------|
| No simulation available               | This is an informational stub    | Install simstudio-ai on GPU hardware for full features |
| Container exits immediately           | pip install failure              | Run `docker compose logs simstudioai` for details      |
| GPU not detected in Docker            | GPU passthrough not configured   | Add `deploy: resources: reservations: devices: ...`    |

## API Endpoints

| Endpoint   | Method | Description                         |
|------------|--------|-------------------------------------|
| `/health`  | GET    | Health check                        |
| `/guide`   | GET    | Usage guidance and setup notes      |

