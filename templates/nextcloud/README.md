# Nextcloud

Self-hosted content collaboration platform with file sync, calendar, contacts, and an extensive app ecosystem. Nextcloud gives you control over your data — files, photos, documents, and communication stay on your infrastructure.

## Project Overview

**Nextcloud** is the most deployed self-hosted file sync and content collaboration platform. It provides:

- **File sync & share** — sync files across devices, share with links or federated users
- **Calendar & contacts** — CalDAV/CardDAV server replacing Google Calendar/Contacts
- **Office suite** — collaborative document editing via Collabora Online or OnlyOffice integration
- **Talk** — video conferencing, screen sharing, and chat
- **Mobile & desktop clients** — native apps for iOS, Android, Windows, macOS, and Linux
- **App ecosystem** — 300+ apps for notes, kanban, passwords, mail, media, and more

This template deploys Nextcloud as a single container using the official Docker image with a persistent data volume.

### Who it's for

Individuals, families, and small teams who want to replace Google Drive/iCloud/Dropbox with something they control. Works well as a personal cloud, a family file server, or a small-team collaboration hub.

## Architecture

```
┌─────────────────────────────────┐
│           nextcloud             │
│  (library/nextcloud:latest)     │
│                                 │
│  Port: ${NEXTCLOUD_PORT:-80}    │
│                                 │
│  ┌───────────────────────────┐  │
│  │     /data (volume)        │  │
│  │     nextcloud_data        │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

### Services

| Service | Image | Purpose |
|---------|-------|---------|
| `nextcloud` | `library/nextcloud:latest` | Web server, file storage, and application runtime |

### Volumes

| Volume | Mount | Purpose |
|--------|-------|---------|
| `nextcloud_data` | `/data` | All user files, database (SQLite by default), config, and app data |

### Health Check

The container includes a health check that probes `http://localhost:80/` every 30 seconds with a 60-second startup grace period. The container is marked healthy once Nextcloud responds to HTTP requests.

## Quick Start

1. **Clone or navigate to the template directory:**

   ```bash
   cd templates/nextcloud
   ```

2. **Create your environment file:**

   ```bash
   cp .env.example .env
   ```

3. **Start the stack:**

   ```bash
   docker compose up -d
   ```

4. **Complete the setup wizard:**

   Open `http://localhost` (or your configured port) in a browser. On first launch, Nextcloud walks you through:
   - Creating an admin account
   - Choosing a database (SQLite is pre-selected for simplicity)

5. **Install clients:**

   Download desktop and mobile clients from [nextcloud.com/install](https://nextcloud.com/install/#clients) and point them at your server URL.

## Configuration Reference

All variables are set in your `.env` file (copied from `.env.example`).

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXTCLOUD_PORT` | `80` | Host port exposed for the Nextcloud web interface. Change if port 80 is in use on your host. |

### Additional environment variables

The official Nextcloud image supports many more environment variables for advanced setups. You can add these directly to the `docker-compose.yml` under the `environment:` key or in your `.env` file:

| Variable | Purpose |
|----------|---------|
| `NEXTCLOUD_ADMIN_USER` | Auto-create admin user on first start (skip setup wizard) |
| `NEXTCLOUD_ADMIN_PASSWORD` | Password for the auto-created admin user |
| `NEXTCLOUD_TRUSTED_DOMAINS` | Space-separated list of domains/IPs allowed to access the instance |

Example — adding trusted domains and auto-provisioning an admin:

```yaml
# In docker-compose.yml, add under the nextcloud service:
environment:
  - NEXTCLOUD_ADMIN_USER=admin
  - NEXTCLOUD_ADMIN_PASSWORD=changeme
  - NEXTCLOUD_TRUSTED_DOMAINS=cloud.example.com 192.168.1.100
```

### Upgrading to a production database

By default, Nextcloud uses SQLite (fine for personal use). For teams or heavy usage, add PostgreSQL or MariaDB as a companion service. See the [Nextcloud Docker documentation](https://github.com/docker-library/docs/blob/master/nextcloud/README.md) for multi-service compose examples.

## Troubleshooting

### First-load is slow

Nextcloud runs database migrations and index jobs on first access. Give it 1–2 minutes after the health check passes.

### "Trusted domain" error after login

If you access Nextcloud from an IP or hostname not in its trusted domains list, you'll see a security warning. Fix by either:

1. Setting `NEXTCLOUD_TRUSTED_DOMAINS` in your environment, or
2. Editing `config/config.php` inside the container and adding your domain to the `trusted_domains` array:

   ```bash
   docker exec -it nextcloud php occ config:system:set trusted_domains 1 --value="your.domain.com"
   ```

### Permission errors on the data volume

The Nextcloud container runs as `www-data` (UID 33). If you mount a host directory instead of a named volume, ensure the host path is owned by UID 33:

```bash
sudo chown -R 33:33 /path/to/host/data
```

### Health check failing

Check container logs:

```bash
docker compose logs nextcloud
```

Common causes: port conflict on the host, or Nextcloud still initializing after first start (the 60-second `start_period` should cover this).

### Resetting the admin password

```bash
docker exec -it nextcloud php occ user:resetpassword admin
```

## Backup & Recovery

### What to back up

The `nextcloud_data` named volume contains everything: user files, SQLite database, configuration, and installed apps.

### Backup

```bash
# Stop the container to ensure data consistency
docker compose stop nextcloud

# Back up the volume
docker run --rm -v nextcloud_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/nextcloud-backup-$(date +%Y%m%d).tar.gz -C /data .

# Restart
docker compose start nextcloud
```

### Restore

```bash
# Stop the container
docker compose stop nextcloud

# Restore from backup
docker run --rm -v nextcloud_data:/data -v $(pwd):/backup alpine \
  sh -c "rm -rf /data/* && tar xzf /backup/nextcloud-backup-YYYYMMDD.tar.gz -C /data"

# Restart
docker compose start nextcloud
```

### Automated backups

Add the backup command to a cron job on the host. Run it daily during low-traffic hours. For production setups using PostgreSQL or MariaDB, use `pg_dump` or `mysqldump` before the file-level backup.

## Links

- **Source code:** [github.com/nextcloud/server](https://github.com/nextcloud/server)
- **Official docs:** [docs.nextcloud.com](https://docs.nextcloud.com/)
- **Docker Hub:** [hub.docker.com/_/nextcloud](https://hub.docker.com/_/nextcloud)
- **App store:** [apps.nextcloud.com](https://apps.nextcloud.com/)
- **Community forum:** [help.nextcloud.com](https://help.nextcloud.com/)
- **Desktop & mobile clients:** [nextcloud.com/install](https://nextcloud.com/install/#clients)
