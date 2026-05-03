---
title: "Solr"
description: "Self-hosted Solr deployment via Docker"
---

# Solr

Self-hosted Solr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/solr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/solr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/solr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `solr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1f46f09cb33f7db20c1f7cbebb468922583b159a7635acdf63340ba8c556ca07` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `solr` | docker.io/bitnamicharts/solr:latest | Main application service |
| `solr_data` | (volume) | Persistent data storage |

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
| `SOLR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs solr
```

**Port conflict:**
Edit `.env` and change `SOLR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec solr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect solr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v solr_data:/data -v $(pwd):/backup alpine tar czf /backup/solr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v solr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/solr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Solr](https://github.com/bitnamicharts/solr)
- **Docker Image:** `docker.io/bitnamicharts/solr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/bitnamicharts/solr/wiki)
- **Issues:** [GitHub Issues](https://github.com/bitnamicharts/solr/issues)

