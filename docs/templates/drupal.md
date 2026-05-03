---
title: "Drupal"
description: "Self-hosted Drupal deployment via Docker"
---

# Drupal

Self-hosted Drupal deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/drupal/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/drupal/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/drupal/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `drupal` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `61fdfdef216fbe2b946ed56c2f78d3958a60aa169fed3deee4d30272c79cedea` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `drupal` | docker.io/bitnami/drupal:latest | Main application service |
| `drupal_data` | (volume) | Persistent data storage |

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
| `DRUPAL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs drupal
```

**Port conflict:**
Edit `.env` and change `DRUPAL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec drupal ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect drupal --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v drupal_data:/data -v $(pwd):/backup alpine tar czf /backup/drupal-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v drupal_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/drupal-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/bitnami/drupal:latest`

