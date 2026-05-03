---
title: "Netbird"
description: "Self-hosted Netbird deployment via Docker"
---

# Netbird

Self-hosted Netbird deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netbird/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netbird/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netbird/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `netbird` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3751bd2aebad7ba9462e1fec43fc712fa77984e1dfba24ad60aab15fd07181a4` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `netbird` | ghcr.io/netbirdio/netbird:latest | Main application service |
| `netbird_data` | (volume) | Persistent data storage |

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
| `NETBIRD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs netbird
```

**Port conflict:**
Edit `.env` and change `NETBIRD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec netbird ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect netbird --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v netbird_data:/data -v $(pwd):/backup alpine tar czf /backup/netbird-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v netbird_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/netbird-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Netbird](https://github.com/netbirdio/netbird)
- **Docker Image:** `ghcr.io/netbirdio/netbird:latest`
- **Documentation:** [GitHub Wiki](https://github.com/netbirdio/netbird/wiki)
- **Issues:** [GitHub Issues](https://github.com/netbirdio/netbird/issues)

