---
title: "Bitaxe Sentry"
description: "Self-hosted Bitaxe Sentry deployment via Docker"
---

# Bitaxe Sentry

Self-hosted Bitaxe Sentry deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bitaxe-sentry/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bitaxe-sentry/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bitaxe-sentry/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `bitaxe-sentry` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `39e5dffa4d38c8b0451e0abd16220a18d267ffbb5818c35c1ef95eb662241fc8` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `bitaxe-sentry` | docker.io/zachprice105/bitaxe-sentry:latest | Main application service |
| `bitaxe-sentry_data` | (volume) | Persistent data storage |

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
| `BITAXE_SENTRY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs bitaxe-sentry
```

**Port conflict:**
Edit `.env` and change `BITAXE-SENTRY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec bitaxe-sentry ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect bitaxe-sentry --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v bitaxe-sentry_data:/data -v $(pwd):/backup alpine tar czf /backup/bitaxe-sentry-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v bitaxe-sentry_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/bitaxe-sentry-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Bitaxe Sentry](https://github.com/zachprice105/bitaxe-sentry)
- **Docker Image:** `docker.io/zachprice105/bitaxe-sentry:latest`
- **Documentation:** [GitHub Wiki](https://github.com/zachprice105/bitaxe-sentry/wiki)
- **Issues:** [GitHub Issues](https://github.com/zachprice105/bitaxe-sentry/issues)

