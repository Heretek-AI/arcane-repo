---
title: "Pairdrop"
description: "Self-hosted Pairdrop deployment via Docker"
---

# Pairdrop

Self-hosted Pairdrop deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pairdrop/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pairdrop/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pairdrop/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pairdrop` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1a13daf15ead3f08b4998cf6cccc2039d8b2c7c021048224ad62c7940cdf5c78` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `pairdrop` | ghcr.io/linuxserver/pairdrop:latest | Main application service |
| `pairdrop_data` | (volume) | Persistent data storage |

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
| `PAIRDROP_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs pairdrop
```

**Port conflict:**
Edit `.env` and change `PAIRDROP_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pairdrop ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pairdrop --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pairdrop_data:/data -v $(pwd):/backup alpine tar czf /backup/pairdrop-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pairdrop_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pairdrop-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Pairdrop](https://github.com/linuxserver/pairdrop)
- **Docker Image:** `ghcr.io/linuxserver/pairdrop:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/pairdrop/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/pairdrop/issues)

