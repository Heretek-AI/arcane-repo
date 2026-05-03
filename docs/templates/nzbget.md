---
title: "Nzbget"
description: "Self-hosted Nzbget deployment via Docker"
---

# Nzbget

Self-hosted Nzbget deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nzbget/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nzbget/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nzbget/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `nzbget` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e1aad0239ce5c34d83bff13a06ebc31767e32a132d09cdc98c95c709256eb299` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `nzbget` | ghcr.io/linuxserver/nzbget:latest | Main application service |
| `nzbget_data` | (volume) | Persistent data storage |

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
| `NZBGET_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs nzbget
```

**Port conflict:**
Edit `.env` and change `NZBGET_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec nzbget ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect nzbget --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v nzbget_data:/data -v $(pwd):/backup alpine tar czf /backup/nzbget-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v nzbget_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/nzbget-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Nzbget](https://github.com/linuxserver/nzbget)
- **Docker Image:** `ghcr.io/linuxserver/nzbget:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/nzbget/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/nzbget/issues)

