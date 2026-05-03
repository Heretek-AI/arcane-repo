---
title: "Languagetool"
description: "Self-hosted Languagetool deployment via Docker"
---

# Languagetool

Self-hosted Languagetool deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/languagetool/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/languagetool/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/languagetool/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `languagetool` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6e4cfcfb3a92c7d0467a8bd5bcd49ea29be496f9bd8c535cee428709505a1f47` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `languagetool` | docker.io/erikvl87/languagetool:latest | Main application service |
| `languagetool_data` | (volume) | Persistent data storage |

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
| `LANGUAGETOOL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs languagetool
```

**Port conflict:**
Edit `.env` and change `LANGUAGETOOL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec languagetool ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect languagetool --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v languagetool_data:/data -v $(pwd):/backup alpine tar czf /backup/languagetool-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v languagetool_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/languagetool-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Languagetool](https://github.com/erikvl87/languagetool)
- **Docker Image:** `docker.io/erikvl87/languagetool:latest`
- **Documentation:** [GitHub Wiki](https://github.com/erikvl87/languagetool/wiki)
- **Issues:** [GitHub Issues](https://github.com/erikvl87/languagetool/issues)

