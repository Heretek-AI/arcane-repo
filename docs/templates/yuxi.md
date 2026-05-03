---
title: "Yuxi"
description: "Multi-agent LLM conversation platform with modular agent architecture, knowledge base integration, and tool ecosystem"
---

# Yuxi

Multi-agent LLM conversation platform with modular agent architecture, knowledge base integration, and tool ecosystem

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/llm" class="tag-badge">llm</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yuxi/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yuxi/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yuxi/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `yuxi` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `17c6d20f8a68c1c77eec67371d4dca16b803632eea448509142fba6c30e60413` |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/Yuxi/Dockerfile`) built with the uv-python pattern. The FastAPI server wrapper provides health and info endpoints alongside the upstream application's entrypoint. Image is built and pushed to GHCR via CI (`.github/workflows/build-Yuxi.yml`).

## Quick Start

1. **Start the stack:**

   ```bash
   docker compose up -d
   ```

2. **Check health:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **View platform info:**

   ```bash
   curl http://localhost:8000/info
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable              | Default  | Description                         |
|-----------------------|----------|-------------------------------------|
| `YUXI_PORT`           | `8000`   | Host port for the Yuxi API          |
| `POSTGRES_DB`         | `yuxi`   | PostgreSQL database name            |
| `POSTGRES_USER`       | `yuxi`   | PostgreSQL user                     |
| `POSTGRES_PASSWORD`   | `yuxi`   | PostgreSQL password                 |

## API Endpoints

| Endpoint  | Method | Description                   |
|-----------|--------|-------------------------------|
| `/health` | GET    | Health check                  |
| `/info`   | GET    | Platform and upstream details |

## Upstream

- **Repository:** [xerrors/Yuxi](https://github.com/xerrors/Yuxi)
- **Stars:** 5k+
- **Backend:** Python

