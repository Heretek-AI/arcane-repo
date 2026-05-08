# Weaviate

AI-native vector database

## Project Overview

[Weaviate](https://github.com/weaviate/weaviate) is a self-hosted deployment packaged as a Docker Compose template. This template provides everything needed to run Weaviate in a containerized environment with persistent storage, health checks, and environment-based configuration.

## Architecture

### Services

| Service | Image | Purpose |
|---------|-------|---------|
| `weaviate` | `semitechnologies/weaviate:latest` | Main application service |

### Volumes

| Volume | Mount | Purpose |
|--------|-------|---------|
| `weaviate_data` | (varies) | Persistent data storage |

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
curl -s http://localhost:8080/ | head -c 200
```

### 4. Access the application

Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration Reference

### Environment Variables

Set these in your `.env` file (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `WEAVIATE_PORT` | `8080` | Host port to expose the Weaviate API on (default: 8080) |
| `AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED` | `true` | Set to false and configure an API key or OIDC for production |
| `CLUSTER_HOSTNAME` | `weaviate-node-0` | Cluster hostname for multi-node setups (default: weaviate-node-0) |
| `DEFAULT_VECTORIZER_MODULE` | `none` | Options: text2vec-cohere, text2vec-huggingface, text2vec-openai, text2vec-ollama, none |
| `ENABLE_MODULES` | `text2vec-cohere,text2vec-huggingface,text2vec-openai,text2vec-ollama,generative-openai,generative-cohere,generative-ollama,qna-openai` | Comma-separated list of vectorizer and generative modules to enable. |


## Troubleshooting

### Container won't start

Check the logs for error messages:

```bash
docker compose logs
```

### Port conflict

If the default port 8080 is already in use, change it in `.env` and restart:

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
docker compose exec weaviate ls -la /data 2>/dev/null || echo "Volume directory not accessible"
```

## Backup & Recovery

### Backup

Stop the service to ensure data consistency, then back up the data volume:

```bash
docker compose down
docker run --rm -v weaviate_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/weaviate-backup-$(date +%Y%m%d).tar.gz -C /data .
docker compose up -d
```

### Recovery

```bash
docker compose down
docker run --rm -v weaviate_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/weaviate-backup-YYYYMMDD.tar.gz -C /data
docker compose up -d
```

## Project Homepage

- **Project site:** [Weaviate](https://github.com/weaviate/weaviate)
- **Docker Image:** `semitechnologies/weaviate:latest`
- **Issues:** [GitHub Issues](https://github.com/weaviate/weaviate/issues)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
