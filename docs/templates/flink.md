---
title: "Flink"
description: "Self-hosted Flink deployment via Docker"
---

# Flink

Self-hosted Flink deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flink/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flink/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flink/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `flink` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `72dd92bed673b5b3bf2fd6944550f4d71210be29421dc8a6061605a18f6afd11` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `flink` | docker.io/apache/flink:latest | Main application service |
| `flink_data` | (volume) | Persistent data storage |

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
| `FLINK_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs flink
```

**Port conflict:**
Edit `.env` and change `FLINK_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec flink ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect flink --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v flink_data:/data -v $(pwd):/backup alpine tar czf /backup/flink-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v flink_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/flink-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Flink](https://github.com/apache/flink)
- **Docker Image:** `docker.io/apache/flink:latest`
- **Documentation:** [GitHub Wiki](https://github.com/apache/flink/wiki)
- **Issues:** [GitHub Issues](https://github.com/apache/flink/issues)

