---
title: "Grafana"
description: "Self-hosted Grafana deployment via Docker"
---

# Grafana

Self-hosted Grafana deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grafana/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grafana/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grafana/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `grafana` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `cf4653fde527efb0b41bab47c757f1ee107d90e7d8a0476d35a99161d8380586` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `grafana` | docker.io/grafana/grafana:latest | Main application service |
| `grafana_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:3000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `GRAFANA_PORT` | `3000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs grafana
```

**Port conflict:**
Edit `.env` and change `GRAFANA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec grafana ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect grafana --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v grafana_data:/data -v $(pwd):/backup alpine tar czf /backup/grafana-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v grafana_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/grafana-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/grafana/grafana:latest`

