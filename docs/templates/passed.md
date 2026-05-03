---
title: "Passed"
description: "Self-hosted Passed deployment via Docker"
---

# Passed

Self-hosted Passed deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/passed/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/passed/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/passed/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `passed` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `682ef7fc3caba7a6dee02d7db4e1876885fedf22fce0b50c141e6122ce4785ad` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `passed` | docker.io/shokohsc/passed:latest | Main application service |
| `passed_data` | (volume) | Persistent data storage |

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
| `PASSED_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs passed
```

**Port conflict:**
Edit `.env` and change `PASSED_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec passed ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect passed --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v passed_data:/data -v $(pwd):/backup alpine tar czf /backup/passed-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v passed_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/passed-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Passed](https://github.com/shokohsc/passed)
- **Docker Image:** `docker.io/shokohsc/passed:latest`
- **Documentation:** [GitHub Wiki](https://github.com/shokohsc/passed/wiki)
- **Issues:** [GitHub Issues](https://github.com/shokohsc/passed/issues)

