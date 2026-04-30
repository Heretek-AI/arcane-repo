# AstrBot — AI Agent Assistant

[AstrBot](https://github.com/AstrBotDevs/AstrBot) (31k+ ★) is an all-in-one AI agent assistant supporting multiple IM platforms (WeChat, QQ, Telegram, Discord), LLM backends, and an extensible plugin ecosystem.

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

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/astrbot/Dockerfile`) that clones the upstream AstrBot repository and wraps it with a FastAPI health/info server. The image is built and pushed to GHCR automatically via CI (`.github/workflows/build-astrbot.yml`).

## API Endpoints

| Endpoint  | Method | Description              |
|-----------|--------|--------------------------|
| `/health` | GET    | Health check             |
| `/info`   | GET    | Bot and upstream details |

## Upstream

- **Repository:** [AstrBotDevs/AstrBot](https://github.com/AstrBotDevs/AstrBot)
- **Stars:** 31k+
- **License:** MIT
