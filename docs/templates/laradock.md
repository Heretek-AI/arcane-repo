---
title: "Laradock"
description: "Simplified PHP deployment environment — nginx + php-fpm + mysql + redis (not the full Laradock dev stack)"
---

# Laradock

Simplified PHP deployment environment — nginx + php-fpm + mysql + redis (not the full Laradock dev stack)

## Tags

<a href="/categories/web" class="tag-badge">web</a> <a href="/categories/multi-service" class="tag-badge">multi-service</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/laradock/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/laradock/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/laradock/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `laradock` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `dc248198ed73744f2e452e7b918d77251efa9f28b9373c7ebe3cb2d0a2e003db` |

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` to set secure database credentials:**

   ```ini
   MYSQL_ROOT_PASSWORD=your-secure-root-password
   MYSQL_PASSWORD=your-secure-user-password
   ```

3. **Place your PHP application code in a volume-mounted directory** or update `laradock_app` volume to bind-mount your project:

   ```bash
   docker compose up -d
   ```

4. **Access your app:**

   Open [http://localhost:8080](http://localhost:8080) (or your configured `NGINX_PORT`).

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `NGINX_PORT` | `8080` | Host port for nginx HTTP |
| `MYSQL_PORT` | `3306` | Host port for MySQL |
| `MYSQL_ROOT_PASSWORD` | `rootsecret` | MySQL root password |
| `MYSQL_DATABASE` | `laradock` | MySQL database name |
| `MYSQL_USER` | `laradock` | MySQL user |
| `MYSQL_PASSWORD` | `secret` | MySQL user password |
| `REDIS_PORT` | `6379` | Host port for Redis |

## Service Details

- **nginx** (alpine) — Reverse proxy serving PHP application on port `NGINX_PORT`
- **php-fpm** (8.3-fpm-alpine) — PHP runtime with PDO MySQL and Redis extensions
- **mysql** (8.0) — Primary database with persistent named volume
- **redis** (7-alpine) — Cache/session store with persistent named volume

All services include health checks and proper dependency ordering (`depends_on` with `condition: service_healthy`).

## Upstream

- [GitHub Repository](https://github.com/laradock/laradock)
- [Documentation](https://laradock.io/)

