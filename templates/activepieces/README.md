# Activepieces — Open-Source Workflow Automation

[Activepieces](https://www.activepieces.com) is an open-source workflow automation platform with 400+ app integrations, a visual drag-and-drop editor, and built-in AI agent capabilities. It's a self-hosted alternative to Zapier, Make, and n8n — designed for teams that want full control over their automation infrastructure and data.

This template runs Activepieces as a single container with embedded SQLite storage — no external database required.

## Quick Start

1. **Start Activepieces:**

   ```bash
   docker compose up -d
   ```

2. **Access the UI:**

   Open [http://localhost:8080](http://localhost:8080) in your browser.

3. **Create your account:**

   On first launch you'll be prompted to create an admin account. This account owns the workspace and all flows.

4. **Verify the service:**

   ```bash
   curl -s http://localhost:8080/ | head -c 200
   ```

   A successful response returns HTML for the Activepieces frontend.

## Architecture

| Component         | Description                                                      |
|-------------------|------------------------------------------------------------------|
| `activepieces`    | The Activepieces application server — serves the UI, API, flow engine, and webhook receiver all in one container. |
| `activepieces_data` | Named Docker volume mounted at `/data` — stores the SQLite database, flow state, and uploaded files. |

The stack is a single service with no external dependencies. Activepieces uses an embedded SQLite database stored in the `activepieces_data` volume, so there's no PostgreSQL or Redis to manage.

## Configuration

Copy `.env.example` to `.env` and edit:

```bash
cp .env.example .env
```

### Environment Variables

| Variable            | Default  | Description                              |
|---------------------|----------|------------------------------------------|
| `ACTIVEPIECES_PORT` | `8080`   | Host port for the Activepieces web UI and API. |

## Adding Environment Variables

Activepieces supports additional environment variables for production deployments. You can add these to your `.env` file and reference them in `docker-compose.yml`:

| Variable                  | Description                                                       |
|---------------------------|-------------------------------------------------------------------|
| `AP_ENGINE_EXECUTABLE_PATH` | Custom path to the flow engine executable (rarely needed)       |
| `AP_ENCRYPTION_KEY`       | Encryption key for sensitive data (credentials, connections). **Set this before first run in production** — changing it later makes existing encrypted data unreadable. Generate with `openssl rand -hex 32`. |
| `AP_JWT_SECRET`           | JWT signing secret. **Set this before first run in production** — changing it invalidates all active sessions. Generate with `openssl rand -hex 32`. |
| `AP_WEBHOOK_URL`          | Public URL for webhook callbacks (e.g., `https://activepieces.example.com`). Required if you're behind a reverse proxy. |
| `AP_POSTGRES_DATABASE`    | PostgreSQL database name (for external DB migration — see below). |
| `AP_POSTGRES_HOST`        | PostgreSQL host (for external DB migration — see below).          |
| `AP_POSTGRES_PORT`        | PostgreSQL port (default: `5432`).                                |
| `AP_POSTGRES_USERNAME`    | PostgreSQL username.                                              |
| `AP_POSTGRES_PASSWORD`    | PostgreSQL password.                                              |
| `AP_REDIS_URL`            | Redis URL (e.g., `redis://redis:6379`). For queue management in high-traffic deployments. |

To pass these through, add them to your `.env` and add an `environment:` block to `docker-compose.yml`:

```yaml
services:
  activepieces:
    environment:
      - AP_ENCRYPTION_KEY=${AP_ENCRYPTION_KEY}
      - AP_JWT_SECRET=${AP_JWT_SECRET}
      - AP_WEBHOOK_URL=${AP_WEBHOOK_URL}
```

## Health Check

The container includes a built-in health check that pings `http://localhost:8080/` every 30 seconds. Check status with:

```bash
docker compose ps
```

A healthy container shows `(healthy)` in the status column. You can also verify manually:

```bash
curl -sf http://localhost:8080/ > /dev/null && echo "healthy" || echo "unhealthy"
```

## Webhooks

Activepieces flows can be triggered via incoming webhooks. Each flow with a webhook trigger gets a unique URL like:

```
http://localhost:8080/api/v1/webhooks/<flow-id>
```

If you're running behind a reverse proxy or need public webhook access, set `AP_WEBHOOK_URL` to your public domain (e.g., `https://activepieces.example.com`) so generated webhook URLs point to the correct external address.

## Upgrading

```bash
# Pull the latest image
docker compose pull

# Recreate the container
docker compose up -d
```

Activepieces runs automatic database migrations on startup. Check the [Activepieces changelog](https://github.com/activepieces/activepieces/releases) for breaking changes between major versions before upgrading.

## Troubleshooting

| Symptom                                  | Likely Cause                                  | Fix                                                       |
|------------------------------------------|-----------------------------------------------|-----------------------------------------------------------|
| Port 8080 already in use                 | Another service occupies the port             | Change `ACTIVEPIECES_PORT` in `.env` to a free port        |
| Container shows `unhealthy` immediately  | Still starting up — health check has 30s grace| Wait 30–60 seconds, then re-check with `docker compose ps` |
| Flows fail after encryption key change   | `AP_ENCRYPTION_KEY` changed between runs      | Restore the original key — encrypted credentials are lost otherwise |
| Session invalidation after restart       | `AP_JWT_SECRET` not set or changed            | Set a fixed `AP_JWT_SECRET` in `.env` before first run     |
| Webhooks return 404                      | Flow not published or webhook URL mismatch    | Publish the flow and verify `AP_WEBHOOK_URL` matches your public address |
| Slow flow execution                      | SQLite under heavy load                       | Migrate to PostgreSQL for production traffic (see Activepieces docs) |

## Backup & Recovery

### Backup

All persistent data lives in the `activepieces_data` volume. Back it up with:

```bash
# Stop the container to ensure consistent state
docker compose stop activepieces

# Create a backup archive
docker run --rm \
  -v activepieces_data:/source:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/activepieces-backup-$(date +%Y%m%d).tar.gz -C /source .

# Restart the container
docker compose start activepieces
```

### Restore

```bash
# Stop the container
docker compose stop activepieces

# Restore from backup
docker run --rm \
  -v activepieces_data:/target \
  -v $(pwd):/backup \
  alpine sh -c "rm -rf /target/* && tar xzf /backup/activepieces-backup-YYYYMMDD.tar.gz -C /target"

# Restart the container
docker compose start activepieces
```

Replace `YYYYMMDD` with the actual backup date.

### Production Recommendation

For production workflows with meaningful automation volume, consider migrating to an external PostgreSQL database. This gives you point-in-time recovery, replication, and better concurrency. See the [Activepieces documentation](https://www.activepieces.com/docs) for migration instructions.

## Links

- **Original project:** [github.com/activepieces/activepieces](https://github.com/activepieces/activepieces)
- **Documentation:** [activepieces.com/docs](https://www.activepieces.com/docs)
- **Community:** [community.activepieces.com](https://community.activepieces.com)
- **Docker image:** [ghcr.io/activepieces/activepieces](https://ghcr.io/activepieces/activepieces)
