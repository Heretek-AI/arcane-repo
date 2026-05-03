---
title: "Transmission Openvpn"
description: "Self-hosted Transmission Openvpn deployment via Docker"
---

# Transmission Openvpn

Self-hosted Transmission Openvpn deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/transmission-openvpn/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/transmission-openvpn/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/transmission-openvpn/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `transmission-openvpn` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `458bc3bcf50a2f4cfe76c86d0b44917ea83611f955eb53de3aa3fa7abab23bc6` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `transmission-openvpn` | docker.io/haugene/transmission-openvpn:latest | Main application service |
| `transmission-openvpn_data` | (volume) | Persistent data storage |

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
| `TRANSMISSION_OPENVPN_PORT` | `9091` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs transmission-openvpn
```

**Port conflict:**
Edit `.env` and change `TRANSMISSION-OPENVPN_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec transmission-openvpn ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect transmission-openvpn --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v transmission-openvpn_data:/data -v $(pwd):/backup alpine tar czf /backup/transmission-openvpn-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v transmission-openvpn_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/transmission-openvpn-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Transmission Openvpn](https://github.com/haugene/transmission-openvpn)
- **Docker Image:** `docker.io/haugene/transmission-openvpn:latest`
- **Documentation:** [GitHub Wiki](https://github.com/haugene/transmission-openvpn/wiki)
- **Issues:** [GitHub Issues](https://github.com/haugene/transmission-openvpn/issues)

