---
title: "Homeassistant"
description: "Self-hosted Homeassistant deployment via Docker"
---

# Homeassistant

Self-hosted Homeassistant deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/homeassistant/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/homeassistant/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/homeassistant/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `homeassistant` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3b56672a957c1ffa60b69f1d43e779c813cf10514bbeadbc12424cb22094f51b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `homeassistant` | ghcr.io/linuxserver/homeassistant:latest | Main application service |
| `homeassistant_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:8123/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8123](http://localhost:8123) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `HOMEASSISTANT_PORT` | `8123` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs homeassistant
```

**Port conflict:**
Edit `.env` and change `HOMEASSISTANT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec homeassistant ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect homeassistant --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v homeassistant_data:/data -v $(pwd):/backup alpine tar czf /backup/homeassistant-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v homeassistant_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/homeassistant-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Homeassistant](https://github.com/linuxserver/homeassistant)
- **Docker Image:** `ghcr.io/linuxserver/homeassistant:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/homeassistant/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/homeassistant/issues)

