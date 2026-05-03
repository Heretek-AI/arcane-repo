---
title: "OM1"
description: "Modular AI Runtime for Robots — multi-modal AI agent with vision, audio, speech processing, and hardware integration (headless container mode with hardware passthrough support)"
---

# OM1

Modular AI Runtime for Robots — multi-modal AI agent with vision, audio, speech processing, and hardware integration (headless container mode with hardware passthrough support)

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/om1/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/om1/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/om1/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `om1` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `5c8db68930b5d9be715525bbf58ceec34d84b761adaf66b00bc3cf2a12a4c35a` |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/om1/Dockerfile`) that builds OM1's upstream source with cyclonedds, ffmpeg, PulseAudio, and ALSA system dependencies. The image is published to GHCR via CI (`.github/workflows/build-om1.yml`). A FastAPI wrapper provides health-check and info endpoints.

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

4. **View service details:**

   ```bash
   curl http://localhost:8000/info
   ```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OM1_PORT` | `8000` | Host port for the FastAPI wrapper |
| `OM1_HEADLESS` | `true` | Run in headless mode (no hardware) |
| `OM1_SKIP_INTERNET_CHECK` | `true` | Skip startup internet check |

## API Endpoints

| Endpoint  | Method | Description                  |
|-----------|--------|------------------------------|
| `/health` | GET    | Health check + mode status   |
| `/info`   | GET    | Upstream details + hardware requirements |

## Upstream

- **Repository:** [OpenMind/OM1](https://github.com/OpenMind/OM1)
- **Stars:** 1.5k+
- **License:** MIT

