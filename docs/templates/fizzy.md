---
title: "Fizzy"
description: "Self-hosted Fizzy deployment via Docker"
---

# Fizzy

Self-hosted Fizzy deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fizzy/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fizzy/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fizzy/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `fizzy` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `06ddb671f0a88e4539382df09d04ee2ec0df4b5ecbe23019bb5ea4c67b7c5229` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `fizzy` | docker.io/findingfocusdev/fizzy:latest | Main application service |
| `fizzy_data` | (volume) | Persistent data storage |

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
| `FIZZY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs fizzy
```

**Port conflict:**
Edit `.env` and change `FIZZY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec fizzy ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect fizzy --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v fizzy_data:/data -v $(pwd):/backup alpine tar czf /backup/fizzy-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v fizzy_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/fizzy-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Fizzy](https://github.com/findingfocusdev/fizzy)
- **Docker Image:** `docker.io/findingfocusdev/fizzy:latest`
- **Documentation:** [GitHub Wiki](https://github.com/findingfocusdev/fizzy/wiki)
- **Issues:** [GitHub Issues](https://github.com/findingfocusdev/fizzy/issues)

