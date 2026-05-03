---
title: "Coolify"
description: "Open-source Heroku / Netlify / Vercel alternative — deploy web apps, databases, and services on your own servers with automated SSL, Git integration, and one-click rollbacks"
---

# Coolify

Open-source Heroku / Netlify / Vercel alternative — deploy web apps, databases, and services on your own servers with automated SSL, Git integration, and one-click rollbacks

## Tags

<a href="/categories/paas" class="tag-badge">paas</a> <a href="/categories/platform" class="tag-badge">platform</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/coolify/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/coolify/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/coolify/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `coolify` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6f644f82290c34418daa1eb312414106697d38b26d5c59a3773254de9030ae93` |

## Architecture

```
    ┌─────────────────────────────────────────────────┐
    │              Coolify App :8000                   │
    │         (Laravel API + Vue.js Dashboard)         │
    └────┬─────────────┬──────────────┬───────────────┘
         │             │              │
         ▼             ▼              ▼
  ┌──────────┐ ┌──────────────┐ ┌──────────────┐
  │PostgreSQL│ │    Redis     │ │    Soketi    │
  │  :5432   │ │    :6379     │ │    :6001     │
  │(app data)│ │(cache+queue) │ │ (WebSocket)  │
  └──────────┘ └──────────────┘ └──────────────┘
```

All 4 services share the `coolify-net` bridge network. The Coolify app depends on all three backend services being healthy before it starts. Images are pulled from GitHub Container Registry (`ghcr.io/coollabsio/`) — not Docker Hub, because upstream publishes exclusively to GHCR.

This is the simplified core deployment per Arcane's D010 — it ships what you need to run the platform. For production-scale deployments with separate servers, reverse proxy, and persistent worker nodes, refer to the [official production docs](https://coolify.io/docs/installation).

## Quick Start

1. **Start the core services:**

   ```bash
   docker compose up -d
   ```

2. **Access the dashboard** at [http://localhost:8000](http://localhost:8000)

3. **Follow the on-screen setup wizard** to create your admin account and configure your first server.

4. **Enable Docker container management** — uncomment the `docker.sock` mount in `docker-compose.yml` and restart:

   ```bash
   docker compose down && docker compose up -d
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable               | Default    | Description                                         |
|------------------------|------------|-----------------------------------------------------|
| `COOLIFY_PORT`         | `8000`     | Host port for the Coolify web dashboard             |
| `COOLIFY_APP_ENV`      | `local`    | Environment: `local` or `production`                |
| `COOLIFY_APP_KEY`      | (empty)    | Laravel app encryption key — **required**           |
| `COOLIFY_DB_NAME`      | `coolify`  | PostgreSQL database name                            |
| `COOLIFY_DB_USER`      | `coolify`  | PostgreSQL user                                     |
| `COOLIFY_DB_PASSWORD`  | `changeme` | PostgreSQL password — **change for production**     |
| `REDIS_PASSWORD`       | (empty)    | Redis password (optional — leave empty for no auth) |
| `SOKETI_DEFAULT_APP_ID`  | `coolify`| Soketi application ID for WebSocket auth            |
| `SOKETI_DEFAULT_APP_KEY`   | (empty) | Soketi app key — **required**                       |
| `SOKETI_DEFAULT_APP_SECRET`| (empty) | Soketi app secret — **required**                    |
| `SOKETI_METRICS_SERVER_PORT`| `9601`  | Soketi metrics/health check server port             |

### Generating Required Secrets

```bash
# Coolify app key (Laravel encryption key)
openssl rand -hex 32

# Soketi app key
openssl rand -hex 32

# Soketi app secret
openssl rand -hex 32
```

Set all of `COOLIFY_APP_KEY`, `SOKETI_DEFAULT_APP_KEY`, and `SOKETI_DEFAULT_APP_SECRET` before starting.

## Upstream

- [coollabsio/coolify](https://github.com/coollabsio/coolify) — Official repository
- [Coolify Docs](https://coolify.io/docs) — Full documentation and installation guide
- [Coolify Security](https://coolify.io/docs/security) — Security best practices

