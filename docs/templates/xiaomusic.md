---
title: "Xiaomusic"
description: "Xiaomi smart speaker music player with LLM integration — control your Xiaomi speaker with natural language music requests. Custom-build from hanxi/xiaomusic source"
---

# Xiaomusic

Xiaomi smart speaker music player with LLM integration — control your Xiaomi speaker with natural language music requests. Custom-build from hanxi/xiaomusic source

## Tags

<a href="/categories/llm" class="tag-badge">llm</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/xiaomusic/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/xiaomusic/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/xiaomusic/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `xiaomusic` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `574366359d4db4100bbc1a8083afa096255f67eb894e18fae7817708252e1def` |

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and set your Xiaomi credentials:**

   - `XIAOMUSIC_MI_USER` — Xiaomi account ID
   - `XIAOMUSIC_MI_PASSWORD` — Xiaomi account password
   - `XIAOMUSIC_MI_DID` — device ID (find in Mi Home app)
   - `XIAOMUSIC_MI_HARDWARE` — hardware model

3. **Start the service:**

   ```bash
   docker compose up -d
   ```

4. **Access the web UI:**

   Open [http://localhost:8090](http://localhost:8090) in your browser.

   > **Build:** This is a custom-build template — the Docker image is built
   > from source and hosted on GHCR
   > (`ghcr.io/heretek-ai/arcane-repo/xiaomusic:latest`).
   > No pre-built public image exists upstream.

## Configuration

| Variable                  | Default     | Description                              |
|---------------------------|-------------|------------------------------------------|
| `XIAOMUSIC_MI_USER`       | *(required)* | Xiaomi account ID                        |
| `XIAOMUSIC_MI_PASSWORD`   | *(required)* | Xiaomi account password                  |
| `XIAOMUSIC_MI_DID`        | *(required)* | Device ID from Mi Home                   |
| `XIAOMUSIC_MI_HARDWARE`   | *(required)* | Hardware model identifier                |
| `XIAOMUSIC_WEB_PORT`      | `8090`      | Web UI port                              |
| `XIAOMUSIC_HEALTH_PORT`   | `8091`      | Health check API port                    |
| `TZ`                      | `Asia/Shanghai` | Timezone                            |
| `XIAOMUSIC_CONF_DIR`      | `./conf`    | Configuration directory                  |
| `XIAOMUSIC_MUSIC_DIR`     | `./music`   | Music files directory                    |

## Troubleshooting

| Symptom | Likely Cause | Fix |
|----------|-------------|-----|
| `docker compose up` fails | Image not yet built/pulled | Run `docker compose build` to build locally |
| Cannot connect to speaker | Wrong credentials | Verify Xiaomi account ID and password in `.env` |
| Device not found | Wrong DID/hardware | Check device info in Mi Home app |
| Port conflict | Another service on port 8090 | Change `XIAOMUSIC_WEB_PORT` in `.env` |
| Container exits immediately | Build failure | Run `docker compose logs xiaomusic` for details |

## Service Details

Xiaomusic connects to your Xiaomi smart speaker and enables natural language
music control via LLM integration. You can request songs, playlists, and
radio by speaking or typing.

Volumes:
- `/app/conf` — configuration files
- `/app/music` — local music library

