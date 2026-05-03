---
title: "OpenClaw"
description: "Community and event platform API server — a modern Node.js backend with PostgreSQL, ready for extension"
---

# OpenClaw

Community and event platform API server — a modern Node.js backend with PostgreSQL, ready for extension

## Tags

<a href="/categories/api" class="tag-badge">api</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openclaw/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openclaw/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openclaw/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `openclaw` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f617fc245c05435804ffd316c63868862a4fc80c39a4c77e521122f080a96542` |

## Quick Start

1. **Set required configuration:**

   ```bash
   cp .env.example .env
   # Edit .env — set POSTGRES_PASSWORD and JWT_SECRET
   ```

2. **Start the infrastructure:**

   ```bash
   docker compose up -d
   ```

3. **Verify PostgreSQL is reachable:**

   ```bash
   docker compose exec postgres pg_isready -U openclaw -d openclaw
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### Mandatory Variables

| Variable            | Description                                                                    |
|---------------------|--------------------------------------------------------------------------------|
| `POSTGRES_PASSWORD` | PostgreSQL superuser password. Set to a strong, unique value.                  |
| `JWT_SECRET`        | Secret key for signing JWT authentication tokens. Generate with `openssl rand -hex 32`. |

### Optional Variables

| Variable        | Default      | Description                                         |
|-----------------|--------------|-----------------------------------------------------|
| `API_PORT`      | `3000`       | Host port for the API server                        |
| `POSTGRES_DB`   | `openclaw`   | PostgreSQL database name                            |
| `POSTGRES_USER` | `openclaw`   | PostgreSQL user name                                |
| `POSTGRES_PORT` | `5432`       | Host port for PostgreSQL                            |
| `NODE_ENV`      | `development`| Node.js environment mode (`development`, `production`, `test`) |

## Troubleshooting

| Symptom                                   | Likely Cause                                  | Fix                                                           |
|-------------------------------------------|-----------------------------------------------|---------------------------------------------------------------|
| `POSTGRES_PASSWORD is required` error     | `POSTGRES_PASSWORD` not set in `.env`         | Add `POSTGRES_PASSWORD` to `.env` and restart                 |
| `JWT_SECRET is required` error            | `JWT_SECRET` not set in `.env`                | Add `JWT_SECRET` to `.env` and restart                        |
| API container exits immediately            | No application code configured                | Replace the `command` in `docker-compose.yml` with your app   |
| `pg_isready` connection failure           | PostgreSQL still starting or wrong password   | Check `docker compose logs postgres` for errors              |
| API cannot connect to PostgreSQL           | Wrong credentials or hostname                 | Verify `DATABASE_URL` matches `.env` values                   |
| Port 3000 already in use                  | Another service on port 3000                  | Change `API_PORT` in `.env` to an available port              |

## API Endpoints

Once your application is deployed, typical endpoints for a community/event platform might include:

| Method | Endpoint                  | Description                      |
|--------|---------------------------|----------------------------------|
| GET    | `/health`                 | Health check                     |
| GET    | `/api/events`             | List events                      |
| POST   | `/api/events`             | Create an event                  |
| GET    | `/api/events/:id`         | Get event details                |
| PUT    | `/api/events/:id`         | Update an event                  |
| DELETE | `/api/events/:id`         | Delete an event                  |
| POST   | `/api/auth/register`      | Register a new user              |
| POST   | `/api/auth/login`         | Login (returns JWT token)        |
| GET    | `/api/users/:id`          | Get user profile                 |
| GET    | `/api/events/:id/rsvp`    | RSVP to an event                 |

The above are examples — your actual API surface depends on the application code you bring.

## Health Check

```bash
# PostgreSQL
docker compose exec postgres pg_isready -U openclaw -d openclaw

# API (once your application is running)
curl http://localhost:3000/health
```

