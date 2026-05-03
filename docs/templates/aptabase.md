---
title: "Aptabase"
description: "Self-hosted, privacy-friendly analytics platform for mobile and desktop applications with a simple SDK integration."
---

# Aptabase

Self-hosted, privacy-friendly analytics platform for mobile and desktop applications with a simple SDK integration.

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/aptabase/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/aptabase/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/aptabase/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `aptabase` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b5e4c869e3b2db14a31c0e8fffb052b42ed10dae790b21711acef015afac28f0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `aptabase` | ghcr.io/aptabase/aptabase:latest | Main application service |
| `aptabase_data` | (volume) | Persistent data storage |

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
| `APTABASE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs aptabase
```

**Port conflict:**
Edit `.env` and change `APTABASE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec aptabase ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect aptabase --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v aptabase_data:/data -v $(pwd):/backup alpine tar czf /backup/aptabase-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v aptabase_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/aptabase-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Aptabase](https://github.com/aptabase/aptabase)
- **Docker Image:** `ghcr.io/aptabase/aptabase:latest`
- **Documentation:** [GitHub Wiki](https://github.com/aptabase/aptabase/wiki)
- **Issues:** [GitHub Issues](https://github.com/aptabase/aptabase/issues)

