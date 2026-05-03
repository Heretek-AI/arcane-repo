---
title: "Prometheus"
description: "Self-hosted Prometheus deployment via Docker"
---

# Prometheus

Self-hosted Prometheus deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/prometheus/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/prometheus/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/prometheus/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `prometheus` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `393bf870e92ba12c6a734fada77d330e3a33d012c9d98c0a84096c1415f72ec6` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `prometheus` | docker.io/prom/prometheus:latest | Main application service |
| `prometheus_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:9090/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:9090](http://localhost:9090) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PROMETHEUS_PORT` | `9090` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs prometheus
```

**Port conflict:**
Edit `.env` and change `PROMETHEUS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec prometheus ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect prometheus --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v prometheus_data:/data -v $(pwd):/backup alpine tar czf /backup/prometheus-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v prometheus_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/prometheus-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/prom/prometheus:latest`

