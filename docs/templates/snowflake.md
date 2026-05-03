---
title: "Snowflake"
description: "Self-hosted Snowflake deployment via Docker"
---

# Snowflake

Self-hosted Snowflake deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/snowflake/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/snowflake/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/snowflake/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `snowflake` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `96c288e29f35db3f01c2475687c6405b6c7d9e94e5fcc61006cf0203fa89860d` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `snowflake` | docker.io/tzuehlke/snowflake:latest | Main application service |
| `snowflake_data` | (volume) | Persistent data storage |

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
| `SNOWFLAKE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs snowflake
```

**Port conflict:**
Edit `.env` and change `SNOWFLAKE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec snowflake ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect snowflake --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v snowflake_data:/data -v $(pwd):/backup alpine tar czf /backup/snowflake-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v snowflake_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/snowflake-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Snowflake](https://github.com/tzuehlke/snowflake)
- **Docker Image:** `docker.io/tzuehlke/snowflake:latest`
- **Documentation:** [GitHub Wiki](https://github.com/tzuehlke/snowflake/wiki)
- **Issues:** [GitHub Issues](https://github.com/tzuehlke/snowflake/issues)

