---
title: "n8n"
description: "Fair-code workflow automation platform — connect apps, APIs, and services with drag-and-drop logic, 400+ integrations, and customizable AI agents"
---

# n8n

Fair-code workflow automation platform — connect apps, APIs, and services with drag-and-drop logic, 400+ integrations, and customizable AI agents

## Tags

<a href="/categories/automation" class="tag-badge">automation</a> <a href="/categories/workflow" class="tag-badge">workflow</a> <a href="/categories/low-code" class="tag-badge">low-code</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/n8n/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/n8n/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/n8n/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `n8n` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `446cff5fe8a1893af3de4ce73259c30ecbc4d3558326410560ca64f884d42ce0` |

## Project Overview

[n8n](https://github.com/n8n-io/n8n) is a self-hostable workflow automation tool that lets you build complex integrations between apps, APIs, and services using a visual node-based editor. It ships with 400+ pre-built integrations (Slack, GitHub, Google Sheets, Postgres, OpenAI, and many more) and supports custom code nodes when you need to go beyond the built-in options.

**Who it's for:**

- Developers and teams who want to automate repetitive tasks without writing glue code
- Organizations that need self-hosted automation for data residency or compliance reasons
- Anyone building AI agent workflows — n8n has first-class support for LLM chains, tool calling, and memory

**Key capabilities:**

- Visual drag-and-drop workflow editor with 400+ integrations
- Webhook triggers for real-time event-driven automation
- Cron-based scheduling for periodic tasks
- AI agent nodes for LLM-powered workflows with tool use
- Custom JavaScript/Python code nodes for edge cases
- Execution history with full debugging and retry

## Architecture

### Services

| Service | Image | Purpose |
|---------|-------|---------|
| `n8n` | `n8nio/n8n:latest` | Workflow automation engine — web UI, API, webhook listener, and execution runtime |

### Volumes

| Volume | Mount | Purpose |
|--------|-------|---------|
| `n8n_data` | `/home/node/.n8n` | Persists workflows, credentials, execution history, and configuration across container restarts |

### Health Check

The container runs a health check against `/healthz` every 30 seconds (3 retries, 30s start period). Docker will report the container as unhealthy if the endpoint fails consistently.

### Networks

Uses the default Docker bridge network. If you need to connect n8n to other services (databases, Redis, internal APIs), attach it to a shared Docker network.

## Quick Start

### 1. Generate an encryption key

```bash
openssl rand -hex 32
```

This key encrypts all credentials stored inside n8n. **You must set it before the first run and never change it afterward** — changing it makes all saved credentials permanently unrecoverable.

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and paste your generated encryption key:

```
N8N_ENCRYPTION_KEY=<your-generated-key>
```

### 3. Start the service

```bash
docker compose up -d
```

### 4. Access n8n

Open [http://localhost:5678](http://localhost:5678) in your browser. On first visit you'll be prompted to create an owner account.

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `N8N_ENCRYPTION_KEY` | **Yes** | — | Hex string used to encrypt stored credentials. Generate with `openssl rand -hex 32`. **Never change after first run.** |
| `N8N_PORT` | No | `5678` | Port the web UI and API are exposed on from the host |
| `N8N_PROTOCOL` | No | `http` | Protocol for webhook URLs. Set to `https` if behind a reverse proxy with TLS. |
| `N8N_HOST` | No | `localhost` | Public hostname or IP where n8n is reachable. Critical for incoming webhooks — external services need a routable URL. |
| `N8N_WEBHOOK_URL` | No | — | Full webhook URL override (e.g. `https://n8n.example.com/`). Takes precedence over `N8N_PROTOCOL` + `N8N_HOST` when set. |
| `N8N_BASIC_AUTH_ACTIVE` | No | `false` | Set to `true` to enable basic auth on the n8n editor |
| `N8N_BASIC_AUTH_USER` | No | — | Username for basic auth (only used when `N8N_BASIC_AUTH_ACTIVE=true`) |
| `N8N_BASIC_AUTH_PASSWORD` | No | — | Password for basic auth (only used when `N8N_BASIC_AUTH_ACTIVE=true`) |

### External PostgreSQL Database (Optional)

By default, n8n uses an internal SQLite database stored in the `n8n_data` volume. For production workloads or higher reliability, you can switch to PostgreSQL by uncommenting these variables in `docker-compose.yml`:

```
DB_TYPE=postgresdb
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_HOST=postgres
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_USER=n8n
DB_POSTGRESDB_PASSWORD=your-password
```

When using an external database, make sure the database exists and the user has full access before starting n8n.

## Troubleshooting

### n8n starts but webhooks don't trigger

**Cause:** External services can't reach n8n because `N8N_HOST` is set to `localhost`.

**Fix:** Set `N8N_HOST` to the public IP or domain name where n8n is reachable. If behind a reverse proxy, also set `N8N_PROTOCOL=https` and optionally `N8N_WEBHOOK_URL` to the full public URL.

### Credentials lost after container restart

**Cause:** The `n8n_data` volume wasn't persisted or was accidentally removed.

**Fix:** Ensure the `n8n_data` named volume exists (`docker volume ls | grep n8n_data`). Don't run `docker compose down -v` unless you intend to wipe all data.

### "Encryption key" error on startup

**Cause:** `N8N_ENCRYPTION_KEY` is missing or empty.

**Fix:** Set a valid 64-character hex string in `.env`. Generate one with `openssl rand -hex 32`.

### Credentials become unreadable after changing the encryption key

**Cause:** `N8N_ENCRYPTION_KEY` was changed after credentials were saved. This is **not recoverable**.

**Fix:** There is no fix — you must re-create all credentials in n8n. This is why you should set the key once and never change it.

### Health check shows unhealthy

**Cause:** n8n is slow to start (especially on first run or low-resource hosts).

**Fix:** The health check has a 30-second start period. If n8n needs more time, increase `start_period` in `docker-compose.yml`. Check logs with `docker logs n8n` for startup errors.

### Port already in use

**Cause:** Another service is bound to port 5678.

**Fix:** Change `N8N_PORT` in `.env` to an available port (e.g. `5679`), then `docker compose up -d`.

## Backup & Recovery

### Backup

n8n stores all data (workflows, credentials, execution history) in the `n8n_data` volume at `/home/node/.n8n`.

**Stop n8n first** to ensure data consistency, then back up the volume:

```bash
docker compose down

# Option A: Copy the volume contents
docker run --rm -v n8n_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/n8n-backup-$(date +%Y%m%d).tar.gz -C /data .

docker compose up -d
```

**For zero-downtime backups**, use `docker volume` with a snapshot-capable storage driver, or back up the external PostgreSQL database if you've configured one.

### Recovery

```bash
docker compose down

# Restore from backup
docker run --rm -v n8n_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/n8n-backup-YYYYMMDD.tar.gz -C /data

docker compose up -d
```

**Important:** The backup and restore must use the same `N8N_ENCRYPTION_KEY`. If you lose the key, the restored credentials will be unreadable.

### Automated Backups

For scheduled backups, add a cron job:

```bash
# Back up n8n data every night at 2 AM
0 2 * * * docker stop n8n && docker run --rm -v n8n_data:/data -v /backups:/backup alpine tar czf /backup/n8n-$(date +\%Y\%m\%d).tar.gz -C /data . && docker start n8n
```

## Links

- **Original Project:** [https://github.com/n8n-io/n8n](https://github.com/n8n-io/n8n)
- **Documentation:** [https://docs.n8n.io](https://docs.n8n.io)
- **Community Forum:** [https://community.n8n.io](https://community.n8n.io)
- **Docker Hub:** [https://hub.docker.com/r/n8nio/n8n](https://hub.docker.com/r/n8nio/n8n)
- **Integration List:** [https://n8n.io/integrations](https://n8n.io/integrations)

