---
title: "Tianji"
description: "All-in-one website analytics, uptime monitoring, and server status dashboard — lightweight, self-hosted, and privacy-first"
---

# Tianji

All-in-one website analytics, uptime monitoring, and server status dashboard — lightweight, self-hosted, and privacy-first

## Tags

<a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/analytics" class="tag-badge">analytics</a> <a href="/categories/observability" class="tag-badge">observability</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tianji/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tianji/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tianji/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tianji` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a1b9b07d3994d5c36587718cdff8ca8a82b1566817680d8b31a9063d0df07b5d` |

## Architecture

- **tianji-app**: Node.js application — serves the web dashboard, API, background workers for uptime checks and telemetry processing
- **tianji-db**: PostgreSQL 15.4 — stores analytics events, uptime results, user accounts, and configuration

## Quick Start

1. **Start the services:**

   ```bash
   docker compose up -d
   ```

2. **Access the dashboard** at [http://localhost:12345](http://localhost:12345)

3. **Create your admin account** on first launch, then set `TIANJI_ALLOW_REGISTER=false` in `.env` to lock it down.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                | Default    | Description                                   |
|-------------------------|------------|-----------------------------------------------|
| `TIANJI_PORT`           | `12345`    | Host port for the web dashboard               |
| `TIANJI_DB_NAME`        | `tianji`   | PostgreSQL database name                      |
| `TIANJI_DB_USER`        | `tianji`   | PostgreSQL user                               |
| `TIANJI_DB_PASSWORD`    | `changeme` | PostgreSQL password — **change for production**|
| `TIANJI_JWT_SECRET`     | (empty)    | JWT signing secret — **required**             |
| `TIANJI_ALLOW_REGISTER` | `true`     | Allow new user registration (disable after setup)|

## Health Check

```bash
curl -s http://localhost:12345/api/health
```

Full documentation: [github.com/msgbyte/tianji](https://github.com/msgbyte/tianji)

