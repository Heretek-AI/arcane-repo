---
title: "Quassel Core"
description: "Self-hosted Quassel Core deployment via Docker"
---

# Quassel Core

Self-hosted Quassel Core deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/quassel-core/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/quassel-core/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/quassel-core/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `quassel-core` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `dca982520012312579c474c83f1c2545ae8c4937cff158805ec805f10b2856ce` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `quassel-core` | ghcr.io/linuxserver/quassel-core:latest | Main application service |
| `quassel-core_data` | (volume) | Persistent data storage |

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
| `QUASSEL_CORE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs quassel-core
```

**Port conflict:**
Edit `.env` and change `QUASSEL-CORE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec quassel-core ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect quassel-core --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v quassel-core_data:/data -v $(pwd):/backup alpine tar czf /backup/quassel-core-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v quassel-core_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/quassel-core-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Quassel Core](https://github.com/linuxserver/quassel-core)
- **Docker Image:** `ghcr.io/linuxserver/quassel-core:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/quassel-core/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/quassel-core/issues)

