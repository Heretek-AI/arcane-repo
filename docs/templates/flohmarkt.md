---
title: "Flohmarkt"
description: "Self-hosted Flohmarkt deployment via Docker"
---

# Flohmarkt

Self-hosted Flohmarkt deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flohmarkt/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flohmarkt/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flohmarkt/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `flohmarkt` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `93103aa47758a730090c3af8c9698d667cd53a3b37c565f974f41f7f50626b71` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `flohmarkt` | docker.io/yonggan/flohmarkt:latest | Main application service |
| `flohmarkt_data` | (volume) | Persistent data storage |

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
| `FLOHMARKT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs flohmarkt
```

**Port conflict:**
Edit `.env` and change `FLOHMARKT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec flohmarkt ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect flohmarkt --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v flohmarkt_data:/data -v $(pwd):/backup alpine tar czf /backup/flohmarkt-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v flohmarkt_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/flohmarkt-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Flohmarkt](https://github.com/yonggan/flohmarkt)
- **Docker Image:** `docker.io/yonggan/flohmarkt:latest`
- **Documentation:** [GitHub Wiki](https://github.com/yonggan/flohmarkt/wiki)
- **Issues:** [GitHub Issues](https://github.com/yonggan/flohmarkt/issues)

