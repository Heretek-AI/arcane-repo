---
title: "Your Spotify"
description: "Self-hosted Your Spotify deployment via Docker"
---

# Your Spotify

Self-hosted Your Spotify deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/your-spotify/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/your-spotify/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/your-spotify/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `your-spotify` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c6969a302f3f933661fe8246e0850d0c4846e66a26f53d24bdb779adef68ac4f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `your-spotify` | ghcr.io/linuxserver/your_spotify:latest | Main application service |
| `your-spotify_data` | (volume) | Persistent data storage |

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
| `YOUR_SPOTIFY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs your-spotify
```

**Port conflict:**
Edit `.env` and change `YOUR-SPOTIFY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec your-spotify ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect your-spotify --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v your-spotify_data:/data -v $(pwd):/backup alpine tar czf /backup/your-spotify-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v your-spotify_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/your-spotify-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Your Spotify](https://github.com/linuxserver/your_spotify)
- **Docker Image:** `ghcr.io/linuxserver/your_spotify:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/your_spotify/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/your_spotify/issues)

