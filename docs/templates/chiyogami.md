---
title: "Chiyogami"
description: "Self-hosted wallpaper management and rotation tool for organizing and cycling through desktop wallpapers."
---

# Chiyogami

Self-hosted wallpaper management and rotation tool for organizing and cycling through desktop wallpapers.

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chiyogami/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chiyogami/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chiyogami/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `chiyogami` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d8597b3eb5ab95dc8969f16cdbbcae5a1796e6da8794b46592829ac3a09229c4` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `chiyogami` | ghcr.io/rhee876527/chiyogami:latest | Main application service |
| `chiyogami_data` | (volume) | Persistent data storage |

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
| `CHIYOGAMI_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs chiyogami
```

**Port conflict:**
Edit `.env` and change `CHIYOGAMI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec chiyogami ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect chiyogami --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v chiyogami_data:/data -v $(pwd):/backup alpine tar czf /backup/chiyogami-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v chiyogami_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/chiyogami-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Chiyogami](https://github.com/rhee876527/chiyogami)
- **Docker Image:** `ghcr.io/rhee876527/chiyogami:latest`
- **Documentation:** [GitHub Wiki](https://github.com/rhee876527/chiyogami/wiki)
- **Issues:** [GitHub Issues](https://github.com/rhee876527/chiyogami/issues)

