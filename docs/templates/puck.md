---
title: "Puck"
description: "AI agent orchestration and automation tool — manage and coordinate multi-agent workflows with configurable pipelines and event-driven execution"
---

# Puck

AI agent orchestration and automation tool — manage and coordinate multi-agent workflows with configurable pipelines and event-driven execution

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/orchestration" class="tag-badge">orchestration</a> <a href="/categories/automation" class="tag-badge">automation</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/workflow" class="tag-badge">workflow</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/puck/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/puck/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/puck/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `puck` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `83e02d09cf4dc93d217ba59be0753f5da5d36203ae665c753f2e9b5f5f65805a` |

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

Copy `.env.example` to `.env` and edit:

| Variable     | Default     | Description                                    |
|--------------|-------------|------------------------------------------------|
| `PUCK_PORT`  | `8000`      | Host port for the informational API            |

## Troubleshooting

| Symptom                              | Likely Cause                 | Fix                                                |
|--------------------------------------|------------------------------|----------------------------------------------------|
| No agent orchestration available      | This is an informational stub | Install `puck` via pip for full capabilities       |
| Container exits immediately           | pip install failure          | Run `docker compose logs puck` for details         |
| Need advanced pipeline features      | Not available in this stub   | Use pip-installed puck for complete functionality  |

## API Endpoints

| Endpoint   | Method | Description                         |
|------------|--------|-------------------------------------|
| `/health`  | GET    | Health check                        |
| `/guide`   | GET    | Usage guidance and CLI/Python examples |

