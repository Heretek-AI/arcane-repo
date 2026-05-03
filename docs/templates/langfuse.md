---
title: "Langfuse"
description: "Self-hosted Langfuse deployment via Docker"
---

# Langfuse

Self-hosted Langfuse deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/langfuse/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/langfuse/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/langfuse/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `langfuse` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `09d2129987377124e37aed2543aaed565eefd0d16c42b886ce71104a3eb24a42` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `langfuse` | ghcr.io/langfuse/langfuse:latest | Main application service |
| `langfuse_data` | (volume) | Persistent data storage |

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
| `LANGFUSE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs langfuse
```

**Port conflict:**
Edit `.env` and change `LANGFUSE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec langfuse ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect langfuse --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v langfuse_data:/data -v $(pwd):/backup alpine tar czf /backup/langfuse-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v langfuse_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/langfuse-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Langfuse](https://github.com/langfuse/langfuse)
- **Docker Image:** `ghcr.io/langfuse/langfuse:latest`
- **Documentation:** [GitHub Wiki](https://github.com/langfuse/langfuse/wiki)
- **Issues:** [GitHub Issues](https://github.com/langfuse/langfuse/issues)

