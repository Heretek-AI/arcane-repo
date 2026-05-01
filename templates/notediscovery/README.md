# Notediscovery — Upstream Project Removed

> **Non-serviceable:** The notediscovery upstream repository (`noteed/notediscovery`) has been removed from GitHub and is no longer available. This template serves as a historical reference placeholder.

## What This Template Does

This template deploys a minimal FastAPI informational server on `python:3.12-slim` that documents the project's removal and suggests alternatives. It exposes `/health` for registry validation and `/guide` for alternative recommendations.

## Quick Start

```bash
cp .env.example .env
docker compose up -d
curl http://localhost:8000/health
```

## Why This Is Non-Serviceable

The upstream project no longer exists. No container image, source code, or documentation is available. The GitHub organization (`noteed`) and repository (`notediscovery`) both return 404 errors.

## Alternatives

If you're looking for self-hosted bookmark or note organization tools, consider:

| Tool | Description | Link |
|------|-------------|------|
| **Linkwarden** | Collaborative bookmark manager with archiving | [linkwarden.app](https://linkwarden.app) |
| **Hoarder** | Bookmark-everything app with AI auto-tagging | [hoarder.app](https://hoarder.app) |
| **Shiori** | Simple self-hosted bookmarks manager | [github.com/go-shiori/shiori](https://github.com/go-shiori/shiori) |
| **Linkding** | Self-hosted bookmark manager with archive support | [github.com/sissbruecker/linkding](https://github.com/sissbruecker/linkding) |

## Health Check

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok","note":"placeholder — upstream repository removed"}`
