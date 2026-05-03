---
title: "Cannery"
description: "Self-hosted pantry and food inventory tracker that helps manage stored food, expiration dates, and stock levels."
---

# Cannery

Self-hosted pantry and food inventory tracker that helps manage stored food, expiration dates, and stock levels.

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cannery/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cannery/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cannery/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cannery` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b05cb50bbfe8eacd3a6c33e4f5e1ecf95b9dd93d06dbbd782d46fe39a09e9cfc` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `cannery` | docker.io/shibaobun/cannery:latest | Main application service |
| `cannery_data` | (volume) | Persistent data storage |

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
| `CANNERY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs cannery
```

**Port conflict:**
Edit `.env` and change `CANNERY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec cannery ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect cannery --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v cannery_data:/data -v $(pwd):/backup alpine tar czf /backup/cannery-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v cannery_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/cannery-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Cannery](https://github.com/shibaobun/cannery)
- **Docker Image:** `docker.io/shibaobun/cannery:latest`
- **Documentation:** [GitHub Wiki](https://github.com/shibaobun/cannery/wiki)
- **Issues:** [GitHub Issues](https://github.com/shibaobun/cannery/issues)

