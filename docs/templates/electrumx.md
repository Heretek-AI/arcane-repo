---
title: "Electrumx"
description: "Self-hosted Electrumx deployment via Docker"
---

# Electrumx

Self-hosted Electrumx deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/electrumx/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/electrumx/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/electrumx/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `electrumx` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `edc1707423f723803b696ddee46f752be73a4cf87f0ad1c003a52d9c7b9763a4` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `electrumx` | docker.io/lukechilds/electrumx:latest | Main application service |
| `electrumx_data` | (volume) | Persistent data storage |

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
| `ELECTRUMX_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs electrumx
```

**Port conflict:**
Edit `.env` and change `ELECTRUMX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec electrumx ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect electrumx --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v electrumx_data:/data -v $(pwd):/backup alpine tar czf /backup/electrumx-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v electrumx_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/electrumx-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Electrumx](https://github.com/lukechilds/electrumx)
- **Docker Image:** `docker.io/lukechilds/electrumx:latest`
- **Documentation:** [GitHub Wiki](https://github.com/lukechilds/electrumx/wiki)
- **Issues:** [GitHub Issues](https://github.com/lukechilds/electrumx/issues)

