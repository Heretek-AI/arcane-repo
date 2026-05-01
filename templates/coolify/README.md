# Coolify — Open-Source Heroku / Netlify / Vercel Alternative

[Coolify](https://coolify.io/) is an open-source PaaS that lets you deploy web applications, databases, and services on your own servers. It gives you automated SSL via Let's Encrypt, one-click rollbacks, Git integration (GitHub, GitLab, Bitbucket), and a beautiful dashboard — all running on your own infrastructure. No vendor lock-in, no per-app pricing.

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

## Architecture (Simplified 4-Service Core)

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

## Docker Socket Mount

Coolify manages Docker containers on your host — it needs access to the Docker socket. The mount is **commented out by default** so you can review the security implications first:

```yaml
# - /var/run/docker.sock:/var/run/docker.sock
```

**What this enables:** Coolify can deploy apps as Docker containers, create networks, manage volumes, and proxy traffic — all the core PaaS functionality.

**Security considerations:**
- Mounting `docker.sock` gives the Coolify container **full root-equivalent control** over your Docker daemon
- Anyone who compromises the Coolify dashboard can run arbitrary containers on your host
- Review [Coolify's security docs](https://coolify.io/docs/security) before enabling
- Consider using a dedicated Docker context or isolated VM for production deployments

To enable: uncomment the mount line in `docker-compose.yml`, then `docker compose up -d`.

## Features

- **One-click deploy**: Deploy static sites, Node.js, Python, PHP, Go, Rust, Docker containers, and databases
- **Automated SSL**: Let's Encrypt certificates for every deployed app — zero manual renewal
- **Git integration**: Connect GitHub, GitLab, Bitbucket — automatic deploys on push
- **Database hosting**: PostgreSQL, MySQL, MongoDB, Redis, MariaDB — with automated backups
- **Server management**: Add multiple servers, view resource usage, manage firewall rules
- **Rollbacks**: Instant rollbacks to any previous deployment with a single click
- **Team collaboration**: Invite team members with role-based access control
- **Web terminal**: Browser-based terminal for each server — debug without SSH

## Health Checks

All 4 core services have Docker health checks:

```bash
# Check service health
docker compose ps

# Coolify app health
curl http://localhost:8000/api/health

# PostgreSQL readiness
docker compose exec coolify-db pg_isready -U coolify

# Redis ping
docker compose exec coolify-redis redis-cli ping

# Soketi readiness
curl http://localhost:6001/ready
```

## Volume Management

- **coolify_data**: Coolify application data (SQLite local cache, config)
- **coolify_db_data**: PostgreSQL persistent data
- **coolify_redis_data**: Redis append-only file (AOF) data

Destroy all data (including deployed apps): `docker compose down -v`

## Dependencies

| Service      | Depends On                                                |
|--------------|-----------------------------------------------------------|
| coolify      | coolify-db (healthy), coolify-redis (healthy), coolify-soketi (healthy)|
| coolify-db   | (none)                                                    |
| coolify-redis| (none)                                                    |
| coolify-soketi| (none)                                                   |

## Upstream References

- [coollabsio/coolify](https://github.com/coollabsio/coolify) — Official repository
- [Coolify Docs](https://coolify.io/docs) — Full documentation and installation guide
- [Coolify Security](https://coolify.io/docs/security) — Security best practices
