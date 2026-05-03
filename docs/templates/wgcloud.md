---
title: "WGCloud"
description: "Java Spring Boot distributed monitoring system — CPU, memory, disk, GPU, Docker, network, service API monitoring with web SSH and topology visualization"
---

# WGCloud

Java Spring Boot distributed monitoring system — CPU, memory, disk, GPU, Docker, network, service API monitoring with web SSH and topology visualization

## Tags

<a href="/categories/monitoring" class="tag-badge">monitoring</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wgcloud/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wgcloud/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wgcloud/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `wgcloud` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `065abf5c44acf0fe6e8aff03f58274f4aead66cb715349242f9b69c0ca3039fe` |

## Architecture

- **MySQL 5.7** — relational database for metrics, configuration, and user data
- **WGCloud Server** — Spring Boot JAR (custom-built from upstream `tianshiyeben/wgcloud` source via `scripts/dockerfiles/wgcloud/Dockerfile`)

A FastAPI wrapper (`scripts/dockerfiles/wgcloud/server.py`) starts the JAR as a subprocess and exposes `/health` and `/info` endpoints.

> **Note:** The WGCloud agent component runs on monitored hosts, not in this container. See the [upstream documentation](https://github.com/tianshiyeben/wgcloud) for agent configuration.

## Quick Start

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env to set MYSQL_ROOT_PASSWORD

# Start the stack
docker compose up -d
```

The server UI is available at `http://localhost:${WGCLOUD_PORT:-9999}/wgcloud`.

> **First start:** MySQL takes ~30s to initialize. The WGCloud server will wait for MySQL to be healthy before starting. If the WGCloud application fails on first start, check that the `wgcloud` database was auto-created — the SQL schema (`wgcloud.sql`) ships inside the custom-built Docker image.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `WGCLOUD_PORT` | `9999` | Spring Boot server port |
| `MYSQL_ROOT_PASSWORD` | `changeme` | MySQL root password (set this!) |
| `MYSQL_DATABASE` | `wgcloud` | MySQL database name |
| `MYSQL_PORT` | `3306` | MySQL port exposed to host |

