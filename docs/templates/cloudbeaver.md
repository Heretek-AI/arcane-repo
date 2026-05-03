---
title: "Cloudbeaver"
description: "Self-hosted Cloudbeaver deployment via Docker"
---

# Cloudbeaver

Self-hosted Cloudbeaver deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cloudbeaver/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cloudbeaver/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cloudbeaver/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cloudbeaver` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `67e8597f283409004e7d57d8936ee9f3aeba9820c824363ac418fb508db3f087` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `cloudbeaver` | docker.io/dbeaver/cloudbeaver:latest | Main application service |
| `cloudbeaver_data` | (volume) | Persistent data storage |

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
| `CLOUDBEAVER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs cloudbeaver
```

**Port conflict:**
Edit `.env` and change `CLOUDBEAVER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec cloudbeaver ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect cloudbeaver --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v cloudbeaver_data:/data -v $(pwd):/backup alpine tar czf /backup/cloudbeaver-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v cloudbeaver_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/cloudbeaver-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Cloudbeaver](https://github.com/dbeaver/cloudbeaver)
- **Docker Image:** `docker.io/dbeaver/cloudbeaver:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dbeaver/cloudbeaver/wiki)
- **Issues:** [GitHub Issues](https://github.com/dbeaver/cloudbeaver/issues)

