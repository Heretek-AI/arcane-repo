---
title: "Rabbitmq"
description: "Self-hosted Rabbitmq deployment via Docker"
---

# Rabbitmq

Self-hosted Rabbitmq deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rabbitmq/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rabbitmq/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rabbitmq/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `rabbitmq` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `5bb0a5ba2a80b1e26b58d8120b0a1bd489bfa3fb3ca3d88e28b96f2b2fb9eeeb` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `rabbitmq` | docker.io/bitnamicharts/rabbitmq:latest | Main application service |
| `rabbitmq_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Quick Start

1. **Clone and configure:**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Verify it's running:**

   ```bash
   docker compose ps
   curl -s http://localhost:8080/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `RABBITMQ_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs rabbitmq
```

**Port conflict:**
Edit `.env` and change `RABBITMQ_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec rabbitmq ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect rabbitmq --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v rabbitmq_data:/data -v $(pwd):/backup alpine tar czf /backup/rabbitmq-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v rabbitmq_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/rabbitmq-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/bitnamicharts/rabbitmq:latest`

