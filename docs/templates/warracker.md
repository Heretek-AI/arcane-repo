---
title: "Warracker"
description: "Self-hosted Warracker deployment via Docker"
---

# Warracker

Self-hosted Warracker deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/warracker/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/warracker/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/warracker/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `warracker` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a9f99b718f0b5402a011c5e3bb0031892f5320bfc27652c83d5cbb6729ba2d72` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `warracker` | docker.io/legamy/warracker:latest | Main application service |
| `warracker_data` | (volume) | Persistent data storage |

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
| `WARRACKER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs warracker
```

**Port conflict:**
Edit `.env` and change `WARRACKER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec warracker ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect warracker --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v warracker_data:/data -v $(pwd):/backup alpine tar czf /backup/warracker-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v warracker_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/warracker-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Warracker](https://github.com/legamy/warracker)
- **Docker Image:** `docker.io/legamy/warracker:latest`
- **Documentation:** [GitHub Wiki](https://github.com/legamy/warracker/wiki)
- **Issues:** [GitHub Issues](https://github.com/legamy/warracker/issues)

