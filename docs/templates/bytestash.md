---
title: "Bytestash"
description: "Self-hosted code snippet manager for storing, organizing, and sharing code snippets with syntax highlighting."
---

# Bytestash

Self-hosted code snippet manager for storing, organizing, and sharing code snippets with syntax highlighting.

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bytestash/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bytestash/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bytestash/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `bytestash` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c323356c1030174776f5f27c518334ca2461d0f43050cd49769037f0d08529bd` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `bytestash` | ghcr.io/jordan-dalby/bytestash:latest | Main application service |
| `bytestash_data` | (volume) | Persistent data storage |

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
| `BYTESTASH_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs bytestash
```

**Port conflict:**
Edit `.env` and change `BYTESTASH_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec bytestash ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect bytestash --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v bytestash_data:/data -v $(pwd):/backup alpine tar czf /backup/bytestash-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v bytestash_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/bytestash-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Bytestash](https://github.com/jordan-dalby/bytestash)
- **Docker Image:** `ghcr.io/jordan-dalby/bytestash:latest`
- **Documentation:** [GitHub Wiki](https://github.com/jordan-dalby/bytestash/wiki)
- **Issues:** [GitHub Issues](https://github.com/jordan-dalby/bytestash/issues)

