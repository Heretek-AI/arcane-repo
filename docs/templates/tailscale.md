---
title: "Tailscale"
description: "Self-hosted Tailscale deployment via Docker"
---

# Tailscale

Self-hosted Tailscale deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tailscale/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tailscale/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tailscale/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tailscale` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `41d457e78da0272419dbe59666dabeece471282825f0595ec9938bcfd0f2bcbc` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `tailscale` | ghcr.io/tailscale/tailscale:latest | Main application service |
| `tailscale_data` | (volume) | Persistent data storage |

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
| `TAILSCALE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs tailscale
```

**Port conflict:**
Edit `.env` and change `TAILSCALE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec tailscale ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect tailscale --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v tailscale_data:/data -v $(pwd):/backup alpine tar czf /backup/tailscale-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v tailscale_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/tailscale-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Tailscale](https://github.com/tailscale/tailscale)
- **Docker Image:** `ghcr.io/tailscale/tailscale:latest`
- **Documentation:** [GitHub Wiki](https://github.com/tailscale/tailscale/wiki)
- **Issues:** [GitHub Issues](https://github.com/tailscale/tailscale/issues)

