---
title: "Databasus"
description: "Web-based PostgreSQL database browser — query, visualize, and manage Postgres databases through a clean web UI"
---

# Databasus

Web-based PostgreSQL database browser — query, visualize, and manage Postgres databases through a clean web UI

## Tags

<a href="/categories/database" class="tag-badge">database</a> <a href="/categories/sql" class="tag-badge">sql</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/databasus/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/databasus/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/databasus/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `databasus` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d6a4f85ef0cf5618ac2857d39141989651bbc94760803666e0ba0e770627fb07` |

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

   Open [http://localhost:5433](http://localhost:5433).

   Connect to your PostgreSQL database by providing host, port, database name, username, and password in the UI.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `DATABASUS_PORT` | `5433` | Host port for the web UI |

## Service Details

- **Web UI** — Browser-based PostgreSQL client on port 5433
- **Connection Manager** — Save and manage multiple database connections
- **Query Editor** — SQL editor with syntax highlighting and results grid
- **Data Browser** — Browse tables, views, and schemas
- **Export** — Export query results to CSV

## Upstream

- [Docker Hub](https://hub.docker.com/r/databasus/databasus)

