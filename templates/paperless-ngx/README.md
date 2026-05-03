# Paperless-ngx — Document Management System

[Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) is a self-hosted document management system that replaces physical paper archives. It scans, indexes, and archives your documents with full-text search, automatic tagging, and OCR — making every piece of paper searchable from a web browser.

This template deploys a single Paperless-ngx container with persistent data storage. For most home and small-office setups, the default configuration works out of the box.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access Paperless-ngx:**

   Open [http://localhost:8000](http://localhost:8000) in your browser. On first launch you'll be prompted to create an admin account.

4. **Verify the service is healthy:**

   ```bash
   curl -s http://localhost:8000/ | head -c 200
   ```

   A healthy instance returns the login page HTML.

## Architecture

This is a single-service template. Paperless-ngx bundles its own database (SQLite by default) and document storage inside the container volume.

```
┌──────────────────────────────────────────┐
│  paperless-ngx                           │
│  ghcr.io/paperless-ngx/paperless-ngx     │
│                                          │
│  ┌──────────┐  ┌──────────┐             │
│  │  SQLite   │  │  Media   │             │
│  │  (index)  │  │ (docs)   │             │
│  └────┬─────┘  └────┬─────┘             │
│       └──────┬───────┘                   │
│              ▼                           │
│       /data  (volume)                    │
└──────────────┬───────────────────────────┘
               │
               ▼
         Host port 8000
```

| Component      | Details                                                     |
|----------------|-------------------------------------------------------------|
| **Image**      | `ghcr.io/paperless-ngx/paperless-ngx:latest`                |
| **Port**       | `8000` (configurable via `PAPERLESS_NGX_PORT`)              |
| **Volume**     | `paperless-ngx_data` → `/data` (documents, database, media) |
| **Restart**    | `unless-stopped`                                            |
| **Health**     | wget probe to `http://localhost:8000/` every 30s            |

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable            | Default | Description                                              |
|---------------------|---------|----------------------------------------------------------|
| `PAPERLESS_NGX_PORT`| `8000`  | Host port for the Paperless-ngx web interface and API    |

### Advanced Configuration

Paperless-ngx supports many environment variables for customization. Add these to your `docker-compose.yml` under the `environment:` key or to your `.env` file. See the [full reference](https://docs.paperless-ngx.com/configuration/#docker).

| Variable                           | Default         | Description                                              |
|------------------------------------|-----------------|----------------------------------------------------------|
| `PAPERLESS_TIME_ZONE`             | `UTC`           | Your timezone (e.g. `America/New_York`)                 |
| `PAPERLESS_OCR_LANGUAGE`          | `eng`           | OCR language — use `deu`, `fra`, `spa`, etc.            |
| `PAPERLESS_SECRET_KEY`            | *(auto)*        | Django secret key — set a fixed value to persist sessions across restarts |
| `PAPERLESS_URL`                   | *(empty)*       | Public URL if behind a reverse proxy (e.g. `https://paperless.example.com`) |
| `PAPERLESS_ALLOWED_HOSTS`         | `*`             | Comma-separated list of allowed hostnames               |
| `PAPERLESS_CSRF_TRUSTED_ORIGINS`  | *(empty)*       | CSRF-trusted origins for reverse proxy setups            |
| `PAPERLESS_ADMIN_USER`            | *(empty)*       | Auto-create admin on first launch                        |
| `PAPERLESS_ADMIN_PASSWORD`        | *(empty)*       | Password for the auto-created admin                      |
| `PAPERLESS_ADMIN_MAIL`            | *(empty)*       | Email for the auto-created admin                         |
| `PAPERLESS_CONSUMER_IGNORE_DATES` | `false`         | Ignore dates in filenames during import                  |

## Health Check

The container includes a built-in health check that probes `http://localhost:8000/` every 30 seconds.

```bash
# Check container health status
docker inspect --format='{{.State.Health.Status}}' paperless-ngx

# View health check logs
docker inspect --format='{{json .State.Health}}' paperless-ngx | jq .
```

## Troubleshooting

| Symptom                              | Likely Cause                                  | Fix                                                       |
|--------------------------------------|-----------------------------------------------|-----------------------------------------------------------|
| Container won't start                | Port 8000 already in use                      | Change `PAPERLESS_NGX_PORT` in `.env` and restart         |
| Health check shows `unhealthy`       | Container still initializing (first boot)     | Wait 30–60 seconds — OCR setup takes time on first run   |
| Documents fail to process            | OCR language not installed                    | Set `PAPERLESS_OCR_LANGUAGE` to an installed language     |
| Login page shows but can't log in    | Lost admin credentials                        | Create a new superuser: `docker compose exec paperless-ngx document_exporter createsuperuser` |
| "Bad Request (400)" behind proxy     | `PAPERLESS_URL` or CSRF origins not set       | Set `PAPERLESS_URL` and `PAPERLESS_CSRF_TRUSTED_ORIGINS` to your public URL |
| Slow document processing             | Insufficient CPU/RAM for OCR                  | Increase container resource limits or reduce OCR DPI      |
| Volume permissions errors            | UID/GID mismatch                              | Set `USERMAP_UID` and `USERMAP_GID` to match host user   |

### Viewing Logs

```bash
# Tail live logs
docker compose logs -f paperless-ngx

# Last 100 lines
docker compose logs --tail 100 paperless-ngx
```

## Backup & Recovery

All persistent data lives in the `paperless-ngx_data` volume, which is mounted at `/data` inside the container. This includes:

- **Documents** — the actual PDF/image files
- **SQLite database** — metadata, tags, correspondents, and full-text index
- **Media files** — thumbnails and previews

### Backup

```bash
# Stop the container to ensure consistency
docker compose stop paperless-ngx

# Backup the volume
docker run --rm \
  -v paperless-ngx_data:/source:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/paperless-ngx-backup-$(date +%Y%m%d).tar.gz -C /source .

# Restart
docker compose up -d
```

### Restore

```bash
# Stop the container
docker compose stop paperless-ngx

# Restore the volume
docker run --rm \
  -v paperless-ngx_data:/target \
  -v $(pwd):/backup \
  alpine sh -c "rm -rf /target/* && tar xzf /backup/paperless-ngx-backup-YYYYMMDD.tar.gz -C /target"

# Restart
docker compose up -d
```

### Automated Backup

For scheduled backups without downtime, use Paperless-ngx's built-in exporter:

```bash
# Export all documents and metadata
docker compose exec paperless-ngx document_exporter ../export
```

## Upgrading

```bash
# Pull the latest image
docker compose pull

# Recreate the container
docker compose up -d

# Verify health
docker inspect --format='{{.State.Health.Status}}' paperless-ngx
```

Check the [Paperless-ngx release notes](https://github.com/paperless-ngx/paperless-ngx/releases) before upgrading — major versions may include database migrations that run automatically on startup.

## Links

- **Original Project:** [github.com/paperless-ngx/paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)
- **Documentation:** [docs.paperless-ngx.com](https://docs.paperless-ngx.com)
- **Docker Hub:** [ghcr.io/paperless-ngx/paperless-ngx](https://ghcr.io/paperless-ngx/paperless-ngx)
- **Community:** [GitHub Discussions](https://github.com/paperless-ngx/paperless-ngx/discussions)
- **Configuration Reference:** [docs.paperless-ngx.com/configuration](https://docs.paperless-ngx.com/configuration/#docker)
