---
title: "OpenGist"
description: "Self-hosted pastebin and git snippet host — create, share, and manage code snippets with Git-backed versioning"
---

# OpenGist

Self-hosted pastebin and git snippet host — create, share, and manage code snippets with Git-backed versioning

## Tags

<a href="/categories/tools" class="tag-badge">tools</a> <a href="/categories/web" class="tag-badge">web</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/opengist/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/opengist/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/opengist/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `opengist` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8dde204815df9babb636ebae74a7416c1c8e207622e4a7c101545895d075dfff` |

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the web UI:**

   Open [http://localhost:6157](http://localhost:6157).

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `OPENGIST_PORT` | `6157` | Host port for the web UI |

## Service Details

- **Web UI** — Browser-based snippet manager on port 6157
- **Git-Backed** — Every gist is a full Git repository with full revision history
- **Syntax Highlighting** — Automatic syntax highlighting for 200+ languages
- **Public & Private** — Create public snippets for sharing or private snippets for personal use
- **Forking** — Fork gists to build on others' snippets
- **Storage** — All data persisted in the `opengist_data` named volume

## Upstream

- [GitHub Repository](https://github.com/thomiceli/opengist)
- [Docker Hub](https://hub.docker.com/r/thomiceli/opengist)

