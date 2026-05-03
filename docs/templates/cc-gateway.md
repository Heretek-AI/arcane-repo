---
title: "CC Gateway"
description: "Privacy-preserving AI API reverse proxy with identity forwarding — route LLM requests through an identity-aware gateway"
---

# CC Gateway

Privacy-preserving AI API reverse proxy with identity forwarding — route LLM requests through an identity-aware gateway

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/proxy" class="tag-badge">proxy</a> <a href="/categories/gateway" class="tag-badge">gateway</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cc-gateway/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cc-gateway/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cc-gateway/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cc-gateway` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `899464a4cd469d3e20ffb117f10bebe69fe73fe5f4b834995f388721336a213d` |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/cc-gateway/Dockerfile`) with a multi-stage Node.js Alpine build. The upstream TypeScript project is cloned and compiled at build time. A FastAPI Python wrapper provides the health endpoint alongside the Node.js reverse proxy server.

Image is built and pushed to GHCR via CI (`.github/workflows/build-cc-gateway.yml`).

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

## API Endpoints

| Endpoint  | Method | Description                   |
|-----------|--------|-------------------------------|
| `/health` | GET    | Health and upstream status    |
| `/info`   | GET    | Gateway metadata and upstream |

## Upstream

- **Repository:** [motiful/cc-gateway](https://github.com/motiful/cc-gateway)
- **Stars:** 2.7k+
- **Runtime:** TypeScript / Node.js

