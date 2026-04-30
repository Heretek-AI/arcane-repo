# Yuxi — Multi-Agent LLM Conversation Platform

[Yuxi](https://github.com/xerrors/Yuxi) (5k+ ★) is a multi-agent LLM conversation platform with a modular agent architecture, knowledge base integration, and tool ecosystem. It enables sophisticated multi-turn conversations orchestrated across specialized AI agents.

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

## Simplified Architecture

Upstream Yuxi defines a 4-service compose (`backend + frontend + neo4j + postgres`). This template simplifies to **backend + PostgreSQL only** — the two essential runtime services. Omitted services and their purpose:

| Omitted        | Purpose                                      | How to Replace                       |
|----------------|----------------------------------------------|--------------------------------------|
| **Frontend**   | Web UI dashboard for monitoring agents       | Access via the REST API directly      |
| **Neo4j**      | Graph database for knowledge graphs          | PostgreSQL handles structured data; graph features require upstream compose |

For the full multi-service deployment, use [upstream's docker-compose.yml](https://github.com/xerrors/Yuxi).

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/Yuxi/Dockerfile`) built with the uv-python pattern. The FastAPI server wrapper provides health and info endpoints alongside the upstream application's entrypoint. Image is built and pushed to GHCR via CI (`.github/workflows/build-Yuxi.yml`).

## API Endpoints

| Endpoint  | Method | Description                   |
|-----------|--------|-------------------------------|
| `/health` | GET    | Health check                  |
| `/info`   | GET    | Platform and upstream details |

## Upstream

- **Repository:** [xerrors/Yuxi](https://github.com/xerrors/Yuxi)
- **Stars:** 5k+
- **Backend:** Python
