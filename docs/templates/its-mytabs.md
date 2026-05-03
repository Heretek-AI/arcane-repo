---
title: "Its Mytabs"
description: "Self-hosted Its Mytabs deployment via Docker"
---

# Its Mytabs

Self-hosted Its Mytabs deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/its-mytabs/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/its-mytabs/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/its-mytabs/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `its-mytabs` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c2d8b3716c3f5f3a9abbbff134ef796cf2bf171cc7e2d1078666129e22333142` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `its-mytabs` | ghcr.io/louislam/its-mytabs:latest | Main application service |
| `its-mytabs_data` | (volume) | Persistent data storage |

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
| `ITS_MYTABS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs its-mytabs
```

**Port conflict:**
Edit `.env` and change `ITS-MYTABS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec its-mytabs ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect its-mytabs --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v its-mytabs_data:/data -v $(pwd):/backup alpine tar czf /backup/its-mytabs-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v its-mytabs_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/its-mytabs-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Its Mytabs](https://github.com/louislam/its-mytabs)
- **Docker Image:** `ghcr.io/louislam/its-mytabs:latest`
- **Documentation:** [GitHub Wiki](https://github.com/louislam/its-mytabs/wiki)
- **Issues:** [GitHub Issues](https://github.com/louislam/its-mytabs/issues)

