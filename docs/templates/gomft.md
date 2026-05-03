---
title: "Gomft"
description: "Self-hosted Gomft deployment via Docker"
---

# Gomft

Self-hosted Gomft deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gomft/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gomft/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gomft/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `gomft` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `822c65feedba6c648718a10437c43e4124531b09e73f4d141afc383d0b9027ea` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `gomft` | ghcr.io/starfleetcptn/gomft:latest | Main application service |
| `gomft_data` | (volume) | Persistent data storage |

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
| `GOMFT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs gomft
```

**Port conflict:**
Edit `.env` and change `GOMFT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gomft ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gomft --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gomft_data:/data -v $(pwd):/backup alpine tar czf /backup/gomft-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gomft_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gomft-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Gomft](https://github.com/starfleetcptn/gomft)
- **Docker Image:** `ghcr.io/starfleetcptn/gomft:latest`
- **Documentation:** [GitHub Wiki](https://github.com/starfleetcptn/gomft/wiki)
- **Issues:** [GitHub Issues](https://github.com/starfleetcptn/gomft/issues)

