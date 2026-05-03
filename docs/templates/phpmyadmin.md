---
title: "Phpmyadmin"
description: "Self-hosted Phpmyadmin deployment via Docker"
---

# Phpmyadmin

Self-hosted Phpmyadmin deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/phpmyadmin/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/phpmyadmin/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/phpmyadmin/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `phpmyadmin` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `772a969d5744b00c9c0d5bcc807bb2fa166d5f863728ac513f1012c6b2614e5c` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `phpmyadmin` | docker.io/library/phpmyadmin:latest | Main application service |
| `phpmyadmin_data` | (volume) | Persistent data storage |

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
| `PHPMYADMIN_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs phpmyadmin
```

**Port conflict:**
Edit `.env` and change `PHPMYADMIN_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec phpmyadmin ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect phpmyadmin --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v phpmyadmin_data:/data -v $(pwd):/backup alpine tar czf /backup/phpmyadmin-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v phpmyadmin_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/phpmyadmin-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/library/phpmyadmin:latest`

