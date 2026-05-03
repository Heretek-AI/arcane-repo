# AFFiNE — Knowledge Base & Document Workspace

[AFFiNE](https://github.com/toeverything/AFFiNE) is an open-source, local-first knowledge base and document workspace that combines docs, whiteboards, and databases into a single canvas. Think Notion meets Miro — but self-hosted and privacy-respecting. Write documents, sketch ideas on an infinite whiteboard, organize tasks with kanban boards, and collaborate in real time.

This template runs the official AFFiNE all-in-one Docker image with persistent data storage and a health check.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access AFFiNE:**

   Open [http://localhost:8080](http://localhost:8080) in your browser. On first launch you'll be prompted to create an account and workspace.

4. **Verify the service is healthy:**

   ```bash
   curl -s http://localhost:8080/ | head -5
   ```

   A successful response returns the AFFiNE web app HTML.

## Architecture

This template runs a single AFFiNE container that bundles the server, web client, and embedded database.

| Component     | Image                                  | Port  | Description                          |
|---------------|----------------------------------------|-------|--------------------------------------|
| `affine`      | `affinefoundation/affine:latest`       | 8080  | AFFiNE all-in-one server and web UI  |

### Volume

| Volume        | Mount Point | Content                                    |
|---------------|-------------|--------------------------------------------|
| `affine_data` | `/data`     | Database files, uploaded blobs, config     |

### Health Check

The container includes a built-in health check that probes `http://localhost:8080/` every 30 seconds. The service is marked healthy after 3 consecutive successful checks. On startup, it waits 30 seconds before the first probe to allow initialization to complete.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable      | Default | Description                                              |
|---------------|---------|----------------------------------------------------------|
| `AFFINE_PORT` | `8080`  | Host port for the AFFiNE web interface and API           |

### Changing the Port

To run AFFiNE on a different port (e.g., 9090):

```bash
# In .env
AFFINE_PORT=9090
```

Then restart:

```bash
docker compose up -d
```

AFFiNE will be available at `http://localhost:9090`.

## Features

AFFiNE is a full-featured workspace — here's what you get out of the box:

- **Documents** — Block-based editor with markdown support, slash commands, and rich content blocks
- **Whiteboards** — Infinite canvas for sketching, diagramming, and visual brainstorming
- **Databases** — Kanban boards, tables, and galleries built from structured data blocks
- **Collections** — Group and organize pages across your workspace
- **Real-time Collaboration** — Multiple users editing simultaneously (requires configuring a shared backend)
- **Local-first** — Data stored on your server, accessible even offline via the desktop/mobile apps
- **Templates** — Pre-built templates for common workflows
- **Cross-platform** — Web, desktop (Windows/macOS/Linux), iOS, and Android clients

## Managing the Service

**View logs:**

```bash
docker compose logs -f affine
```

**Restart:**

```bash
docker compose restart affine
```

**Stop:**

```bash
docker compose down
```

**Apply environment variable changes:**

```bash
docker compose up -d
```

This recreates the container with updated configuration.

## Upgrading

To upgrade AFFiNE to the latest version:

```bash
# Pull the latest image
docker compose pull

# Recreate the container
docker compose up -d
```

Check the [AFFiNE releases](https://github.com/toeverything/AFFiNE/releases) for changelog and migration notes between versions. The embedded database handles schema migrations automatically on startup.

## Backup & Recovery

### What to Back Up

The `affine_data` Docker volume contains everything — database, uploaded files, and configuration. Back up this single volume to capture your entire AFFiNE instance.

### Backup

**Volume-level backup (recommended):**

```bash
docker run --rm \
  -v affine_data:/source:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/affine-backup-$(date +%Y%m%d).tar.gz -C /source .
```

This creates a timestamped archive in your current directory.

**Verify the backup:**

```bash
tar tzf affine-backup-*.tar.gz | head -20
```

### Restore

1. **Stop the service:**

   ```bash
   docker compose down
   ```

2. **Restore the volume data:**

   ```bash
   docker run --rm \
     -v affine_data:/target \
     -v $(pwd):/backup \
     alpine sh -c "rm -rf /target/* && tar xzf /backup/affine-backup-YYYYMMDD.tar.gz -C /target"
   ```

   Replace `YYYYMMDD` with your backup date.

3. **Restart the service:**

   ```bash
   docker compose up -d
   ```

### Automated Backups

For scheduled backups, add a cron job:

```bash
# Back up daily at 2am, keep last 7 days
0 2 * * * cd /path/to/affine && docker run --rm -v affine_data:/source:ro -v $(pwd)/backups:/backup alpine tar czf /backup/affine-$(date +\%Y\%m\%d).tar.gz -C /source . && find backups -mtime +7 -delete
```

## Troubleshooting

| Symptom                          | Likely Cause                              | Fix                                                        |
|----------------------------------|-------------------------------------------|------------------------------------------------------------|
| Container won't start            | Port 8080 already in use                   | Change `AFFINE_PORT` in `.env` to a free port              |
| Health check shows unhealthy     | AFFiNE still initializing (first boot)     | Wait 60–90 seconds — first startup runs migrations         |
| "502 Bad Gateway" via reverse proxy | AFFiNE not yet ready                     | Wait for health check to pass, or increase proxy timeout   |
| Pages not saving                 | Volume not mounted or disk full            | Verify `affine_data` volume exists: `docker volume ls`     |
| Slow performance                 | Insufficient RAM                           | AFFiNE recommends at least 2 GB RAM for comfortable use    |
| Can't access from another device | Firewall blocking the port                 | Open the configured port in your firewall                  |
| Data lost after recreate         | Volume was removed                         | Never run `docker volume rm affine_data` unless intentionally resetting |

## Links

- **Original Project:** [github.com/toeverything/AFFiNE](https://github.com/toeverything/AFFiNE)
- **Documentation:** [docs.affine.pro](https://docs.affine.pro)
- **Self-hosting Guide:** [docs.affine.pro/self-host-affine](https://docs.affine.pro/docs/self-host-affine)
- **Docker Hub:** [hub.docker.com/r/affinefoundation/affine](https://hub.docker.com/r/affinefoundation/affine)
- **Community (Discord):** [affine.pro/community](https://affine.pro/community)
- **Releases:** [github.com/toeverything/AFFiNE/releases](https://github.com/toeverything/AFFiNE/releases)
