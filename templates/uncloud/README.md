# Uncloud

🔗 **Upstream:** [psviderski/uncloud](https://github.com/psviderski/uncloud) (5.1k ★)

## Overview

Uncloud is a lightweight container orchestration platform that deploys and manages containerised applications across a network of Docker hosts. It creates a secure WireGuard mesh between hosts, provides automatic service discovery, load balancing, ingress with HTTPS, and a Docker-like CLI — all without Kubernetes overhead.

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

## Architecture

This template wraps the custom-built `uncloud` image (built from upstream `psviderski/uncloud` source via `scripts/dockerfiles/uncloud/Dockerfile`). The image contains:

- **uncloudd** — the Go-based cluster daemon that handles orchestration
- **corrosion** — the Rust WireGuard agent for mesh networking

A FastAPI server (`scripts/dockerfiles/uncloud/server.py`) starts `uncloudd` as a subprocess and exposes `/health` and `/info` endpoints for monitoring.

> **Note:** This is a single-machine deployment. For multi-machine Uncloud clusters, follow the [upstream documentation](https://github.com/psviderski/uncloud).

## CI Build

Built daily via `.github/workflows/build-uncloud.yml` and pushed to `ghcr.io/heretek-ai/arcane-repo/uncloud:latest`.
