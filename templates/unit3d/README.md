# UNIT3D

[UNIT3D](https://github.com/HDInnovations/UNIT3D-Community-Edition) — Self-hosted private torrent tracker built with Laravel, Livewire, and AlpineJS. Features Gazelle-inspired layouts, automated moderation, and a modern responsive UI.

## Quick Start

1. **Copy the environment file & set the app key:**

   ```bash
   cp .env.example .env
   # Generate a secure APP_KEY (required — container won't start without it):
   sed -i "s/^APP_KEY=$/APP_KEY=$(head -c 32 \/dev\/urandom | base64)/" .env
   ```

2. **Start the platform:**

   ```bash
   docker compose up -d
   ```

   Wait ~60 seconds for Laravel to run database migrations, cache config, and compile views. The `unit3d` container depends on MySQL, Redis, and Meilisearch health checks before starting.

3. **Create an admin account:**

   ```bash
   docker compose exec unit3d php artisan db:seed --class=OwnerUserSeeder
   ```

   Default credentials are seeded from the UNIT3D defaults. Change the password immediately after first login.

4. **Access the tracker:**

   Open [http://localhost](http://localhost) and log in.

## Architecture

| Service | Image | Port | Purpose |
|---|---|---|---|
| `mysql` | `mysql:8` | — | Relational database (users, torrents, peers, categories) |
| `redis` | `redis:7-alpine` | — | Cache, session storage, queue backend |
| `meilisearch` | `getmeili/meilisearch:v1.12` | — | Full-text torrent search engine |
| `unit3d` | `ghcr.io/heretek-ai/arcane-repo/unit3d:latest` | 80 | Laravel app (PHP-FPM + nginx via supervisord) |

All four services use health checks with `condition: service_healthy` dependency cascading — the `unit3d` container waits for MySQL, Redis, and Meilisearch to be healthy before starting.

## Configuration

Copy `.env.example` to `.env` and edit the values.

### Required

| Variable | Description |
|---|---|
| `APP_KEY` | Laravel encryption key (32 bytes, base64-encoded). **Container refuses to start without this.** |
| `DB_PASSWORD` | MySQL password for the `unit3d` database user |
| `MYSQL_ROOT_PASSWORD` | MySQL root password (used for healthcheck) |

### Optional

| Variable | Default | Description |
|---|---|---|
| `APP_URL` | `http://localhost` | Public URL for asset generation and redirects |
| `DB_DATABASE` | `unit3d` | MySQL database name |
| `DB_USERNAME` | `unit3d` | MySQL user name |
| `MEILISEARCH_KEY` | `unit3d-meili-master-key` | Meilisearch master key (must match between app and search service) |
| `UNIT3D_PORT` | `80` | Host port for the web UI |

## Service Details

### Meilisearch

UNIT3D uses Meilisearch for fast torrent search. The search index is populated automatically during Laravel's database seed. If you add torrents before Meilisearch is healthy, run:

```bash
docker compose exec unit3d php artisan scout:import "App\Models\Torrent"
```

### Redis

Redis serves three roles: cache driver, session store, and queue backend. All configured via environment variables in the compose file. No additional setup required.

### MySQL

The MySQL 8 container initializes the database on first start. The `unit3d` database and user are created automatically from the environment variables. Migrations run when the app container starts.

## Post-Install Steps

- [ ] Log in and change the default admin password
- [ ] Configure site name, description, and upload rules via the admin panel
- [ ] Set up a reverse proxy (nginx/caddy) with TLS for production use
- [ ] Configure announce URLs in tracker settings
- [ ] Schedule database backups

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Container `unit3d-app` exits immediately | Missing `APP_KEY` | Generate one: `head -c 32 /dev/urandom \| base64` and set in `.env` |
| `SQLSTATE[HY000]` connection refused | MySQL not ready | Wait for MySQL healthcheck to pass; check `DB_PASSWORD` matches `MYSQL_ROOT_PASSWORD` setup |
| Search returns no results | Meilisearch not indexed | Run `php artisan scout:import "App\Models\Torrent"` inside the app container |
| 500 errors on pages | Redis connection failed | Check `redis` container health; verify `REDIS_HOST=redis` in compose environment |
| Meilisearch healthcheck fails | Port conflict or slow start | Increase `start_period` in compose; check `MEILISEARCH_KEY` is set |

## Upstream

- [GitHub Repository](https://github.com/HDInnovations/UNIT3D-Community-Edition)
- [Documentation](https://github.com/HDInnovations/UNIT3D-Community-Edition/wiki)
