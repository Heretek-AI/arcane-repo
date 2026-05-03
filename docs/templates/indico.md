---
title: "Indico"
description: "Self-hosted Indico deployment via Docker"
---

# Indico

Self-hosted Indico deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/indico/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/indico/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/indico/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `indico` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `fd89fe8d996cc704c295afd44e08336ea014c4552f0f8026eff64a7048cf4ecd` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `indico` | ghcr.io/indico/indico:latest | Main application service |
| `indico_data` | (volume) | Persistent data storage |

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
| `INDICO_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs indico
```

**Port conflict:**
Edit `.env` and change `INDICO_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec indico ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect indico --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v indico_data:/data -v $(pwd):/backup alpine tar czf /backup/indico-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v indico_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/indico-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Indico](https://github.com/indico/indico)
- **Docker Image:** `ghcr.io/indico/indico:latest`
- **Documentation:** [GitHub Wiki](https://github.com/indico/indico/wiki)
- **Issues:** [GitHub Issues](https://github.com/indico/indico/issues)

