---
title: "Automatisch"
description: "Self-hosted business automation tool that connects your apps and automates workflows without coding, similar to Zapier."
---

# Automatisch

Self-hosted business automation tool that connects your apps and automates workflows without coding, similar to Zapier.

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/automatisch/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/automatisch/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/automatisch/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `automatisch` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1fe2785d6ffa8763384b74fcbf4c80598b3f3eb980c1df8b9408cbedacc4713b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `automatisch` | ghcr.io/automatisch/automatisch:latest | Main application service |
| `automatisch_data` | (volume) | Persistent data storage |

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
| `AUTOMATISCH_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs automatisch
```

**Port conflict:**
Edit `.env` and change `AUTOMATISCH_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec automatisch ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect automatisch --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v automatisch_data:/data -v $(pwd):/backup alpine tar czf /backup/automatisch-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v automatisch_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/automatisch-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Automatisch](https://github.com/automatisch/automatisch)
- **Docker Image:** `ghcr.io/automatisch/automatisch:latest`
- **Documentation:** [GitHub Wiki](https://github.com/automatisch/automatisch/wiki)
- **Issues:** [GitHub Issues](https://github.com/automatisch/automatisch/issues)

