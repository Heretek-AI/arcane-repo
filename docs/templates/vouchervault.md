---
title: "Vouchervault"
description: "Self-hosted Vouchervault deployment via Docker"
---

# Vouchervault

Self-hosted Vouchervault deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vouchervault/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vouchervault/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vouchervault/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `vouchervault` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6673dc1970ae051d40f62f8d62ceabde1c8cf14b8af47d198e7f8a2820c0b8a1` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `vouchervault` | docker.io/l4rm4nd/vouchervault:latest | Main application service |
| `vouchervault_data` | (volume) | Persistent data storage |

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
| `VOUCHERVAULT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs vouchervault
```

**Port conflict:**
Edit `.env` and change `VOUCHERVAULT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec vouchervault ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect vouchervault --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v vouchervault_data:/data -v $(pwd):/backup alpine tar czf /backup/vouchervault-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v vouchervault_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/vouchervault-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Vouchervault](https://github.com/l4rm4nd/vouchervault)
- **Docker Image:** `docker.io/l4rm4nd/vouchervault:latest`
- **Documentation:** [GitHub Wiki](https://github.com/l4rm4nd/vouchervault/wiki)
- **Issues:** [GitHub Issues](https://github.com/l4rm4nd/vouchervault/issues)

