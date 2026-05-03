---
title: "TrendRadar"
description: "Multi-platform news aggregation and sentiment analysis engine — track trending topics across news sources with AI-powered analysis"
---

# TrendRadar

Multi-platform news aggregation and sentiment analysis engine — track trending topics across news sources with AI-powered analysis

## Tags

<a href="/categories/ai" class="tag-badge">ai</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/trendradar/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/trendradar/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/trendradar/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `trendradar` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `882949dd3d5fbcc2ac0bed4b613413cfebcca057e5ed57f99d8c9a6fd2243f6b` |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/TrendRadar/Dockerfile`) built with the uv-python pattern. Upstream includes a `docker/` directory with reference container setups. The FastAPI wrapper provides health and info endpoints alongside the upstream application.

Image is built and pushed to GHCR via CI (`.github/workflows/build-TrendRadar.yml`).

## Quick Start

1. **Start TrendRadar:**

   ```bash
   docker compose up -d
   ```

2. **Check health:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **View info:**

   ```bash
   curl http://localhost:8000/info
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable            | Default | Description                      |
|---------------------|---------|----------------------------------|
| `TRENDRADAR_PORT`   | `8000`  | Host port for the TrendRadar API |

## API Endpoints

| Endpoint  | Method | Description              |
|-----------|--------|--------------------------|
| `/health` | GET    | Health check             |
| `/info`   | GET    | Engine and upstream info |

## Upstream

- **Repository:** [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)
- **Stars:** 55.9k+ (highest-starred custom build in Arcane)
- **Backend:** Python

