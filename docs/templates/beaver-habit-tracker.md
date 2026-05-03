---
title: "Beaver Habit Tracker"
description: "Self-hosted habit tracking application that helps you build and maintain daily habits with a clean, minimal interface."
---

# Beaver Habit Tracker

Self-hosted habit tracking application that helps you build and maintain daily habits with a clean, minimal interface.

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/beaver-habit-tracker/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/beaver-habit-tracker/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/beaver-habit-tracker/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `beaver-habit-tracker` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ead373c7b011f5889fe4214dafae9d77f8016c49ac3afdba5582f0f2d42d0d6d` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `beaver-habit-tracker` | docker.io/daya0576/beaverhabits:latest | Main application service |
| `beaver-habit-tracker_data` | (volume) | Persistent data storage |

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
| `BEAVER_HABIT_TRACKER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs beaver-habit-tracker
```

**Port conflict:**
Edit `.env` and change `BEAVER-HABIT-TRACKER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec beaver-habit-tracker ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect beaver-habit-tracker --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v beaver-habit-tracker_data:/data -v $(pwd):/backup alpine tar czf /backup/beaver-habit-tracker-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v beaver-habit-tracker_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/beaver-habit-tracker-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Beaver Habit Tracker](https://github.com/daya0576/beaverhabits)
- **Docker Image:** `docker.io/daya0576/beaverhabits:latest`
- **Documentation:** [GitHub Wiki](https://github.com/daya0576/beaverhabits/wiki)
- **Issues:** [GitHub Issues](https://github.com/daya0576/beaverhabits/issues)

