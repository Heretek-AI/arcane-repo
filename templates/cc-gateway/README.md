# CC Gateway — AI API Identity Gateway

[CC Gateway](https://github.com/motiful/cc-gateway) (2.7k+ ★) is a privacy-preserving reverse proxy for AI APIs with identity forwarding. Route LLM requests through a gateway that preserves user identity context while anonymizing traffic patterns.

## Quick Start

1. **Start the gateway:**

   ```bash
   docker compose up -d
   ```

2. **Check health:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **View gateway info:**

   ```bash
   curl http://localhost:8000/info
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable           | Default | Description                     |
|--------------------|---------|---------------------------------|
| `CC_GATEWAY_PORT`  | `8000`  | Host port for the gateway proxy |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/cc-gateway/Dockerfile`) with a multi-stage Node.js Alpine build. The upstream TypeScript project is cloned and compiled at build time. A FastAPI Python wrapper provides the health endpoint alongside the Node.js reverse proxy server.

Image is built and pushed to GHCR via CI (`.github/workflows/build-cc-gateway.yml`).

## API Endpoints

| Endpoint  | Method | Description                   |
|-----------|--------|-------------------------------|
| `/health` | GET    | Health and upstream status    |
| `/info`   | GET    | Gateway metadata and upstream |

## Upstream

- **Repository:** [motiful/cc-gateway](https://github.com/motiful/cc-gateway)
- **Stars:** 2.7k+
- **Runtime:** TypeScript / Node.js
