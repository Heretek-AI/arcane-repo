---
title: "Mstream"
description: "Self-hosted Mstream deployment via Docker"
---

# Mstream

Self-hosted Mstream deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mstream/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mstream/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mstream/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mstream` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `619a12b5d4310c113352f65b540f5eb341ec48a09e2112ddf974d9f618111fe2` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `mstream` | ghcr.io/linuxserver/mstream:latest | Main application service |
| `mstream_data` | (volume) | Persistent data storage |

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
| `MSTREAM_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs mstream
```

**Port conflict:**
Edit `.env` and change `MSTREAM_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec mstream ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect mstream --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v mstream_data:/data -v $(pwd):/backup alpine tar czf /backup/mstream-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v mstream_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/mstream-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Mstream](https://github.com/linuxserver/mstream)
- **Docker Image:** `ghcr.io/linuxserver/mstream:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/mstream/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/mstream/issues)

