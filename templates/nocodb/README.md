# NocoDB — Open-Source Airtable Alternative

[NocoDB](https://nocodb.com) transforms any database into a smart spreadsheet. It connects to MySQL, PostgreSQL, SQL Server, SQLite, and MariaDB, then layers a no-code interface on top — spreadsheet views, forms, kanban boards, galleries, and calendars — without locking your data behind proprietary formats. Teams use it as a collaborative database that anyone can use, while developers retain full SQL access to the underlying data.

## Project Overview

**Who it's for:** Teams that need a shared database with a friendly UI — project trackers, inventory managers, CRM-lite setups, form-driven workflows — without the cost or vendor lock-in of Airtable/Notion databases.

**Key features:**

- Spreadsheet, kanban, gallery, form, and calendar views
- Role-based access control (owner, creator, viewer, commenter)
- REST API auto-generated for every table
- Webhook support for row-level events
- CSV/Excel import and export
- Connect to existing external databases (MySQL, PostgreSQL, SQLite, SQL Server, MariaDB)
- Audit logs and field-level permissions
- Works with any PostgreSQL-compatible service (Neon, Supabase, CockroachDB)

**This template** deploys NocoDB as a single container with an embedded SQLite database for metadata storage — no external database required for a standalone setup.

## Architecture

```
┌──────────────────────────────────┐
│           nocodb (container)     │
│  image: nocodb/nocodb:latest    │
│  port: 8080                      │
│  data: /data (SQLite metadata)   │
└──────────┬───────────────────────┘
           │
           ▼
    nocodb_data (named volume)
    └── /data/app.db
```

| Component | Description |
|-----------|-------------|
| **nocodb** | The NocoDB application server (Node.js). Serves the web UI and REST API on port 8080. |
| **nocodb_data** | Named Docker volume persisting the SQLite metadata database (`/data/app.db`). Survives container restarts and upgrades. |

No external database is required for a standalone NocoDB deployment. The embedded SQLite file stores NocoDB's own metadata (users, workspaces, views, etc.). Your actual business data can live in an external database that NocoDB connects to at runtime.

## Quick Start

1. **Clone or copy the template files** into a directory:

   ```bash
   mkdir -p nocodb && cd nocodb
   ```

   Copy `docker-compose.yml` and `.env.example` into this directory.

2. **Create your `.env` file:**

   ```bash
   cp .env.example .env
   ```

3. **Start the service:**

   ```bash
   docker compose up -d
   ```

4. **Wait for the health check to pass:**

   ```bash
   docker compose ps
   ```

   The `nocodb` container should show `healthy` within 30–60 seconds.

5. **Access NocoDB:**

   Open [http://localhost:8080](http://localhost:8080) in your browser. The first user to sign up becomes the super admin.

## Configuration Reference

Copy `.env.example` to `.env` and edit as needed.

| Variable | Default | Description |
|----------|---------|-------------|
| `NOCODB_PORT` | `8080` | Host port for the NocoDB web UI and API. Change if 8080 is already in use. |

### Environment-specific overrides

NocoDB supports additional environment variables passed directly to the container. To use them, add an `environment:` block to the `nocodb` service in `docker-compose.yml`:

| Variable | Description | Example |
|----------|-------------|---------|
| `NC_DB` | External database for NocoDB metadata (instead of SQLite). Supports `pg`, `mysql`, `mssql`, `sqlite`. | `pg://host:5432?u=user&p=pass&d=nocodb` |
| `NC_AUTH_JWT_SECRET` | Custom JWT secret for token signing. Auto-generated if not set. | `your-random-secret-string` |
| `NC_PUBLIC_URL` | The public-facing URL where NocoDB is accessible. Used for email links and callbacks. | `https://nocodb.example.com` |
| `NC_ADMIN_EMAIL` | Pre-create a super admin account on first boot. | `admin@example.com` |
| `NC_ADMIN_PASSWORD` | Password for the pre-created admin. Must be set alongside `NC_ADMIN_EMAIL`. | `secure-password-here` |

Example with environment variables added to `docker-compose.yml`:

```yaml
services:
  nocodb:
    image: docker.io/nocodb/nocodb:latest
    environment:
      NC_PUBLIC_URL: "https://nocodb.example.com"
      NC_ADMIN_EMAIL: "admin@example.com"
      NC_ADMIN_PASSWORD: "secure-password-here"
```

## Troubleshooting

### Container starts but health check fails

The health check uses `wget` against `http://localhost:8080/`. NocoDB takes 15–30 seconds to initialize on first boot.

```bash
docker compose logs nocodb
```

Look for `HTTP server started` in the output. If the container is stuck in a restart loop, check for port conflicts.

### Port 8080 is already in use

Change the host port in your `.env` file:

```bash
NOCODB_PORT=3000
```

Then restart:

```bash
docker compose down && docker compose up -d
```

### Lost admin password

If you set `NC_ADMIN_EMAIL` and `NC_ADMIN_PASSWORD`, stop the container, remove the volume (this deletes all metadata), and restart:

```bash
docker compose down
docker volume rm nocodb_data
docker compose up -d
```

**Warning:** This destroys all NocoDB metadata — workspaces, views, and configurations. External database data is unaffected.

### Cannot connect to an external database

When using `NC_DB` to point NocoDB at an external PostgreSQL or MySQL instance:

- Ensure the database exists and the user has `CREATE TABLE` permissions.
- The container must be able to reach the database host. Use `host.docker.internal` for services on the Docker host, or connect both to the same Docker network.
- For PostgreSQL: `NC_DB=pg://db-host:5432?u=nocodb&p=secret&d=nocodb_db`

### Slow performance with large datasets

NocoDB's embedded SQLite metadata store works well for typical use but can bottleneck under heavy concurrent writes. For production workloads with many simultaneous users, switch to PostgreSQL metadata:

```yaml
environment:
  NC_DB: "pg://postgres:5432?u=nocodb&p=secret&d=nocodb_meta"
```

## Backup & Recovery

### What to back up

NocoDB stores its metadata (users, workspaces, views, configurations) in `/data/app.db` inside the container, which maps to the `nocodb_data` named volume. If you connect NocoDB to an external database for your actual tables, that database needs separate backups.

### Backup the metadata volume

**Option 1 — Copy the SQLite file directly:**

```bash
docker compose exec nocodb sqlite3 /data/app.db ".backup /data/backup.db"
docker compose cp nocodb:/data/backup.db ./nocodb-backup-$(date +%Y%m%d).db
```

**Option 2 — Use a volume mount for the backup:**

```bash
docker run --rm \
  -v nocodb_data:/data \
  -v $(pwd):/backup \
  alpine \
  cp /data/app.db /backup/nocodb-backup-$(date +%Y%m%d).db
```

### Restore from backup

1. Stop the container:

   ```bash
   docker compose down
   ```

2. Replace the volume data:

   ```bash
   docker run --rm \
     -v nocodb_data:/data \
     -v $(pwd):/backup \
     alpine \
     cp /backup/nocodb-backup-YYYYMMDD.db /data/app.db
   ```

3. Restart:

   ```bash
   docker compose up -d
   ```

### Automate backups

Add a cron job on the host to back up the volume nightly:

```bash
# /etc/cron.d/nocodb-backup
0 2 * * * root docker run --rm -v nocodb_data:/data -v /backups/nocodb:/backup alpine cp /data/app.db /backup/nocodb-$(date +\%Y\%m\%d).db
```

### Upgrading NocoDB

```bash
docker compose pull nocodb
docker compose down
docker compose up -d
```

The volume persists across upgrades. NocoDB runs migrations automatically on startup. Always back up before upgrading major versions.

## Links

- **Source code:** [github.com/nocodb/nocodb](https://github.com/nocodb/nocodb)
- **Documentation:** [docs.nocodb.com](https://docs.nocodb.com)
- **Docker Hub:** [hub.docker.com/r/nocodb/nocodb](https://hub.docker.com/r/nocodb/nocodb)
- **Community:** [NocoDB Discord](https://discord.gg/5RgZmkW)
- **API reference:** [docs.nocodb.com/developer-resources/api-access-tokens](https://docs.nocodb.com/developer-resources/api-access-tokens)
- **Changelog:** [github.com/nocodb/nocodb/releases](https://github.com/nocodb/nocodb/releases)
