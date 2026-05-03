---
title: "Linkwarden"
description: "Self-hosted Linkwarden deployment via Docker"
---

# Linkwarden

Self-hosted Linkwarden deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/linkwarden/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/linkwarden/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/linkwarden/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `linkwarden` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a237b1577723d8d00dd13a9b76e9bef66382030430af76d4c8d1a01b246e848c` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `linkwarden` | ghcr.io/linkwarden/linkwarden:latest | Main application service |
| `linkwarden_data` | (volume) | Persistent data storage |

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
| `LINKWARDEN_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs linkwarden
```

**Port conflict:**
Edit `.env` and change `LINKWARDEN_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec linkwarden ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect linkwarden --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v linkwarden_data:/data -v $(pwd):/backup alpine tar czf /backup/linkwarden-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v linkwarden_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/linkwarden-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Linkwarden](https://github.com/linkwarden/linkwarden)
- **Docker Image:** `ghcr.io/linkwarden/linkwarden:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linkwarden/linkwarden/wiki)
- **Issues:** [GitHub Issues](https://github.com/linkwarden/linkwarden/issues)

