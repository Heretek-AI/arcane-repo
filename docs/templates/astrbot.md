---
title: "AstrBot"
description: "All-in-one AI agent assistant with multi-platform IM integration, LLM backend support, and extensible plugin system"
---

# AstrBot

All-in-one AI agent assistant with multi-platform IM integration, LLM backend support, and extensible plugin system

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/llm" class="tag-badge">llm</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/astrbot/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/astrbot/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/astrbot/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `astrbot` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `83c41a83f19f45b46825f287dfeba375380162f5611f530764f522fdc146791f` |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/astrbot/Dockerfile`) that clones the upstream AstrBot repository and wraps it with a FastAPI health/info server. The image is built and pushed to GHCR automatically via CI (`.github/workflows/build-astrbot.yml`).

## Quick Start

1. **Start the bot:**

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

| Variable        | Default | Description                   |
|-----------------|---------|-------------------------------|
| `ASTRBOT_PORT`  | `8000`  | Host port for the bot API     |

## API Endpoints

| Endpoint  | Method | Description              |
|-----------|--------|--------------------------|
| `/health` | GET    | Health check             |
| `/info`   | GET    | Bot and upstream details |

## Upstream

- **Repository:** [AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot)
- **Stars:** 31k+
- **License:** MIT

