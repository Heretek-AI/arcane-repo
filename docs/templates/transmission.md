---
title: "Transmission"
description: "Self-hosted Transmission deployment via Docker"
---

# Transmission

Self-hosted Transmission deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/transmission/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/transmission/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/transmission/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `transmission` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c9a115d4a74372c1996ba2c21e44bdcb928c574e8eb6b7d4d775d95947d0b1b4` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `transmission` | ghcr.io/linuxserver/transmission:latest | Main application service |
| `transmission_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:9091/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:9091](http://localhost:9091) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `TRANSMISSION_PORT` | `9091` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs transmission
```

**Port conflict:**
Edit `.env` and change `TRANSMISSION_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec transmission ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect transmission --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v transmission_data:/data -v $(pwd):/backup alpine tar czf /backup/transmission-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v transmission_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/transmission-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Transmission](https://github.com/linuxserver/transmission)
- **Docker Image:** `ghcr.io/linuxserver/transmission:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/transmission/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/transmission/issues)

