# OpenFang — Federated Learning Attack Platform

[OpenFang](https://github.com/RightNow-AI/openfang) (1k+ ★) is an open-source Agent Operating System focused on federated learning security research. It orchestrates multi-agent workflows for developing, debugging, and testing AI agent-based attacks and defenses.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Check health:**

   ```bash
   curl http://localhost:8000/health
   ```

4. **Access the native interface:**

   The upstream binary listens internally on port 4200. If you need direct access, map it in docker-compose, but the FastAPI wrapper on port 8000 provides health and info endpoints.

## Configuration

| Variable        | Default | Description                          |
|-----------------|---------|--------------------------------------|
| `OPENFANG_PORT` | `8000`  | Host port for the FastAPI wrapper    |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/openfang/Dockerfile`) that compiles the upstream Rust binary from source (multi-stage build) and wraps it with a FastAPI health-check server. The compiled binary handles all agent logic; the FastAPI wrapper provides observability and health monitoring.

## API Endpoints

| Endpoint  | Method | Description                  |
|-----------|--------|------------------------------|
| `/health` | GET    | Health check (binary status) |
| `/info`   | GET    | Upstream and service details |

## Upstream

- **Repository:** [RightNow-AI/openfang](https://github.com/RightNow-AI/openfang)
- **Stars:** 1k+
- **License:** Apache 2.0
