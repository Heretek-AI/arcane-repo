---
title: "Clawith"
description: "Enterprise AI digital employee platform — multi-service workflow builder with visual canvas, agent orchestration, and OKR management"
---

# Clawith

Enterprise AI digital employee platform — multi-service workflow builder with visual canvas, agent orchestration, and OKR management

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/workflow" class="tag-badge">workflow</a> <a href="/categories/orchestration" class="tag-badge">orchestration</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/low-code" class="tag-badge">low-code</a> <a href="/categories/multi-service" class="tag-badge">multi-service</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/clawith/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/clawith/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/clawith/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `clawith` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `42576026382cfc437ccb51b5afe7e6dfc27fe3bda43dbe3ab45a62041334c512` |

## Architecture

Clawith is a multi-service application:
- **Backend**: FastAPI (Python 3.12) with async PostgreSQL and Redis
- **Frontend**: React 19 / Vite SPA built as static assets
- **Database**: PostgreSQL 15 (automatically included in docker-compose)
- **Cache/Queue**: Redis 7 (automatically included in docker-compose)

The container image is built from upstream source via a custom Dockerfile and published to GitHub Container Registry.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** — at minimum, change `SECRET_KEY` and `JWT_SECRET_KEY` for security.

3. **Start all services:**

   ```bash
   docker compose up -d
   ```

4. **Access the service:**

   Open [http://localhost:8000](http://localhost:8000) in your browser.

   The API health check is at `/api/health`.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `CLAWITH_PORT` | `8000` | Host port for the combined API + frontend |
| `POSTGRES_DB` | `clawith` | PostgreSQL database name |
| `POSTGRES_USER` | `clawith` | PostgreSQL user |
| `POSTGRES_PASSWORD` | `clawith` | PostgreSQL password |
| `SECRET_KEY` | (change me) | Backend secret for session tokens |
| `JWT_SECRET_KEY` | (change me) | JWT signing key |
| `CORS_ORIGINS` | `'["*"]'` | Allowed CORS origins |
| `PUBLIC_BASE_URL` | `http://localhost:8000` | Public URL for OAuth callbacks |
| `FEISHU_APP_ID` | (optional) | Feishu/Lark integration |
| `FEISHU_APP_SECRET` | (optional) | Feishu/Lark secret |

## Service Details

The `docker-compose.yml` runs three services with health checks:
- `clawith` — the main application container (GHCR image)
- `postgres` — PostgreSQL 15 with persistent volume
- `redis` — Redis 7 with persistent volume

Both PostgreSQL and Redis must be healthy before the main app starts.

