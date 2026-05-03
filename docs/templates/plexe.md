---
title: "Plexe"
description: "AI agent orchestration with observability and debugging"
---

# Plexe

AI agent orchestration with observability and debugging

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/orchestration" class="tag-badge">orchestration</a> <a href="/categories/observability" class="tag-badge">observability</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/plexe/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/plexe/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/plexe/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `plexe` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `232407de60e39a379de3bab31f2f312dff5af520ef3a5dcf2812575b9b30a815` |

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the service:**

   Open [http://localhost:8000](http://localhost:8000) in your browser.

   > **Build:** This is a custom-build template — the Docker image is built from source and hosted on GHCR (`ghcr.io/heretek-ai/arcane-repo/plexe:latest`). No pre-built public image exists upstream.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|----------|-------------|-----|
| `docker compose up` fails | Image not yet built/pulled | Run `docker compose build` to build locally, or wait for CI-published image |
| Port conflict | Another service on port 8000 | Change `PLEXE_PORT` in `.env` |
| Container exits immediately | Build failure | Run `docker compose logs plexe` for details |

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

