---
title: "Tabby"
description: "Self-hosted Tabby deployment via Docker"
---

# Tabby

Self-hosted Tabby deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tabby/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tabby/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tabby/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tabby` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c2c5469c939557ebc65b8dc2e11594b048592c4bc5662840f16e792deb00b0c8` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `tabby` | ghcr.io/tabbyml/tabby:latest | Main application service |
| `tabby_data` | (volume) | Persistent data storage |

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
| `TABBY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs tabby
```

**Port conflict:**
Edit `.env` and change `TABBY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec tabby ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect tabby --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v tabby_data:/data -v $(pwd):/backup alpine tar czf /backup/tabby-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v tabby_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/tabby-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Tabby](https://github.com/tabbyml/tabby)
- **Docker Image:** `ghcr.io/tabbyml/tabby:latest`
- **Documentation:** [GitHub Wiki](https://github.com/tabbyml/tabby/wiki)
- **Issues:** [GitHub Issues](https://github.com/tabbyml/tabby/issues)

