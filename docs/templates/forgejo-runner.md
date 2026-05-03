---
title: "Forgejo Runner"
description: "Self-hosted Forgejo Runner deployment via Docker"
---

# Forgejo Runner

Self-hosted Forgejo Runner deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/forgejo-runner/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/forgejo-runner/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/forgejo-runner/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `forgejo-runner` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c166529d5b8f55b51757e1c170be0e03b648c4b2845490393351377f3cd029c9` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `forgejo-runner` | docker.io/techvoyager/forgejo_runner:latest | Main application service |
| `forgejo-runner_data` | (volume) | Persistent data storage |

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
| `FORGEJO_RUNNER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs forgejo-runner
```

**Port conflict:**
Edit `.env` and change `FORGEJO-RUNNER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec forgejo-runner ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect forgejo-runner --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v forgejo-runner_data:/data -v $(pwd):/backup alpine tar czf /backup/forgejo-runner-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v forgejo-runner_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/forgejo-runner-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Forgejo Runner](https://github.com/techvoyager/forgejo_runner)
- **Docker Image:** `docker.io/techvoyager/forgejo_runner:latest`
- **Documentation:** [GitHub Wiki](https://github.com/techvoyager/forgejo_runner/wiki)
- **Issues:** [GitHub Issues](https://github.com/techvoyager/forgejo_runner/issues)

