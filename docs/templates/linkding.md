---
title: "Linkding"
description: "Self-hosted Linkding deployment via Docker"
---

# Linkding

Self-hosted Linkding deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/linkding/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/linkding/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/linkding/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `linkding` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c2ec3f02aece07b357183cf562ca162275b1b09d621416b6075f13cbe6cb2e03` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `linkding` | ghcr.io/sissbruecker/linkding:latest | Main application service |
| `linkding_data` | (volume) | Persistent data storage |

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
| `LINKDING_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs linkding
```

**Port conflict:**
Edit `.env` and change `LINKDING_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec linkding ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect linkding --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v linkding_data:/data -v $(pwd):/backup alpine tar czf /backup/linkding-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v linkding_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/linkding-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Linkding](https://github.com/sissbruecker/linkding)
- **Docker Image:** `ghcr.io/sissbruecker/linkding:latest`
- **Documentation:** [GitHub Wiki](https://github.com/sissbruecker/linkding/wiki)
- **Issues:** [GitHub Issues](https://github.com/sissbruecker/linkding/issues)

