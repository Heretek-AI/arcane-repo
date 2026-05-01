# Supabase

[Supabase](https://github.com/supabase/supabase) — Open-source Firebase alternative with PostgreSQL, auth, realtime, storage, and edge functions (101.7k★)

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Generate JWT keys:**

   First, generate a strong `JWT_SECRET`:

   ```bash
   echo "JWT_SECRET=$(openssl rand -hex 32)"
   ```

   Copy the output into `.env`, replacing the default `JWT_SECRET`.

   Then generate `ANON_KEY` and `SERVICE_ROLE_KEY` using the Python helper:

   ```bash
   python3 -c "
   import jwt, time
   secret = open('.env').read().split('JWT_SECRET=')[1].split('\\n')[0].strip()
   now = int(time.time())
   anon = jwt.encode({'role': 'anon', 'iss': 'supabase', 'iat': now, 'exp': now + 10*365*24*3600}, secret, algorithm='HS256')
   service = jwt.encode({'role': 'service_role', 'iss': 'supabase', 'iat': now, 'exp': now + 10*365*24*3600}, secret, algorithm='HS256')
   print(f'ANON_KEY={anon}')
   print(f'SERVICE_ROLE_KEY={service}')
   "
   ```

   Copy each output line into `.env` replacing the placeholder values.

   > **Note:** Requires `pyjwt` — install with `pip install pyjwt` if not available.

3. **Start the platform:**

   ```bash
   docker compose up -d
   ```

   Wait ~30-60 seconds for all services to initialize.

4. **Access the dashboard:**

   Open [http://localhost:8082](http://localhost:8082) and log in with the credentials from `.env` (`DASHBOARD_USERNAME` / `DASHBOARD_PASSWORD`).

5. **Use the API:**

   The Supabase API is available at [http://localhost:8000](http://localhost:8000).

## Architecture

This template reproduces Supabase's core self-hosted stack using the **simplified core + documented optionals** pattern (D010). It runs 8 core services instead of the full 20+ service stack — enough for local development and testing.

### Core Services (8)

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `postgres` | `supabase/postgres:15.8.1` | 5432 | PostgreSQL with Supabase extensions (pg_graphql, pg_cron, etc.) |
| `kong` | `supabase/kong:2.8.1` | 8000, 8001 | API gateway — routes all Supabase API traffic |
| `auth` | `supabase/auth:2.172.0` | 9999 | GoTrue — user authentication and management |
| `rest` | `supabase/rest:12.2.6` | 3000 | PostgREST — auto-generated REST API from PostgreSQL schema |
| `realtime` | `supabase/realtime:2.34.16` | 4000 | WebSocket-based realtime subscriptions |
| `storage` | `supabase/storage-api:1.20.3` | 5000 | S3-compatible object storage (files, images) |
| `edge-runtime` | `supabase/edge-runtime:v1.67.5` | 9998 | Deno runtime for edge functions |
| `studio` | `supabase/studio:2026.04.21` | 3000→8082 | Admin dashboard with table editor, SQL editor, auth management |

All services communicate over a shared `supabase-net` bridge network. Health checks use `pg_isready` (PostgreSQL), `/health` (auth), `/ready` (rest), `/status` (kong admin API).

### Startup Order

```
postgres → auth, rest
postgres → realtime
postgres + rest → storage
kong → edge-runtime, studio
rest + kong → studio
```

`depends_on` with `condition: service_healthy` ensures cascade-correct startup (MEM069).

## Configuration

Copy `.env.example` to `.env` and set:

| Variable | Required | Description |
|----------|----------|-------------|
| `POSTGRES_PASSWORD` | ✅ | PostgreSQL superuser password |
| `JWT_SECRET` | ✅ | HMAC key for JWT tokens (generate with `openssl rand -hex 32`) |
| `ANON_KEY` | ✅ | Anonymous key (JWT signed with `JWT_SECRET`, role: `anon`) |
| `SERVICE_ROLE_KEY` | ✅ | Service role key (JWT signed with `JWT_SECRET`, role: `service_role`) |
| `DASHBOARD_USERNAME` | ✅ | Studio dashboard login username |
| `DASHBOARD_PASSWORD` | ✅ | Studio dashboard login password |
| `KONG_HTTP_PORT` | | Host port for API gateway (default: 8000) |
| `KONG_ADMIN_PORT` | | Host port for Kong admin API (default: 8001) |
| `STUDIO_PORT` | | Host port for Studio dashboard (default: 8082) |

## Optional Services

Supabase's full self-hosted stack includes additional services not included in this core template. You can add them by extending `docker-compose.yml`:

| Service | Image | Purpose | Why Optional |
|---------|-------|---------|-------------|
| `imgproxy` | `supabase/imgproxy:v3.26.1` | On-the-fly image resizing/transformation | Only needed if using Storage image transformations |
| `meta` | `supabase/meta:0.85.1` | PostgreSQL introspection API | Studio already includes basic table viewing; meta adds advanced schema introspection |
| `logflare` | `supabase/logflare:1.22.14` | Log ingestion and search for Studio logs | Log collection is useful for debugging edge functions but adds complexity |
| `vector` | `supabase/vector:0.28.1` | Log transport pipeline | Transports PostgreSQL logs to logflare |

To add an optional service, copy its service definition from the [upstream docker-compose.yml](https://github.com/supabase/supabase/blob/master/docker/docker-compose.yml) and add it to this template's compose file.

## Key Features

- **Managed PostgreSQL** with 50+ extensions (pgvector, pg_cron, pgsodium, pg_graphql)
- **Instant REST API** — tables become REST endpoints automatically via PostgREST
- **Auth** — email/password, magic links, OAuth (40+ providers), phone login
- **Realtime** — subscribe to database changes over WebSockets
- **Edge Functions** — serverless Deno functions deployed globally
- **Row-Level Security** — fine-grained access control on every table
- **Storage** — S3-compatible object storage with resumable uploads
- **Studio** — browser-based admin dashboard with table editor, SQL editor, and auth management

## Design Decisions

- **Docker-ready** (not custom-build) — all images are published on Docker Hub by Supabase. No custom Dockerfiles or CI workflow needed.
- **Specific version tags** (never `:latest`) — Supabase images version independently; pinning ensures reproducible deployments.
- **D010 core+optionals** — 8 services cover 95% of developer workflows. Optional services documented for advanced users.
- **Health-checked dependencies** — MEM069 pattern: `pg_isready` for PostgreSQL, `/health` for auth, `/ready` for rest, `/status` for Kong admin API.

## Limitations

- **Not production-hardened** — this template assumes `GOTRUE_MAILER_AUTOCONFIRM=true` for local dev. For production, configure SMTP, rate limiting, and TLS.
- **No backup automation** — PostgreSQL data persists in a named volume, but no automated backup is included.
- **Single-node only** — no replication, load balancing, or high-availability setup.
- **Simplified networking** — services use a single bridge network. Production deployments should isolate public and internal traffic.

## Troubleshooting

**Studio shows "Failed to connect" after login:**
Wait 30-60 seconds after `docker compose up -d`. The studio takes time to discover all backend services. Run `docker compose logs studio` to check progress.

**Auth returns 500 errors:**
The auth service needs PostgreSQL migrations to run first. Check logs with `docker compose logs auth`. If you see "relation does not exist" errors, restart the auth container: `docker compose restart auth`.

**Storage uploads fail:**
Ensure `ENABLE_IMAGE_TRANSFORMATION=false` if imgproxy is not running. The storage service attempts to contact imgproxy on startup; missing imgproxy causes warnings but doesn't block uploads when image transformations are disabled.

**Realtime subscriptions don't work:**
The realtime service needs a replication slot. Check logs: `docker compose logs realtime`. On first start, PostgreSQL must be healthy for at least 15s before realtime can create the publication.

## Upstream

- **Repository:** [github.com/supabase/supabase](https://github.com/supabase/supabase)
- **Stars:** 101,675★
- **License:** Apache-2.0
