---
title: "Hedgedoc"
description: "Self-hosted Hedgedoc deployment via Docker"
---

# Hedgedoc

Self-hosted Hedgedoc deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hedgedoc/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hedgedoc/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hedgedoc/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `hedgedoc` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `18eb90a64bb77561a1ca39d1cb9b9b5148baf0eb8646b578dde5b83830faf13a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `hedgedoc` | ghcr.io/linuxserver/hedgedoc:latest | Main application service |
| `hedgedoc_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:3000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `HEDGEDOC_PORT` | `3000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs hedgedoc
```

**Port conflict:**
Edit `.env` and change `HEDGEDOC_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec hedgedoc ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect hedgedoc --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v hedgedoc_data:/data -v $(pwd):/backup alpine tar czf /backup/hedgedoc-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v hedgedoc_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/hedgedoc-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Hedgedoc](https://github.com/linuxserver/hedgedoc)
- **Docker Image:** `ghcr.io/linuxserver/hedgedoc:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/hedgedoc/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/hedgedoc/issues)

