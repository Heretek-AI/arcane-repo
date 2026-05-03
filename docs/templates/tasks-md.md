---
title: "Tasks.Md"
description: "Self-hosted Tasks.Md deployment via Docker"
---

# Tasks.Md

Self-hosted Tasks.Md deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tasks-md/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tasks-md/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tasks-md/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tasks-md` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `67764c0dd56bb27dc0c720ab9a38040a17d42b41026725906ff013d6ca635e9e` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `tasks-md` | docker.io/baldissaramatheus/tasks.md:latest | Main application service |
| `tasks-md_data` | (volume) | Persistent data storage |

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
| `TASKS_MD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs tasks-md
```

**Port conflict:**
Edit `.env` and change `TASKS-MD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec tasks-md ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect tasks-md --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v tasks-md_data:/data -v $(pwd):/backup alpine tar czf /backup/tasks-md-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v tasks-md_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/tasks-md-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Tasks.Md](https://github.com/baldissaramatheus/tasks.md)
- **Docker Image:** `docker.io/baldissaramatheus/tasks.md:latest`
- **Documentation:** [GitHub Wiki](https://github.com/baldissaramatheus/tasks.md/wiki)
- **Issues:** [GitHub Issues](https://github.com/baldissaramatheus/tasks.md/issues)

