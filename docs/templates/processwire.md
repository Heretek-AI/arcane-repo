---
title: "Processwire"
description: "Self-hosted Processwire deployment via Docker"
---

# Processwire

Self-hosted Processwire deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/processwire/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/processwire/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/processwire/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `processwire` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `258a0a3052bac7a16ab47a0f5176e94f57d1df9bb23859940b2a1801c371d8b5` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `processwire` | docker.io/poljpocket/processwire:latest | Main application service |
| `processwire_data` | (volume) | Persistent data storage |

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
| `PROCESSWIRE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs processwire
```

**Port conflict:**
Edit `.env` and change `PROCESSWIRE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec processwire ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect processwire --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v processwire_data:/data -v $(pwd):/backup alpine tar czf /backup/processwire-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v processwire_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/processwire-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Processwire](https://github.com/poljpocket/processwire)
- **Docker Image:** `docker.io/poljpocket/processwire:latest`
- **Documentation:** [GitHub Wiki](https://github.com/poljpocket/processwire/wiki)
- **Issues:** [GitHub Issues](https://github.com/poljpocket/processwire/issues)

