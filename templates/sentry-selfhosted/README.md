# Sentry (Self-Hosted) — Error Tracking & Observability

> **WARNING: This is a reference architecture — `docker compose up` alone will NOT work.**
> You MUST run the official `./install.sh` first for one-time setup (key generation,
> database migrations, initial user creation). This docker-compose.yml is a simplified
> core that works **after** the official install. See
> [Sentry Self-Hosted Docs](https://develop.sentry.dev/self-hosted/) for the full guide.

## Why This Template Exists

Upstream Sentry self-hosted has 20+ services orchestrated by `install.sh` — not a standalone
`docker compose up`. Following [D010](../.gsd/milestones/M004/M004-CONTEXT.md) (core +
optionals simplification), this template ships a **reference core** of 7 essential services:

| Service          | Image                              | Role                                    |
|------------------|------------------------------------|-----------------------------------------|
| `postgres`       | `postgres:16-alpine`               | Primary database (events, metadata)     |
| `redis`          | `redis:7-alpine`                   | Caching, rate limiting, task queue      |
| `kafka`          | `confluentinc/cp-kafka:7.9.0`      | Event streaming + ingestion pipeline    |
| `clickhouse`     | `clickhouse/clickhouse-server`     | Analytic queries (discover, dashboards) |
| `snuba`          | `getsentry/snuba:latest`           | ClickHouse query layer                  |
| `sentry-web`     | `getsentry/sentry:latest`          | Web UI + API                            |
| `nginx`          | `nginx:alpine`                     | Reverse proxy                           |

The remaining optional services (symbolicator, relay, memcached, pgbouncer, smtp, seaweedfs,
vroom, subscription-consumer) are documented here but excluded from the core compose.

## Full Installation (Required First)

```bash
# 1. Clone and run the official install (one-time)
git clone https://github.com/getsentry/self-hosted.git
cd self-hosted
./install.sh

# 2. install.sh generates SENTRY_SECRET_KEY, runs migrations,
#    creates an admin user, and initializes volumes.

# 3. Copy generated secrets to this template's .env
cp .env ../arcane-repo/templates/sentry-selfhosted/.env
```

**install.sh does:**
- Generates `SENTRY_SECRET_KEY` (required — cannot `docker compose up` without it)
- Runs `docker compose run --rm web upgrade` (migrations)
- Creates initial admin user interactively
- Configures `docker-compose.yml` with generated settings

## Quick Start (Post-Install)

```bash
cp .env.example .env
# Populate .env with values from install.sh output (SENTRY_SECRET_KEY, passwords)
docker compose up -d
```

Verify:

```bash
curl http://localhost:${SENTRY_WEB_PORT:-9000}/api/0/serverstatus/
# or open http://localhost:${SENTRY_NGINX_PORT:-80}/
```

## Configuration

| Variable                      | Default                        | Description                                    |
|-------------------------------|--------------------------------|------------------------------------------------|
| `SENTRY_PG_USER`              | `sentry`                       | PostgreSQL user                                |
| `SENTRY_PG_PASSWORD`          | *(required)*                   | PostgreSQL password                            |
| `SENTRY_PG_DB`                | `sentry`                       | PostgreSQL database name                       |
| `SENTRY_CH_USER`              | `sentry`                       | ClickHouse user                                |
| `SENTRY_CH_PASSWORD`          | *(required)*                   | ClickHouse password                            |
| `SENTRY_CH_DB`                | `sentry`                       | ClickHouse database                            |
| `SENTRY_SECRET_KEY`           | *(required — from install.sh)* | Django secret key for crypto operations        |
| `SENTRY_WEB_PORT`             | `9000`                         | Sentry web UI host port                        |
| `SENTRY_NGINX_PORT`           | `80`                           | Nginx reverse proxy host port                  |
| `SENTRY_KAFKA_PORT`           | `9092`                         | Kafka external listener port                   |
| `SENTRY_KAFKA_CLUSTER_ID`     | `sentry-selfhosted-cluster`    | Kafka KRaft cluster ID                         |
| `SENTRY_EVENT_RETENTION_DAYS` | `90`                           | Days to retain events before deletion          |
| `SENTRY_SINGLE_ORG`           | `true`                         | Restrict to single organization mode           |

## Optional Services (Not in Core Compose)

Sent's full 20+ service architecture includes services excluded from this reference core:

| Service              | Role                              | Why Optional                               |
|----------------------|-----------------------------------|--------------------------------------------|
| `symbolicator`       | Native crash report symbolication | Only needed for native SDK crash reports   |
| `relay`              | Event ingestion gateway           | Core web accepts events directly for dev   |
| `memcached`          | Django cache backend              | Redis already covers caching               |
| `pgbouncer`          | PostgreSQL connection pool        | Single-instance profile doesn't need it    |
| `smtp`               | Outbound mail relay               | Skip for dev; add for production           |
| `seaweedfs`          | Distributed file storage          | Attachments; skip for eval                 |
| `vroom`              | Line-level profiling              | Advanced profiling feature                 |
| `subscription-consumer` | Subscription queries          | SaaS billing; not needed self-hosted       |

Add these from the upstream `docker-compose.yml` when you need full production parity.

## Managing

**View logs:**

```bash
docker compose logs -f
# Or per-service:
docker compose logs -f sentry-web
docker compose logs -f snuba
```

**Restart after config changes:**

```bash
docker compose restart sentry-web sentry-worker sentry-cron
```

**Run migrations (rarely needed post-install):**

```bash
docker compose run --rm sentry-web upgrade
```

**Back up data volumes:**

```bash
# Stop first, then back up named volumes
docker compose down
docker run --rm -v sentry-selfhosted_sentry-pgdata:/data -v $(pwd)/backup:/backup alpine tar czf /backup/pgdata.tar.gz -C /data .
```

## Troubleshooting

| Symptom                                      | Likely Cause                          | Fix                                                              |
|----------------------------------------------|---------------------------------------|------------------------------------------------------------------|
| `SENTRY_SECRET_KEY:?}` error on start        | install.sh not run yet                | Run `./install.sh` in upstream self-hosted repo first            |
| Postgres `FATAL: password authentication failed` | Wrong password in .env            | Copy password from install.sh-generated `.env`                   |
| ClickHouse connection refused                | ClickHouse still starting up          | Wait for health check — ClickHouse init takes 15-30s             |
| Kafka `Connection refused`                   | Kafka bootstrap hasn't finished       | KRaft mode startup takes 30-45s on first run                     |
| Sentry web `OperationalError: could not connect to server` | Postgres not healthy      | Check `docker compose logs postgres`, verify credentials         |
| "The install script has already been run"    | Duplicated install attempt            | Expected — install.sh is idempotent but warns                    |
| Want all 20+ services                        | Core compose is simplified            | Use upstream `docker-compose.yml` from `getsentry/self-hosted`   |
