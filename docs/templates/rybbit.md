---
title: "Rybbit"
description: "Self-hosted Rybbit deployment via Docker"
---

# Rybbit

Self-hosted Rybbit deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rybbit/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rybbit/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rybbit/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `rybbit` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `7b454c96f1e2e1b82495f28ead4a886234e2eb80f082c7b9d9d8f1ecd2b4881e` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `rybbit` | docker.io/allocateengineering/rybbit:latest | Main application service |
| `rybbit_data` | (volume) | Persistent data storage |

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
| `RYBBIT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs rybbit
```

**Port conflict:**
Edit `.env` and change `RYBBIT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec rybbit ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect rybbit --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v rybbit_data:/data -v $(pwd):/backup alpine tar czf /backup/rybbit-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v rybbit_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/rybbit-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Rybbit](https://github.com/allocateengineering/rybbit)
- **Docker Image:** `docker.io/allocateengineering/rybbit:latest`
- **Documentation:** [GitHub Wiki](https://github.com/allocateengineering/rybbit/wiki)
- **Issues:** [GitHub Issues](https://github.com/allocateengineering/rybbit/issues)

