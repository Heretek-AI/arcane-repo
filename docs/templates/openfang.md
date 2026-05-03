---
title: "OpenFang"
description: "Open-source Agent Operating System — Federated Learning Attack Platform with multi-agent orchestration, tool integration, and development/debugging workflows"
---

# OpenFang

Open-source Agent Operating System — Federated Learning Attack Platform with multi-agent orchestration, tool integration, and development/debugging workflows

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/security" class="tag-badge">security</a> <a href="/categories/orchestration" class="tag-badge">orchestration</a> <a href="/categories/tools" class="tag-badge">tools</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openfang/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openfang/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openfang/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `openfang` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3fd305d8f0854e99014f44fc1ffe1edb1ac68928a941defff6d7484ad282e182` |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/openfang/Dockerfile`) that compiles the upstream Rust binary from source (multi-stage build) and wraps it with a FastAPI health-check server. The compiled binary handles all agent logic; the FastAPI wrapper provides observability and health monitoring.

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

## API Endpoints

| Endpoint  | Method | Description                  |
|-----------|--------|------------------------------|
| `/health` | GET    | Health check (binary status) |
| `/info`   | GET    | Upstream and service details |

## Upstream

- **Repository:** [RightNow-AI/openfang](https://github.com/RightNow-AI/openfang)
- **Stars:** 1k+
- **License:** Apache 2.0

