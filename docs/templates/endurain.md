---
title: "Endurain"
description: "Self-hosted Endurain deployment via Docker"
---

# Endurain

Self-hosted Endurain deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/endurain/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/endurain/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/endurain/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `endurain` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1f3ada02eb0c5c6cc826a676b010a8179222091a6ee481d9814440be96a7b6a8` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `endurain` | docker.io/dk2077392/endurain:latest | Main application service |
| `endurain_data` | (volume) | Persistent data storage |

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
| `ENDURAIN_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs endurain
```

**Port conflict:**
Edit `.env` and change `ENDURAIN_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec endurain ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect endurain --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v endurain_data:/data -v $(pwd):/backup alpine tar czf /backup/endurain-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v endurain_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/endurain-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Endurain](https://github.com/dk2077392/endurain)
- **Docker Image:** `docker.io/dk2077392/endurain:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dk2077392/endurain/wiki)
- **Issues:** [GitHub Issues](https://github.com/dk2077392/endurain/issues)

