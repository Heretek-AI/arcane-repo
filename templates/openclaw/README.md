# OpenClaw — Community & Event Platform (Foundation Template)

[OpenClaw](https://github.com) is a foundation template for a community and event platform API server. It provides a starting point for building your own service — a modern Node.js 20 backend with PostgreSQL 16 storage, ready for extension.

This is a **minimal setup template**. Unlike the other Arcane templates which ship working applications, OpenClaw is designed as a scaffold: you bring your application code, and this template gives you the infrastructure layer to run it.

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

## Services

| Service    | Image                   | Port  | Description                                       |
|------------|-------------------------|-------|---------------------------------------------------|
| `api`      | `node:20-alpine`        | 3000  | Node.js 20 API server — bring your own app code   |
| `postgres` | `postgres:16-alpine`    | 5432  | PostgreSQL 16 — application database              |

### Dependency Chain

- `api` depends on `postgres` (must be healthy before `api` starts)
- `postgres` has no internal dependencies

## Developing Your Application

### 1. Replace the startup command

Edit the `command` block in `docker-compose.yml` to point to your application:

```yaml
# Development (with file watching)
command: npx nodemon src/server.js

# Production (after build)
command: node dist/server.js

# TypeScript
command: npx ts-node src/server.ts
```

### 2. Mount your source code

Add a bind mount for your application code:

```yaml
volumes:
  - ./data:/app/data
  - ./src:/app/src        # mount your source code
  - ./package.json:/app/package.json
```

### 3. Install dependencies

Add a build step or use a multi-stage Dockerfile. For simple setups, extend the command to install dependencies on startup:

```yaml
command: sh -c "npm install && npx nodemon src/server.js"
```

For production, build a custom Docker image with dependencies pre-installed.

### 4. Add application-level health check

Once your application is running, add a health check to the `api` service:

```yaml
healthcheck:
  test: ["CMD", "node", "-e", "http.get('http://localhost:3000/health', r => { process.exit(r.statusCode === 200 ? 0 : 1) })"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

## API Endpoints (Example)

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

## Managing the Stack

**View logs:**

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f api
docker compose logs -f postgres
```

**Restart a service:**

```bash
docker compose restart api
```

**Apply environment variable changes:**

```bash
docker compose up -d
```

## Volume Management

A named volume persists database data across container restarts:

| Volume                    | Mount point                       | Content                     |
|---------------------------|-----------------------------------|-----------------------------|
| `openclaw_postgres_data`  | `/var/lib/postgresql/data`        | Database files              |

**Backup:**

```bash
docker run --rm -v openclaw_postgres_data:/source -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz -C /source .
```

## Troubleshooting

| Symptom                                   | Likely Cause                                  | Fix                                                           |
|-------------------------------------------|-----------------------------------------------|---------------------------------------------------------------|
| `POSTGRES_PASSWORD is required` error     | `POSTGRES_PASSWORD` not set in `.env`         | Add `POSTGRES_PASSWORD` to `.env` and restart                 |
| `JWT_SECRET is required` error            | `JWT_SECRET` not set in `.env`                | Add `JWT_SECRET` to `.env` and restart                        |
| API container exits immediately            | No application code configured                | Replace the `command` in `docker-compose.yml` with your app   |
| `pg_isready` connection failure           | PostgreSQL still starting or wrong password   | Check `docker compose logs postgres` for errors              |
| API cannot connect to PostgreSQL           | Wrong credentials or hostname                 | Verify `DATABASE_URL` matches `.env` values                   |
| Port 3000 already in use                  | Another service on port 3000                  | Change `API_PORT` in `.env` to an available port              |
