---
title: "Docker Mailserver"
description: "Self-hosted Docker Mailserver deployment via Docker"
---

# Docker Mailserver

Self-hosted Docker Mailserver deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/communication" class="tag-badge">communication</a> <a href="/categories/devops" class="tag-badge">devops</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docker-mailserver/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docker-mailserver/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docker-mailserver/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `docker-mailserver` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `423c25798c2203c0b6c3c3b32d8ac32c616fe73a2f9252560c206ed576d1fe84` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `docker-mailserver` | ghcr.io/docker-mailserver/docker-mailserver:latest | Main application service |
| `docker-mailserver_data` | (volume) | Persistent data storage |

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
| `DOCKER_MAILSERVER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs docker-mailserver
```

**Port conflict:**
Edit `.env` and change `DOCKER-MAILSERVER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec docker-mailserver ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect docker-mailserver --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v docker-mailserver_data:/data -v $(pwd):/backup alpine tar czf /backup/docker-mailserver-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v docker-mailserver_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/docker-mailserver-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Docker Mailserver](https://github.com/docker-mailserver/docker-mailserver)
- **Docker Image:** `ghcr.io/docker-mailserver/docker-mailserver:latest`
- **Documentation:** [GitHub Wiki](https://github.com/docker-mailserver/docker-mailserver/wiki)
- **Issues:** [GitHub Issues](https://github.com/docker-mailserver/docker-mailserver/issues)

