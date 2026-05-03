---
title: "Fireshare"
description: "Self-hosted Fireshare deployment via Docker"
---

# Fireshare

Self-hosted Fireshare deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fireshare/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fireshare/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fireshare/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `fireshare` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `18275a1251c04744036ca5169ae94c8a88bdcb15767cd33f584fbb2fef8b2943` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `fireshare` | docker.io/shaneisrael/fireshare:latest | Main application service |
| `fireshare_data` | (volume) | Persistent data storage |

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
| `FIRESHARE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs fireshare
```

**Port conflict:**
Edit `.env` and change `FIRESHARE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec fireshare ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect fireshare --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v fireshare_data:/data -v $(pwd):/backup alpine tar czf /backup/fireshare-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v fireshare_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/fireshare-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Fireshare](https://github.com/shaneisrael/fireshare)
- **Docker Image:** `docker.io/shaneisrael/fireshare:latest`
- **Documentation:** [GitHub Wiki](https://github.com/shaneisrael/fireshare/wiki)
- **Issues:** [GitHub Issues](https://github.com/shaneisrael/fireshare/issues)

