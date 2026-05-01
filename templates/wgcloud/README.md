# WGCloud

🔗 **Upstream:** [tianshiyeben/wgcloud](https://github.com/tianshiyeben/wgcloud) (5.1k ★)

## Overview

WGCloud is a distributed monitoring system built on Spring Boot. It monitors CPU, memory, disk I/O, GPU, Docker containers, network traffic, service APIs, and more. Includes web SSH (bastion), topology visualization, and alert notification (email, DingTalk, WeChat, SMS).

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

## Architecture

- **MySQL 5.7** — relational database for metrics, configuration, and user data
- **WGCloud Server** — Spring Boot JAR (custom-built from upstream `tianshiyeben/wgcloud` source via `scripts/dockerfiles/wgcloud/Dockerfile`)

A FastAPI wrapper (`scripts/dockerfiles/wgcloud/server.py`) starts the JAR as a subprocess and exposes `/health` and `/info` endpoints.

> **Note:** The WGCloud agent component runs on monitored hosts, not in this container. See the [upstream documentation](https://github.com/tianshiyeben/wgcloud) for agent configuration.

## CI Build

Built daily via `.github/workflows/build-wgcloud.yml` and pushed to `ghcr.io/heretek-ai/arcane-repo/wgcloud:latest`.
