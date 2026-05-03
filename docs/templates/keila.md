---
title: "Keila"
description: "Self-hosted Keila deployment via Docker"
---

# Keila

Self-hosted Keila deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/keila/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/keila/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/keila/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `keila` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c26f992514427f037cb76ba7cb17449bf3342fc32038d278af232973e5898286` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `keila` | docker.io/pentacent/keila:latest | Main application service |
| `keila_data` | (volume) | Persistent data storage |

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
| `KEILA_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs keila
```

**Port conflict:**
Edit `.env` and change `KEILA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec keila ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect keila --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v keila_data:/data -v $(pwd):/backup alpine tar czf /backup/keila-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v keila_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/keila-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Keila](https://github.com/pentacent/keila)
- **Docker Image:** `docker.io/pentacent/keila:latest`
- **Documentation:** [GitHub Wiki](https://github.com/pentacent/keila/wiki)
- **Issues:** [GitHub Issues](https://github.com/pentacent/keila/issues)

