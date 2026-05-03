---
title: "Uncloud"
description: "Lightweight container orchestration across Docker hosts with WireGuard mesh networking — bridge the gap between Docker and Kubernetes"
---

# Uncloud

Lightweight container orchestration across Docker hosts with WireGuard mesh networking — bridge the gap between Docker and Kubernetes

## Tags

<a href="/categories/paas" class="tag-badge">paas</a> <a href="/categories/orchestration" class="tag-badge">orchestration</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/uncloud/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/uncloud/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/uncloud/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `uncloud` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ff52b8fc47cd0fab9ce830c51372cec4f03ccd42783437bf9b5c7ae975d4c798` |

## Architecture

This template wraps the custom-built `uncloud` image (built from upstream `psviderski/uncloud` source via `scripts/dockerfiles/uncloud/Dockerfile`). The image contains:

- **uncloudd** — the Go-based cluster daemon that handles orchestration
- **corrosion** — the Rust WireGuard agent for mesh networking

A FastAPI server (`scripts/dockerfiles/uncloud/server.py`) starts `uncloudd` as a subprocess and exposes `/health` and `/info` endpoints for monitoring.

> **Note:** This is a single-machine deployment. For multi-machine Uncloud clusters, follow the [upstream documentation](https://github.com/psviderski/uncloud).

## Quick Start

```bash
docker compose up -d
```

The management API is available at `http://localhost:${UNCLOUD_PORT:-8000}`.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `UNCLOUD_PORT` | `8000` | HTTP port for the FastAPI management wrapper |

Copy `.env.example` to `.env` and customize values as needed.

