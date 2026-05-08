# DocsGPT

AI-powered documentation assistant

## Project Overview

[DocsGPT](https://github.com/arc53/DocsGPT) is a self-hosted deployment packaged as a Docker Compose template. This template provides everything needed to run DocsGPT in a containerized environment with persistent storage, health checks, and environment-based configuration.

## Architecture

### Services

| Service | Image | Purpose |
|---------|-------|---------|
| `postgres` | `postgres:16` | Database storage |
| `docsgpt` | `arc53/docsgpt:latest` | Main application service |

### Volumes

| Volume | Mount | Purpose |
|--------|-------|---------|
| `docsgpt_postgres_data` | (varies) | Persistent data storage |

### Health Check

The container runs a health check every 10s (5 retries, 30s start period). Docker will report the container as unhealthy if the endpoint fails consistently.

### Networks

Uses the default Docker bridge network. If you need to connect to other services (databases, APIs, reverse proxy), attach it to a shared Docker network.

## Quick Start

### 1. Configure environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start the service

```bash
docker compose up -d
```

### 3. Verify it's running

```bash
docker compose ps
curl -s http://localhost:5432/ | head -c 200
```

### 4. Access the application

Open [http://localhost:5432](http://localhost:5432) in your browser.

## Configuration Reference

### Environment Variables

Set these in your `.env` file (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `change-me-to-a-random-64-char-hex-string` | Generate with: openssl rand -hex 32 |
| `DOCSGPT_DB_PASSWORD` | `change-me-to-a-strong-password` | Database password (required) |
| `DOCSGPT_PORT` | `3000` | DocsGPT application port (default: 3000) |
| `DOCSGPT_DB_PORT` | `5432` | Host port for PostgreSQL (default: 5432) |
| `DOCSGPT_DB_USER` | `docsgpt` | ── Database ─────────────────────────────────────────────────────── |
| `DOCSGPT_DB_NAME` | `docsgpt` | DOCSGPT_DB_NAME configuration value |
| `LLM_NAME` | `gpt-4o` | Primary LLM provider (e.g., gpt-4o, gpt-4-turbo) |
| `OPENAI_API_KEY` | `—` | OpenAI API key (required for OpenAI models) |
| `OLLAMA_BASE_URL` | `http://host.docker.internal:11434` | For local inference via Ollama |
| `EMBEDDINGS_NAME` | `—` | Override default embedding provider if needed |
| `EMBEDDINGS_KEY` | `—` | EMBEDDINGS_KEY configuration value |
| `APP_ENV` | `production` | ── Application ──────────────────────────────────────────────────── |


## Troubleshooting

### Container won't start

Check the logs for error messages:

```bash
docker compose logs
```

### Port conflict

If the default port 5432 is already in use, change it in `.env` and restart:

```bash
# Edit .env and change to an available port
docker compose down && docker compose up -d
```

### Health check shows unhealthy

The container may need more time to start on first run or low-resource hosts. Check the logs:

```bash
docker compose logs
```

If needed, increase `start_period` in `docker-compose.yml`.

### Permission errors

Ensure the Docker user has write access to the data volume:

```bash
docker compose exec postgres ls -la /data 2>/dev/null || echo "Volume directory not accessible"
```

## Backup & Recovery

### Backup

Stop the service to ensure data consistency, then back up the data volume:

```bash
docker compose down
docker run --rm -v docsgpt_postgres_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/docsgpt-backup-$(date +%Y%m%d).tar.gz -C /data .
docker compose up -d
```

### Recovery

```bash
docker compose down
docker run --rm -v docsgpt_postgres_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/docsgpt-backup-YYYYMMDD.tar.gz -C /data
docker compose up -d
```

## Project Homepage

- **Project site:** [DocsGPT](https://github.com/arc53/DocsGPT)
- **Docker Image:** `postgres:16`
- **Issues:** [GitHub Issues](https://github.com/arc53/DocsGPT/issues)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
