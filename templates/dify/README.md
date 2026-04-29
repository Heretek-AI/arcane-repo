# Dify — Open-Source LLM Application Platform

[Dify](https://dify.ai) is an open-source platform for building AI applications. Create visual workflows, RAG pipelines, AI agents, and custom chatbots with drag-and-drop logic — all backed by your choice of LLM models.

This template provides a simplified Dify stack with four services: the API server, an async worker, PostgreSQL, and Redis. The Nginx reverse proxy is omitted (Arcane handles routing) and the standalone web app is bundled into the API server.

## Quick Start

1. **Set required configuration:**

   Copy `.env.example` to `.env` and set at least the two mandatory values:

   ```bash
   cp .env.example .env
   # Edit .env — set SECRET_KEY and POSTGRES_PASSWORD
   ```

2. **Start the stack:**

   ```bash
   docker compose up -d
   ```

3. **Access Dify:**

   Open [http://localhost:5001](http://localhost:5001) in your browser and follow the first-time setup flow to create your admin account.

4. **Verify the API:**

   ```bash
   curl http://localhost:5001/health
   ```

   A successful response returns JSON indicating the API server is running.

## Configuration

Copy `.env.example` to `.env` and edit:

### Mandatory Variables

| Variable              | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `SECRET_KEY`          | Encrypts session data, tokens, and API keys. Set to a fixed value before first run — changing it invalidates all existing sessions. Generate with `openssl rand -hex 32`. |
| `POSTGRES_PASSWORD`   | PostgreSQL superuser password. Set to a strong, unique value.               |

### Optional Variables

| Variable              | Default     | Description                                        |
|-----------------------|-------------|----------------------------------------------------|
| `POSTGRES_DB`         | `dify`      | PostgreSQL database name                           |
| `POSTGRES_USER`       | `dify`      | PostgreSQL user name                               |
| `POSTGRES_PORT`       | `5432`      | Host port for PostgreSQL                           |
| `REDIS_PORT`          | `6379`      | Host port for Redis                                |
| `DIFY_PORT`           | `5001`      | Host port for the Dify API server                  |
| `DIFY_DEBUG`          | `false`     | Enable debug mode (detailed error messages)        |
| `INIT_PASSWORD`       | *(empty)*   | Initial admin password for first-time setup        |

## Services

| Service   | Image                        | Port   | Description                                      |
|-----------|------------------------------|--------|--------------------------------------------------|
| `api`     | `langgenius/dify-api`        | 5001   | Dify API server — handles all HTTP requests      |
| `worker`  | `langgenius/dify-api`        | —      | Async worker — processes background jobs         |
| `postgres`| `postgres:15-alpine`         | 5432   | PostgreSQL 15 — application database             |
| `redis`   | `redis:7-alpine`             | 6379   | Redis 7 — caching and message broker             |

### Dependency Chain

- `api` depends on `postgres` and `redis` (both must be healthy before `api` starts)
- `worker` depends on `postgres` and `redis` (both must be healthy before `worker` starts)
- `postgres` and `redis` have no internal dependencies

## Health Check

```bash
curl http://localhost:5001/health
```

A successful response returns a JSON object indicating the API server is operational. To check individual services:

```bash
# PostgreSQL
docker compose exec postgres pg_isready -U dify

# Redis
docker compose exec redis redis-cli ping
# Should return: PONG
```

## API Endpoints

Dify exposes a REST API on port 5001:

| Endpoint                      | Method | Description                           |
|-------------------------------|--------|---------------------------------------|
| `/health`                     | GET    | Health check                          |
| `/v1/chat-messages`           | POST   | Send a chat message                   |
| `/v1/completion-messages`     | POST   | Send a completion request             |
| `/v1/datasets`                | GET    | List knowledge base datasets          |
| `/v1/datasets`                | POST   | Create a knowledge base dataset       |
| `/v1/workflows`               | GET    | List workflows                        |
| `/v1/workflows`               | POST   | Create a workflow                     |
| `/console/api/workspaces/current` | GET | Get current workspace info            |
| `/console/api/account/login`  | POST   | Login (returns access token)          |

Full API reference: [docs.dify.ai/api-reference](https://docs.dify.ai/api-reference)

## Managing the Stack

**View logs:**

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f api
docker compose logs -f worker
```

**Restart a single service:**

```bash
docker compose restart api
```

**Apply environment variable changes:**

```bash
docker compose up -d
```

This recreates containers whose environment has changed without downtime on unaffected services.

## Volume Management

Two named volumes persist data across container restarts:

| Volume                | Mount point                       | Content                     |
|-----------------------|-----------------------------------|-----------------------------|
| `dify_postgres_data`  | `/var/lib/postgresql/data`        | Database files              |
| `dify_redis_data`     | `/data`                           | Redis persisted data        |

**Backup a volume:**

```bash
docker run --rm -v dify_postgres_data:/source -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz -C /source .
```

**Restore a volume:**

```bash
docker run --rm -v dify_postgres_data:/target -v $(pwd):/backup alpine tar xzf /backup/postgres-backup.tar.gz -C /target
```

## Upgrading

To upgrade Dify to the latest version:

```bash
# Pull the latest images
docker compose pull

# Recreate containers with new images
docker compose up -d

# Verify the API is healthy
curl http://localhost:5001/health
```

Check the [Dify release notes](https://github.com/langgenius/dify/releases) for any migration steps between major versions.

## Troubleshooting

| Symptom                              | Likely Cause                                  | Fix                                                       |
|--------------------------------------|-----------------------------------------------|-----------------------------------------------------------|
| `SECRET_KEY is required` error       | `SECRET_KEY` not set in `.env`                | Add `SECRET_KEY` to `.env` and restart                    |
| `POSTGRES_PASSWORD is required` error| `POSTGRES_PASSWORD` not set in `.env`         | Add `POSTGRES_PASSWORD` to `.env` and restart             |
| API refuses connection               | `postgres` or `redis` not healthy yet         | Wait 10–15 seconds, then retry — depends_on waits for health |
| Login page loops / sessions lost     | `SECRET_KEY` changed between runs             | Restore the original `SECRET_KEY` value                   |
| Worker not processing jobs           | Worker container stopped or crashed           | Run `docker compose logs worker` and check for errors     |
