---
title: "Lidify"
description: "Self-hosted Lidify deployment via Docker"
---

# Lidify

Self-hosted Lidify deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lidify/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lidify/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lidify/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `lidify` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f270ed0042b34da635bb9208af8938754ce77c27519a0caae3f0dce36f0a9062` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `lidify` | docker.io/thewicklowwolf/lidify:latest | Main application service |
| `lidify_data` | (volume) | Persistent data storage |

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
| `LIDIFY_PORT` | `3000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs lidify
```

**Port conflict:**
Edit `.env` and change `LIDIFY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec lidify ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect lidify --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v lidify_data:/data -v $(pwd):/backup alpine tar czf /backup/lidify-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v lidify_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/lidify-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Lidify](https://github.com/thewicklowwolf/lidify)
- **Docker Image:** `docker.io/thewicklowwolf/lidify:latest`
- **Documentation:** [GitHub Wiki](https://github.com/thewicklowwolf/lidify/wiki)
- **Issues:** [GitHub Issues](https://github.com/thewicklowwolf/lidify/issues)

