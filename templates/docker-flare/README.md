# Docker Flare — Non-Serviceable

> **Non-serviceable:** Docker Flare has no published Docker image on Docker Hub and no `Dockerfile` in its source repository. This template serves as a reference placeholder.

## What This Template Does

This template deploys a minimal FastAPI informational server on `python:3.12-slim` that documents Docker Flare's limitations and suggests alternatives. It exposes `/health` for registry validation and `/guide` for alternative recommendations.

## Quick Start

```bash
cp .env.example .env
docker compose up -d
curl http://localhost:8000/health
```

## Why This Is Non-Serviceable

Docker Flare is a self-hosted start page / dashboard built by [soulteary](https://github.com/soulteary/docker-flare). Despite the name, the project:

- Has **no Docker Hub image** published
- Has **no Dockerfile** in its source repository
- Cannot be containerized without building a custom image from scratch

## Alternatives

If you're looking for self-hosted dashboards and start pages, consider these alternatives which have Docker images available:

| Tool | Description | Link |
|------|-------------|------|
| **Homepage** | Modern, feature-rich dashboard with service widgets and status monitoring | [gethomepage.dev](https://gethomepage.dev) |
| **Dashy** | Highly customizable dashboard with status checks and themes | [dashy.to](https://dashy.to) |
| **Homarr** | Drag-and-drop dashboard with integrations and widgets | [homarr.dev](https://homarr.dev) |
| **Flame** | Simple, fast start page with fuzzy search | [github.com/pawelmalak/flame](https://github.com/pawelmalak/flame) |

## Health Check

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok","note":"placeholder — no containerized deployment available"}`
