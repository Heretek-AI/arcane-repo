# Chatwoot

[Chatwoot](https://github.com/chatwoot/chatwoot) (28.9k★) — Open-source customer engagement platform with shared inboxes, live chat, and omnichannel messaging.

## Quick Start

1. **Copy the environment file & generate secrets:**

   ```bash
   cp .env.example .env
   # Generate a secure SECRET_KEY_BASE:
   sed -i "s/replace-with-openssl-rand-hex-64/$(openssl rand -hex 64)/" .env
   ```

2. **Start the platform:**

   ```bash
   docker compose up -d
   ```

   Wait ~60 seconds for Rails to run database migrations and compile assets. On first start, the `rails` container automatically runs `db:create db:migrate`.

3. **Create a super admin:**

   ```bash
   docker compose exec rails bundle exec rails c
   # Inside the console:
   # Account.create!(name: 'My Org', locale: 'en')
   # SuperAdmin.create!(email: 'admin@example.com', password: 'yourpassword')
   ```

4. **Access the dashboard:**

   Open [http://localhost:3000](http://localhost:3000) and log in.

## Architecture

This template applies the **D010 core+optionals** pattern to simplify Chatwoot's 8+ service upstream compose down to 4 core services:

| Service | Image | Port | Purpose |
|---|---|---|---|
| `postgres` | `postgres:16-alpine` | — | Relational database (user, conversation, account data) |
| `redis` | `redis:7-alpine` | — | Job queue backend, caching, pub/sub |
| `rails` | `chatwoot/chatwoot:latest` | 3000 | Ruby on Rails web server + Vue.js frontend (embedded) |
| `sidekiq` | `chatwoot/chatwoot:latest` | — | Background job processor (email sending, webhook delivery) |

All four services use **MEM069 health checks** with `condition: service_healthy` dependency cascading — `rails` and `sidekiq` wait for `postgres` and `redis` to be healthy before starting.

### What's Not Included (Optional Services)

The upstream compose includes several services this template omits. See the [upstream docker-compose](https://github.com/chatwoot/chatwoot/blob/develop/docker-compose.production.yaml) for how to add them:

| Service | Purpose | When to Add |
|---|---|---|
| `mailcatcher` | SMTP testing (dev) | For local development testing email templates |
| `elasticsearch` | Full-text message search | For large installations needing instant search across millions of conversations |
| `nginx` / `caddy` | Reverse proxy + SSL termination | For production deployments with HTTPS |
| `certbot` | Let's Encrypt certificates | Alongside nginx for auto-renewed TLS |

## Configuration

Copy `.env.example` to `.env` and edit the values.

### Required

| Variable | Description |
|---|---|
| `CHATWOOT_DB_PASSWORD` | PostgreSQL database password |
| `CHATWOOT_SECRET_KEY_BASE` | Rails secret key (min 64 hex chars) |

### SMTP (Required for Production)

Email notifications (password resets, conversation assignments) require SMTP. Without it, you cannot onboard users:

| Variable | Default | Description |
|---|---|---|
| `CHATWOOT_SMTP_ADDRESS` | `smtp.example.com` | SMTP server hostname |
| `CHATWOOT_SMTP_PORT` | `587` | SMTP port |
| `CHATWOOT_SMTP_USERNAME` | — | SMTP username |
| `CHATWOOT_SMTP_PASSWORD` | — | SMTP password |
| `CHATWOOT_MAILER_SENDER` | — | From address for outgoing emails |

### Port

| Variable | Default | Description |
|---|---|---|
| `CHATWOOT_PORT` | `3000` | Host port for the Chatwoot web UI |

## Post-Install Steps

- [ ] Create a super admin account via Rails console
- [ ] Configure SMTP for email delivery
- [ ] Add inbox channels (email, Facebook, WhatsApp, etc.) via the web UI
- [ ] Set up a reverse proxy (nginx/caddy) with TLS for production use
- [ ] Schedule database backups

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Container `chatwoot-rails` exits immediately | Missing `SECRET_KEY_BASE` | Verify `.env` has a 64-char hex key |
| `ActiveRecord::NoDatabaseError` in logs | Database not created | Check `CHATWOOT_DB_PASSWORD` matches postgres env; restart rails after postgres healthcheck passes |
| Login page shows but can't create account | SMTP not configured | Set `ENABLE_ACCOUNT_SIGNUP=true` (default) and complete signup without email confirmation (set `RAILS_ENV=production` already enables auto-confirmation) |
| Sidekiq jobs stuck | Redis unavailable | Check `redis` container health; verify `REDIS_URL=redis://redis:6379` |

## Upstream

- [GitHub Repository](https://github.com/chatwoot/chatwoot) — 28.9k★
- [Docker Hub](https://hub.docker.com/r/chatwoot/chatwoot) — 8.6M+ pulls
- [Official Docs](https://www.chatwoot.com/docs/self-hosted)
