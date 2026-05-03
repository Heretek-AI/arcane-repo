---
title: "Plainpad"
description: "Self-hosted Plainpad deployment via Docker"
---

# Plainpad

Self-hosted Plainpad deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/plainpad/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/plainpad/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/plainpad/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `plainpad` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `2ffc56894b59ab79cf969271df47519956e9b0a2778771082603d4552523d631` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `plainpad` | docker.io/alextselegidis/plainpad:latest | Main application service |
| `plainpad_data` | (volume) | Persistent data storage |

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
| `PLAINPAD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs plainpad
```

**Port conflict:**
Edit `.env` and change `PLAINPAD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec plainpad ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect plainpad --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v plainpad_data:/data -v $(pwd):/backup alpine tar czf /backup/plainpad-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v plainpad_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/plainpad-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Plainpad](https://github.com/alextselegidis/plainpad)
- **Docker Image:** `docker.io/alextselegidis/plainpad:latest`
- **Documentation:** [GitHub Wiki](https://github.com/alextselegidis/plainpad/wiki)
- **Issues:** [GitHub Issues](https://github.com/alextselegidis/plainpad/issues)

