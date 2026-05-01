# Music Tag Web — Non-Serviceable

> **Non-serviceable:** [Music Tag Web](https://github.com/xhongc/music-tag-web) (音乐标签Web版, 5.7k ★) has no published Docker Hub image and no `Dockerfile` in its source repository. This template serves as a reference placeholder.

## What This Template Does

This template deploys a minimal FastAPI informational server on `python:3.12-slim` that documents Music Tag Web's limitations and suggests alternatives. It exposes `/health` for registry validation and `/guide` for alternative recommendations.

## Quick Start

```bash
cp .env.example .env
docker compose up -d
curl http://localhost:8000/health
```

## About Music Tag Web

Music Tag Web is a mature, popular web-based music metadata editor built with Django (backend) and Vue (frontend). It supports editing tags for FLAC, APE, WAV, AIFF, WV, TTA, MP3, M4A, OGG, MPC, OPUS, WMA, DSF, and MP4 formats.

## Why This Is Non-Serviceable

Despite being a web application with a `local.yml` Compose file in its repository:

- The project has **no `Dockerfile`** — `local.yml` references a pre-built image tag that doesn't exist on Docker Hub
- The referenced image (`xhongc/music-tag-web`) returns **404 on Docker Hub**
- No CI pipeline publishes container images
- The project is primarily distributed as a Python/Django application run directly

**To make this template serviceable:** A contributor would need to add a proper Dockerfile to the upstream repository and publish images to Docker Hub or GHCR.

## Alternatives

If you need self-hosted music management with metadata capabilities, consider:

| Tool | Description | Link |
|------|-------------|------|
| **Beets** | CLI music library manager with web plugin, metadata fetching | [beets.io](https://beets.io) |
| **Navidrome** | Modern music server with web UI, Subsonic API, multi-user | [navidrome.org](https://www.navidrome.org) |
| **Airsonic** | Self-hosted music streamer with metadata and transcoding | [airsonic.github.io](https://airsonic.github.io) |
| **Lidarr** | Music collection manager with automated metadata and organization | [lidarr.audio](https://lidarr.audio) |

## Health Check

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok","note":"placeholder — no containerized deployment available"}`
