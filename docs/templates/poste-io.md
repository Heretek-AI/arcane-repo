---
title: "Poste.Io"
description: "Self-hosted Poste.Io deployment via Docker"
---

# Poste.Io

Self-hosted Poste.Io deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/poste-io/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/poste-io/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/poste-io/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `poste-io` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `dd3ea188d6e8dc5e67340cce52f034f0b9904926c94f3374385bde97b3123fd1` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `poste-io` | docker.io/analogic/poste.io:latest | Main application service |
| `poste-io_data` | (volume) | Persistent data storage |

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
| `POSTE_IO_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs poste-io
```

**Port conflict:**
Edit `.env` and change `POSTE-IO_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec poste-io ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect poste-io --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v poste-io_data:/data -v $(pwd):/backup alpine tar czf /backup/poste-io-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v poste-io_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/poste-io-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Poste.Io](https://github.com/analogic/poste.io)
- **Docker Image:** `docker.io/analogic/poste.io:latest`
- **Documentation:** [GitHub Wiki](https://github.com/analogic/poste.io/wiki)
- **Issues:** [GitHub Issues](https://github.com/analogic/poste.io/issues)

