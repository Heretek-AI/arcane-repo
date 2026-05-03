---
title: "Streamer Sales"
description: "AI-powered live stream sales assistant — core bot service for automated product demonstrations and sales conversations"
---

# Streamer Sales

AI-powered live stream sales assistant — core bot service for automated product demonstrations and sales conversations

## Tags

<a href="/categories/ai" class="tag-badge">ai</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/streamer-sales/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/streamer-sales/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/streamer-sales/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `streamer-sales` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c294221824f88f9e475b555d9ef037716ae6495ae61e89c6fc7415df5cd3b85a` |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/Streamer-Sales/Dockerfile`) built with the uv-python pattern. The FastAPI wrapper provides health and info documenting the simplification from 7+ services to core bot. Image is built and pushed to GHCR via CI (`.github/workflows/build-Streamer-Sales.yml`).

## Quick Start

1. **Start the sales bot:**

   ```bash
   docker compose up -d
   ```

2. **Check health:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **View bot info:**

   ```bash
   curl http://localhost:8000/info
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                | Default | Description                      |
|-------------------------|---------|----------------------------------|
| `STREAMER_SALES_PORT`   | `8000`  | Host port for the sales bot API  |

## API Endpoints

| Endpoint  | Method | Description              |
|-----------|--------|--------------------------|
| `/health` | GET    | Health check             |
| `/info`   | GET    | Bot and simplification info |

## Upstream

- **Repository:** [PeterH0323/Streamer-Sales](https://github.com/PeterH0323/Streamer-Sales)
- **Stars:** 3.6k+
- **Backend:** Python
- **Upstream services:** 7+

