---
title: "Directorylister"
description: "Self-hosted Directorylister deployment via Docker"
---

# Directorylister

Self-hosted Directorylister deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/directorylister/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/directorylister/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/directorylister/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `directorylister` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `4c515b8aadec9e521e55d9551b8ad2312b2270f48eb439c3a08da4e52d07abed` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `directorylister` | docker.io/directorylister/directorylister:latest | Main application service |
| `directorylister_data` | (volume) | Persistent data storage |

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
| `DIRECTORYLISTER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs directorylister
```

**Port conflict:**
Edit `.env` and change `DIRECTORYLISTER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec directorylister ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect directorylister --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v directorylister_data:/data -v $(pwd):/backup alpine tar czf /backup/directorylister-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v directorylister_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/directorylister-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Directorylister](https://github.com/directorylister/directorylister)
- **Docker Image:** `docker.io/directorylister/directorylister:latest`
- **Documentation:** [GitHub Wiki](https://github.com/directorylister/directorylister/wiki)
- **Issues:** [GitHub Issues](https://github.com/directorylister/directorylister/issues)

