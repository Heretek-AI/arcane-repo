---
title: "Dailytxt"
description: "Self-hosted Dailytxt deployment via Docker"
---

# Dailytxt

Self-hosted Dailytxt deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dailytxt/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dailytxt/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dailytxt/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dailytxt` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ff26d3fae036318682da0996d69ad2073f8499456d7ea25e0acd7ebc2f59a698` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `dailytxt` | docker.io/phitux/dailytxt:latest | Main application service |
| `dailytxt_data` | (volume) | Persistent data storage |

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
| `DAILYTXT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs dailytxt
```

**Port conflict:**
Edit `.env` and change `DAILYTXT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dailytxt ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dailytxt --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dailytxt_data:/data -v $(pwd):/backup alpine tar czf /backup/dailytxt-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dailytxt_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dailytxt-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Dailytxt](https://github.com/phitux/dailytxt)
- **Docker Image:** `docker.io/phitux/dailytxt:latest`
- **Documentation:** [GitHub Wiki](https://github.com/phitux/dailytxt/wiki)
- **Issues:** [GitHub Issues](https://github.com/phitux/dailytxt/issues)

