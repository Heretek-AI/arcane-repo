---
title: "Vvveb"
description: "Self-hosted Vvveb deployment via Docker"
---

# Vvveb

Self-hosted Vvveb deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vvveb/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vvveb/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vvveb/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `vvveb` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b1c1c3be4cc3cf37c4949df6f0091473fa159cddf402812dc136be920ca738ce` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `vvveb` | docker.io/hamidno/vvveb:latest | Main application service |
| `vvveb_data` | (volume) | Persistent data storage |

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
| `VVVEB_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs vvveb
```

**Port conflict:**
Edit `.env` and change `VVVEB_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec vvveb ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect vvveb --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v vvveb_data:/data -v $(pwd):/backup alpine tar czf /backup/vvveb-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v vvveb_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/vvveb-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Vvveb](https://github.com/hamidno/vvveb)
- **Docker Image:** `docker.io/hamidno/vvveb:latest`
- **Documentation:** [GitHub Wiki](https://github.com/hamidno/vvveb/wiki)
- **Issues:** [GitHub Issues](https://github.com/hamidno/vvveb/issues)

