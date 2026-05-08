# TensorZero

AI agent evaluation and monitoring

## Project Overview

[TensorZero](https://github.com/tensorzero/tensorzero) is a self-hosted deployment packaged as a Docker Compose template. This template provides everything needed to run TensorZero in a containerized environment with persistent storage, health checks, and environment-based configuration.

## Architecture

### Services

| Service | Image | Purpose |
|---------|-------|---------|
| `tensorzero` | `tensorzero/gateway:latest` | Main application service |

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
curl -s http://localhost:3000/ | head -c 200
```

### 4. Access the application

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration Reference

### Environment Variables

Set these in your `.env` file (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `TENSORZERO_PORT` | `3000` | Host port to expose the TensorZero gateway on (default: 3000) |
| `OPENAI_API_KEY` | `—` | OpenAI |
| `ANTHROPIC_API_KEY` | `—` | Anthropic |
| `GOOGLE_API_KEY` | `—` | Google / Gemini |
| `AWS_ACCESS_KEY_ID` | `—` | AWS Bedrock |
| `AWS_SECRET_ACCESS_KEY` | `—` | AWS_SECRET_ACCESS_KEY configuration value |
| `AWS_DEFAULT_REGION` | `us-east-1` | AWS_DEFAULT_REGION configuration value |
| `OLLAMA_BASE_URL` | `http://host.docker.internal:11434` | For Ollama running on the host machine (or at a custom URL) |
| `TENSORZERO_CONFIG_FILE` | `/app/config/tensorzero.toml` | Path to the TensorZero gateway configuration file (default: /app/config/tensorzero.toml) |
| `TENSORZERO_CLICKHOUSE_URL` | `—` | If empty, TensorZero logs to stdout only. |


## Troubleshooting

### Container won't start

Check the logs for error messages:

```bash
docker compose logs
```

### Port conflict

If the default port 3000 is already in use, change it in `.env` and restart:

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
docker compose exec tensorzero ls -la /data 2>/dev/null || echo "Volume directory not accessible"
```

## Backup & Recovery

### Backup

Stop the service to ensure data consistency, then back up the data volume:

```bash
docker compose down
docker run --rm -v tensorzero_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/tensorzero-backup-$(date +%Y%m%d).tar.gz -C /data .
docker compose up -d
```

### Recovery

```bash
docker compose down
docker run --rm -v tensorzero_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/tensorzero-backup-YYYYMMDD.tar.gz -C /data
docker compose up -d
```

## Project Homepage

- **Project site:** [TensorZero](https://github.com/tensorzero/tensorzero)
- **Docker Image:** `tensorzero/gateway:latest`
- **Issues:** [GitHub Issues](https://github.com/tensorzero/tensorzero/issues)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
