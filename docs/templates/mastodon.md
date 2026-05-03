---
title: "Mastodon"
description: "Self-hosted Mastodon deployment via Docker"
---

# Mastodon

Self-hosted Mastodon deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mastodon/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mastodon/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mastodon/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mastodon` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `bef23ae1fe33388d8f6884722726220f6baa4892c542e4ffae3ec422083674f2` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `mastodon` | ghcr.io/mastodon/mastodon:latest | Main application service |
| `mastodon_data` | (volume) | Persistent data storage |

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
| `MASTODON_PORT` | `3000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs mastodon
```

**Port conflict:**
Edit `.env` and change `MASTODON_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec mastodon ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect mastodon --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v mastodon_data:/data -v $(pwd):/backup alpine tar czf /backup/mastodon-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v mastodon_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/mastodon-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Mastodon](https://github.com/mastodon/mastodon)
- **Docker Image:** `ghcr.io/mastodon/mastodon:latest`
- **Documentation:** [GitHub Wiki](https://github.com/mastodon/mastodon/wiki)
- **Issues:** [GitHub Issues](https://github.com/mastodon/mastodon/issues)

