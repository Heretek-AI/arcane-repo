---
title: "Pocket Id"
description: "Self-hosted Pocket Id deployment via Docker"
---

# Pocket Id

Self-hosted Pocket Id deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pocket-id/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pocket-id/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pocket-id/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pocket-id` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `76642dfd032f0e528712dc8bb0b083dfdecb8aa7c3917c8014fc4d989aa83b8a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `pocket-id` | ghcr.io/pocket-id/pocket-id:latest | Main application service |
| `pocket-id_data` | (volume) | Persistent data storage |

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
| `POCKET_ID_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs pocket-id
```

**Port conflict:**
Edit `.env` and change `POCKET-ID_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pocket-id ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pocket-id --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pocket-id_data:/data -v $(pwd):/backup alpine tar czf /backup/pocket-id-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pocket-id_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pocket-id-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Pocket Id](https://github.com/pocket-id/pocket-id)
- **Docker Image:** `ghcr.io/pocket-id/pocket-id:latest`
- **Documentation:** [GitHub Wiki](https://github.com/pocket-id/pocket-id/wiki)
- **Issues:** [GitHub Issues](https://github.com/pocket-id/pocket-id/issues)

