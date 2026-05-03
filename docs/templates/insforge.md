---
title: "InsForge"
description: "Open-source agentic backend — postgres + postgREST for building full-stack AI applications with agent-native primitives"
---

# InsForge

Open-source agentic backend — postgres + postgREST for building full-stack AI applications with agent-native primitives

## Tags

<a href="/categories/ai" class="tag-badge">ai</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/insforge/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/insforge/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/insforge/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `insforge` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3bfb5b37401474661b5fe74ae5ff001399875d83f70b98562a7c07a93717df5f` |

## Quick Start

1. **Start the database and API:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify the database is healthy:**

   ```bash
   docker compose exec postgres pg_isready -U postgres
   ```

3. **Explore the auto-generated API:**

   ```bash
   curl http://localhost:3000/
   ```

   PostgREST serves an OpenAPI spec at `/` and exposes database tables as REST endpoints.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable            | Default                             | Description                        |
|---------------------|-------------------------------------|------------------------------------|
| `POSTGRES_PORT`     | `5432`                              | Host port for PostgreSQL           |
| `POSTGRES_USER`     | `postgres`                          | Database user                      |
| `POSTGRES_PASSWORD` | `postgres`                          | Database password                  |
| `POSTGRES_DB`       | `insforge`                          | Database name                      |
| `POSTGREST_PORT`    | `3000`                              | Host port for REST API             |
| `JWT_SECRET`        | `dev-secret-please-change-in-production` | JWT signing secret           |
| `ENCRYPTION_KEY`    | —                                   | Encryption key for secrets         |

## Troubleshooting

| Symptom                                    | Likely Cause                    | Fix                                                |
|--------------------------------------------|---------------------------------|----------------------------------------------------|
| PostgREST won't connect to postgres        | Postgres not healthy yet        | Wait 10s and retry                                 |
| `pg_isready` fails                         | Wrong credentials in `.env`     | Check `POSTGRES_USER` / `POSTGRES_PASSWORD`        |
| PostgREST returns 503                      | Schema not initialized          | Create tables in the `public` schema via psql      |
| Need the full UI dashboard                 | Using simplified template       | Clone upstream and run its full `docker-compose.yml` |

