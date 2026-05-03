---
title: "TradingAgents"
description: "AI-powered algorithmic trading with multi-agent collaboration"
---

# TradingAgents

AI-powered algorithmic trading with multi-agent collaboration

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tradingagents/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tradingagents/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tradingagents/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tradingagents` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `23c405ebfc67045699c3bf9562ac828361b46776dfe1c43fe4103165f8f05c65` |

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

   > **Build:** This is a custom-build template — the Docker image is built from source and hosted on GHCR (`ghcr.io/heretek-ai/arcane-repo/tradingagents:latest`). No pre-built public image exists upstream.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|----------|-------------|-----|
| `docker compose up` fails | Image not yet built/pulled | Run `docker compose build` to build locally, or wait for CI-published image |
| Port conflict | Another service on port 8000 | Change `TRADINGAGENTS_PORT` in `.env` |
| Container exits immediately | Build failure | Run `docker compose logs tradingagents` for details |

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

