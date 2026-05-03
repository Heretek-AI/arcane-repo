---
title: "Sentry (Self-Hosted)"
description: "Reference architecture for self-hosted Sentry error tracking — 7-service core compose (postgres, redis, kafka, clickhouse, snuba, web, nginx) that works after running the official install.sh for one-time setup"
---

# Sentry (Self-Hosted)

Reference architecture for self-hosted Sentry error tracking — 7-service core compose (postgres, redis, kafka, clickhouse, snuba, web, nginx) that works after running the official install.sh for one-time setup

## Tags

<a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/observability" class="tag-badge">observability</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sentry-selfhosted/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sentry-selfhosted/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sentry-selfhosted/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `sentry-selfhosted` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `26c27e592f53d66b017da7e3044e8ea5aa8243227dd1aa07ac6202ac18912ea9` |

## Quick Start

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

