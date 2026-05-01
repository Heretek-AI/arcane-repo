# TrendRadar — News Aggregation & Sentiment Analysis

[TrendRadar](https://github.com/sansan0/TrendRadar) (55.9k+ ★) is a multi-platform news aggregation engine with AI-powered sentiment analysis and trending topic detection. It monitors news sources, social media, and content platforms to surface emerging trends with sentiment scoring.

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

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/TrendRadar/Dockerfile`) built with the uv-python pattern. Upstream includes a `docker/` directory with reference container setups. The FastAPI wrapper provides health and info endpoints alongside the upstream application.

Image is built and pushed to GHCR via CI (`.github/workflows/build-TrendRadar.yml`).

## API Endpoints

| Endpoint  | Method | Description              |
|-----------|--------|--------------------------|
| `/health` | GET    | Health check             |
| `/info`   | GET    | Engine and upstream info |

## Upstream

- **Repository:** [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)
- **Stars:** 55.9k+ (highest-starred custom build in Arcane)
- **Backend:** Python
