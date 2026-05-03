---
title: "Flagsmith"
description: "Open-source feature flag and remote config platform — release features, run A/B tests, and manage configuration across web, mobile, and server-side apps"
---

# Flagsmith

Open-source feature flag and remote config platform — release features, run A/B tests, and manage configuration across web, mobile, and server-side apps

## Tags

<a href="/categories/devops" class="tag-badge">devops</a> <a href="/categories/multi-service" class="tag-badge">multi-service</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flagsmith/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flagsmith/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flagsmith/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `flagsmith` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1d0a51e27212adaf2ce5f6b1fa1bab58d03668fb8292650925f4e6ba24ae2de9` |

## Architecture

This template ships a 2-service platform:

| Service | Image | Port | Purpose |
|---|---|---|---|
| `postgres` | `postgres:16-alpine` | — | Relational database (flags, segments, identities, audit log) |
| `flagsmith` | `flagsmith/flagsmith:latest` | 8000 | Django REST API + React admin dashboard |

Both services use **MEM069 health checks** with `condition: service_healthy` dependency cascading.

## Quick Start

1. **Copy the environment file & generate secrets:**

   ```bash
   cp .env.example .env
   # Generate a secure SECRET_KEY:
   sed -i "s/replace-with-openssl-rand-hex-32/$(openssl rand -hex 32)/" .env
   # Set a strong admin password:
   # FLAGSMITH_ADMIN_PASSWORD=your-strong-password
   ```

2. **Start the platform:**

   ```bash
   docker compose up -d
   ```

   Wait ~30-60 seconds for the Django app to run database migrations and initialize. The `flagsmith` container automatically runs `python manage.py migrate` on startup.

3. **Create the superuser (first time only):**

   When `ENABLE_ADMIN_ACCESS_USER_PASS=true`, a superuser is **not** auto-created — you must create it manually:

   ```bash
   docker compose exec flagsmith python manage.py createsuperuser
   ```

   Follow the prompts to set an email and password.

   > **Note:** The `ADMIN_EMAIL` / `ADMIN_INITIAL_PASSWORD` env vars are part of Flagsmith's onboarding flow; the actual superuser is created via `createsuperuser`.

4. **Access the dashboard:**

   Open [http://localhost:8000](http://localhost:8000) and log in with the superuser credentials you created.

5. **Use the API:**

   The Flagsmith API is available at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/). Client SDKs (JavaScript, Python, Java, .NET, Go, Ruby, PHP, Swift, Kotlin, Flutter, React, React Native) are available — see the [SDK docs](https://docs.flagsmith.com/clients/overview).

## Configuration

Copy `.env.example` to `.env` and edit the values.

### Required

| Variable | Description |
|---|---|
| `FLAGSMITH_DB_PASSWORD` | PostgreSQL database password |
| `FLAGSMITH_SECRET_KEY` | Django secret key (min 32 hex chars) |

### Admin Setup

| Variable | Default | Description |
|---|---|---|
| `FLAGSMITH_ADMIN_EMAIL` | `admin@example.com` | Admin email for onboarding |
| `FLAGSMITH_ADMIN_PASSWORD` | `changeme` | Admin password — change immediately |

### Access Control

| Variable | Default | Description |
|---|---|---|
| `FLAGSMITH_ALLOW_OPEN_REGISTRATION` | `true` | Allow anyone to sign up |
| `FLAGSMITH_PREVENT_SIGNUP` | `false` | Completely disable new signups |

### SMTP (Recommended for Production)

| Variable | Default | Description |
|---|---|---|
| `FLAGSMITH_SMTP_HOST` | *(empty)* | SMTP server hostname |
| `FLAGSMITH_SMTP_PORT` | `587` | SMTP port |
| `FLAGSMITH_SMTP_USER` | *(empty)* | SMTP username |
| `FLAGSMITH_SMTP_PASSWORD` | *(empty)* | SMTP password |
| `FLAGSMITH_SMTP_USE_TLS` | `true` | Use TLS for SMTP |

### Port

| Variable | Default | Description |
|---|---|---|
| `FLAGSMITH_PORT` | `8000` | Host port for the Flagsmith web UI and API |

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Container exits with `django.db.utils.OperationalError` | Postgres not ready or wrong credentials | Check `postgres` healthcheck; verify `FLAGSMITH_DB_PASSWORD` matches `POSTGRES_PASSWORD` |
| `/health` returns 500 | Migrations not run | Restart flagsmith: `docker compose restart flagsmith` (migrations run on startup) |
| Login page works but can't log in | Superuser not created | Run `docker compose exec flagsmith python manage.py createsuperuser` |
| `FLAGSMITH_PREVENT_SIGNUP=true` prevents first login | No superuser exists | Temporarily set `PREVENT_SIGNUP=false`, create superuser, then re-enable |
| Flags aren't updating in SDK | SDK cache | Clear client-side cache; verify SDK points to the correct API URL |

## Upstream

- [GitHub Repository](https://github.com/Flagsmith/flagsmith) — 6.3k★
- [Docker Hub](https://hub.docker.com/r/flagsmith/flagsmith)
- [Documentation](https://docs.flagsmith.com)
- [Client SDKs](https://docs.flagsmith.com/clients/overview)

