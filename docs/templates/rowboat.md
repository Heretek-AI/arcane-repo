---
title: "Rowboat"
description: "Open-source AI coworker with knowledge graph — turns work into a knowledge graph and acts on it"
---

# Rowboat

Open-source AI coworker with knowledge graph — turns work into a knowledge graph and acts on it

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/multi-service" class="tag-badge">multi-service</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rowboat/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rowboat/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rowboat/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `rowboat` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6c353478f08a642b6d5b427d55f91a85d03fc45da99cc6de843d1a7cc84aac59` |

## Architecture

Rowboat is deployed as a **custom-build** template (MEM036: node-alpine multi-stage build). The Dockerfile clones upstream source at build time and produces a production image pushed to GHCR.

### Core Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `rowboat` | `ghcr.io/heretek-ai/arcane-repo/rowboat:latest` | 8080→8000 | Main Next.js app (custom-built from source) |
| `mongo` | `mongo:7` | 27017 | Document database |
| `redis` | `redis:7-alpine` | 6379 | Job queue / caching |
| `qdrant` | `qdrant/qdrant:latest` | 6333 | Vector database (RAG) |

### Upstream Changes (April 2026)

The upstream `rowboat_agents` and `copilot` services (previously in `docker-compose.yml` with `build:` contexts) no longer exist on the `main` branch. Rowboat has merged the agent runtime into the main Next.js app. Our template uses a single custom Dockerfile for the main app + Docker Hub images for infrastructure services.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Set your LLM API key:**

   Edit `.env` and set `OPENAI_API_KEY` (required for AI features).

3. **Start all services:**

   ```bash
   docker compose up -d
   ```

4. **Access the web UI:**

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

- `OPENAI_API_KEY` — required for AI features
- `ROWBOAT_PORT` — host port for web UI (default: 8080)
- `MONGO_USER` / `MONGO_PASSWORD` — MongoDB credentials
- `USE_RAG` — enable Qdrant vector search (requires QDRANT_API_KEY)
- `USE_COMPOSIO_TOOLS` — enable Composio tool integrations

