---
title: "Paymenter"
description: "Self-hosted Paymenter deployment via Docker"
---

# Paymenter

Self-hosted Paymenter deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/paymenter/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/paymenter/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/paymenter/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `paymenter` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a0f85f0cf39b370995b60aab4cb4a480e19e61a8334d1a74484eedba447dd43a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `paymenter` | ghcr.io/paymenter/paymenter:latest | Main application service |
| `paymenter_data` | (volume) | Persistent data storage |

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
| `PAYMENTER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs paymenter
```

**Port conflict:**
Edit `.env` and change `PAYMENTER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec paymenter ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect paymenter --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v paymenter_data:/data -v $(pwd):/backup alpine tar czf /backup/paymenter-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v paymenter_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/paymenter-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Paymenter](https://github.com/paymenter/paymenter)
- **Docker Image:** `ghcr.io/paymenter/paymenter:latest`
- **Documentation:** [GitHub Wiki](https://github.com/paymenter/paymenter/wiki)
- **Issues:** [GitHub Issues](https://github.com/paymenter/paymenter/issues)

