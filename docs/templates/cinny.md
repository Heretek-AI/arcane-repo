---
title: "Cinny"
description: "Self-hosted Cinny deployment via Docker"
---

# Cinny

Self-hosted Cinny deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/devops" class="tag-badge">devops</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cinny/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cinny/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cinny/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cinny` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `9f05caecd8e8cd8c701bc10aacbb8965675a9e2d0bf6b6916a73a01056dcb632` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `cinny` | docker.io/ajbura/cinny:latest | Main application service |
| `cinny_data` | (volume) | Persistent data storage |

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
| `CINNY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs cinny
```

**Port conflict:**
Edit `.env` and change `CINNY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec cinny ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect cinny --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v cinny_data:/data -v $(pwd):/backup alpine tar czf /backup/cinny-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v cinny_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/cinny-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Cinny](https://github.com/ajbura/cinny)
- **Docker Image:** `docker.io/ajbura/cinny:latest`
- **Documentation:** [GitHub Wiki](https://github.com/ajbura/cinny/wiki)
- **Issues:** [GitHub Issues](https://github.com/ajbura/cinny/issues)

