---
title: "Dumbbudget"
description: "Self-hosted Dumbbudget deployment via Docker"
---

# Dumbbudget

Self-hosted Dumbbudget deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbbudget/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbbudget/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbbudget/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dumbbudget` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `4e8046cd7bde9313a2c792d2d75d1c17cd21116debc468cb52cade01216d6286` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `dumbbudget` | docker.io/dumbwareio/dumbbudget:latest | Main application service |
| `dumbbudget_data` | (volume) | Persistent data storage |

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
| `DUMBBUDGET_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs dumbbudget
```

**Port conflict:**
Edit `.env` and change `DUMBBUDGET_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dumbbudget ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dumbbudget --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dumbbudget_data:/data -v $(pwd):/backup alpine tar czf /backup/dumbbudget-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dumbbudget_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dumbbudget-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Dumbbudget](https://github.com/dumbwareio/dumbbudget)
- **Docker Image:** `docker.io/dumbwareio/dumbbudget:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dumbwareio/dumbbudget/wiki)
- **Issues:** [GitHub Issues](https://github.com/dumbwareio/dumbbudget/issues)

