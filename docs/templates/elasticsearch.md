---
title: "Elasticsearch"
description: "Self-hosted Elasticsearch deployment via Docker"
---

# Elasticsearch

Self-hosted Elasticsearch deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/elasticsearch/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/elasticsearch/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/elasticsearch/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `elasticsearch` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `959e9b15df34bf18e9f7e10e16b20d2226a8f2b44ba6b7043f6a95b321370115` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `elasticsearch` | docker.io/bitnamicharts/elasticsearch:latest | Main application service |
| `elasticsearch_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:9200/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:9200](http://localhost:9200) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `ELASTICSEARCH_PORT` | `9200` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs elasticsearch
```

**Port conflict:**
Edit `.env` and change `ELASTICSEARCH_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec elasticsearch ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect elasticsearch --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v elasticsearch_data:/data -v $(pwd):/backup alpine tar czf /backup/elasticsearch-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v elasticsearch_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/elasticsearch-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/bitnamicharts/elasticsearch:latest`

