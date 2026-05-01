# Laradock

[Laradock](https://github.com/laradock/laradock) (12,667★) — Docker-based PHP development environment, **simplified here for deployment**.

> **⚠️ Important:** This template provides a simplified production-ready deployment (nginx + php-fpm + mysql + redis). It is NOT the full Laradock development environment. The upstream project offers 80+ optional containers for local development (workspace, Horizon, Mailpit, Selenium, etc.). This template ships the minimal core stack suitable for Docker Compose deployment of Laravel/PHP applications.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` to set secure database credentials:**

   ```ini
   MYSQL_ROOT_PASSWORD=your-secure-root-password
   MYSQL_PASSWORD=your-secure-user-password
   ```

3. **Place your PHP application code in a volume-mounted directory** or update `laradock_app` volume to bind-mount your project:

   ```bash
   docker compose up -d
   ```

4. **Access your app:**

   Open [http://localhost:8080](http://localhost:8080) (or your configured `NGINX_PORT`).

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `NGINX_PORT` | `8080` | Host port for nginx HTTP |
| `MYSQL_PORT` | `3306` | Host port for MySQL |
| `MYSQL_ROOT_PASSWORD` | `rootsecret` | MySQL root password |
| `MYSQL_DATABASE` | `laradock` | MySQL database name |
| `MYSQL_USER` | `laradock` | MySQL user |
| `MYSQL_PASSWORD` | `secret` | MySQL user password |
| `REDIS_PORT` | `6379` | Host port for Redis |

## Service Details

- **nginx** (alpine) — Reverse proxy serving PHP application on port `NGINX_PORT`
- **php-fpm** (8.3-fpm-alpine) — PHP runtime with PDO MySQL and Redis extensions
- **mysql** (8.0) — Primary database with persistent named volume
- **redis** (7-alpine) — Cache/session store with persistent named volume

All services include health checks and proper dependency ordering (`depends_on` with `condition: service_healthy`).

## What's NOT Included

The upstream Laradock project includes 80+ optional services for local development. This template omits:
- **Workspace** (dev container with artisan, composer, npm)
- **Horizon** / **Scheduler** (queue workers)
- **Mailpit** / **Mailhog** (email testing)
- **phpMyAdmin** (DB management UI)
- **Selenium** (browser testing)

For full local development, use the upstream [laradock/laradock](https://github.com/laradock/laradock) project directly.

## Upstream

- [GitHub Repository](https://github.com/laradock/laradock)
- [Documentation](https://laradock.io/)
