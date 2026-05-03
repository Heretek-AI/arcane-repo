---
title: "Lychee"
description: "Self-hosted Lychee deployment via Docker"
---

# Lychee

Self-hosted Lychee deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lychee/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lychee/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lychee/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `lychee` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `cd1c24810970ceb2307b9a9d92c8e5a6a735101ee06c8df605d74eb6983cd35d` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `lychee` | ghcr.io/linuxserver/lychee:latest | Main application service |
| `lychee_data` | (volume) | Persistent data storage |

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
| `LYCHEE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs lychee
```

**Port conflict:**
Edit `.env` and change `LYCHEE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec lychee ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect lychee --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v lychee_data:/data -v $(pwd):/backup alpine tar czf /backup/lychee-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v lychee_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/lychee-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Lychee](https://github.com/linuxserver/lychee)
- **Docker Image:** `ghcr.io/linuxserver/lychee:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/lychee/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/lychee/issues)

