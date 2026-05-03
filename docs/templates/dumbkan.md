---
title: "Dumbkan"
description: "Self-hosted Dumbkan deployment via Docker"
---

# Dumbkan

Self-hosted Dumbkan deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbkan/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbkan/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbkan/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dumbkan` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `41331361e08d3a0153a42eac2b13a42a97e2ee3466ed81faf1b9fd60e6f3df7f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `dumbkan` | docker.io/dumbwareio/dumbkan:latest | Main application service |
| `dumbkan_data` | (volume) | Persistent data storage |

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
| `DUMBKAN_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs dumbkan
```

**Port conflict:**
Edit `.env` and change `DUMBKAN_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dumbkan ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dumbkan --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dumbkan_data:/data -v $(pwd):/backup alpine tar czf /backup/dumbkan-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dumbkan_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dumbkan-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Dumbkan](https://github.com/dumbwareio/dumbkan)
- **Docker Image:** `docker.io/dumbwareio/dumbkan:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dumbwareio/dumbkan/wiki)
- **Issues:** [GitHub Issues](https://github.com/dumbwareio/dumbkan/issues)

