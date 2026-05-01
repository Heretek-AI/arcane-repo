# Ory Hydra — OAuth 2.0 & OpenID Connect Provider

[Ory Hydra](https://github.com/ory/hydra) (17,104 ★) is a hardened, OpenID Certified OAuth 2.0 server and OpenID Connect provider trusted by OpenAI, Lufthansa, and thousands of organizations. It issues access tokens, refresh tokens, and ID tokens at scale.

Hydra does **not** provide login/registration pages — you build your own UI and Hydra handles the OAuth 2.0 / OIDC protocol logic. This template ships Hydra v2 with PostgreSQL for persistence.

## Quick Start

1. **Set required secrets:**

   Copy `.env.example` to `.env` and set the two mandatory values:

   ```bash
   cp .env.example .env
   # Edit .env — set SECRETS_SYSTEM and POSTGRES_PASSWORD
   ```

2. **Start the stack:**

   ```bash
   docker compose up -d
   ```

   The `hydra-migrate` service runs once to create database tables, then exits. `hydra` starts after the migration completes.

3. **Verify Hydra is running:**

   ```bash
   # Check health
   curl http://localhost:4445/admin/health/alive

   # Check readiness
   curl http://localhost:4445/admin/health/ready
   ```

4. **Create your first OAuth 2.0 client:**

   ```bash
   docker compose exec hydra hydra create oauth2-client \
     --endpoint http://localhost:4445 \
     --id my-client \
     --secret my-secret \
     --grant-type authorization_code,refresh_token \
     --response-type code \
     --scope openid,offline \
     --redirect-uri http://localhost:3000/callback
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### Required Variables — Must Be Set

| Variable              | Description                                                                                  |
|-----------------------|----------------------------------------------------------------------------------------------|
| `SECRETS_SYSTEM`      | Encrypts internal state and OAuth 2.0 tokens. Generate with `openssl rand -hex 32`. Never change after initial setup. |
| `POSTGRES_PASSWORD`   | PostgreSQL superuser password. Set to a strong, unique value.                                |

### Optional Variables

| Variable              | Default                               | Description                                         |
|-----------------------|---------------------------------------|-----------------------------------------------------|
| `POSTGRES_USER`       | `hydra`                               | PostgreSQL user name                                |
| `POSTGRES_DB`         | `hydra`                               | PostgreSQL database name                            |
| `POSTGRES_PORT`       | `5433`                                | Host port for PostgreSQL (offset from default 5432) |
| `HYDRA_PUBLIC_PORT`   | `4444`                                | Host port for public API (OAuth endpoints)          |
| `HYDRA_ADMIN_PORT`    | `4445`                                | Host port for admin API (keep internal)             |
| `HYDRA_ISSUER_URL`    | `http://localhost:4444`               | Public issuer URL — set to your domain in production|
| `HYDRA_CONSENT_URL`   | `http://localhost:3000/consent`       | URL of your consent page UI                         |
| `HYDRA_LOGIN_URL`     | `http://localhost:3000/login`         | URL of your login page UI                           |
| `HYDRA_LOGOUT_URL`    | `http://localhost:3000/logout`        | URL of your logout page UI                          |
| `HYDRA_LOG_LEVEL`     | `info`                                | Log level: panic, fatal, error, warn, info, debug, trace |

## Services

| Service           | Image                    | Port(s)      | Description                                      |
|-------------------|--------------------------|--------------|--------------------------------------------------|
| `hydra`           | `oryd/hydra:v2`          | 4444, 4445   | Hydra OAuth 2.0 / OIDC server — public + admin API|
| `hydra-migrate`   | `oryd/hydra:v2`          | —            | One-shot DB migration — runs once then exits      |
| `postgres`        | `postgres:16-alpine`     | 5433         | PostgreSQL 16 — persistent OAuth 2.0 data store   |

### Dependency Chain

- `postgres` starts first with a `pg_isready` health check
- `hydra-migrate` runs once after `postgres` is healthy (`service_healthy`)
- `hydra` starts after `postgres` is healthy AND `hydra-migrate` completes successfully (`service_completed_successfully`)

## API Endpoints

### Public API (port 4444)

| Endpoint                          | Method | Description                           |
|-----------------------------------|--------|---------------------------------------|
| `/.well-known/openid-configuration`| GET    | OIDC Discovery document               |
| `/.well-known/jwks.json`          | GET    | JSON Web Key Set                      |
| `/oauth2/auth`                    | GET    | Authorization endpoint                |
| `/oauth2/token`                   | POST   | Token endpoint                        |
| `/oauth2/revoke`                  | POST   | Token revocation                      |
| `/userinfo`                       | GET/POST| UserInfo endpoint                     |

### Admin API (port 4445)

| Endpoint                        | Method | Description                           |
|---------------------------------|--------|---------------------------------------|
| `/admin/health/alive`           | GET    | Liveness check                        |
| `/admin/health/ready`           | GET    | Readiness check                       |
| `/admin/clients`                | GET/POST| List / Create OAuth 2.0 clients       |
| `/admin/oauth2/auth/requests/login` | GET/PUT | Get / Accept login requests        |
| `/admin/oauth2/auth/requests/consent` | GET/PUT | Get / Accept consent requests     |
| `/admin/oauth2/introspect`      | POST   | Token introspection                   |

Full API reference: [ory.sh/hydra/docs](https://www.ory.sh/hydra/docs/)

## Managing the Stack

**View logs:**

```bash
docker compose logs -f hydra
docker compose logs -f postgres
```

**List OAuth 2.0 clients:**

```bash
docker compose exec hydra hydra list oauth2-clients --endpoint http://localhost:4445
```

**Delete a client:**

```bash
docker compose exec hydra hydra delete oauth2-client my-client --endpoint http://localhost:4445
```

**Introspect a token:**

```bash
curl -X POST http://localhost:4445/admin/oauth2/introspect \
  -d "token=<access-token>"
```

## Volume Management

| Volume               | Mount point                  | Content                     |
|----------------------|------------------------------|-----------------------------|
| `ory_hydra_db_data`  | `/var/lib/postgresql/data`   | PostgreSQL database files   |

**Backup the database:**

```bash
docker run --rm -v ory_hydra_db_data:/source -v $(pwd):/backup alpine tar czf /backup/hydra-db-backup.tar.gz -C /source .
```

## Production Considerations

- **`--dev` flag:** This template runs Hydra with `--dev` flag. Remove it in production and set proper TLS (`serve all` without `--dev`).
- **Admin API:** Port 4445 should not be exposed publicly. Use a reverse proxy with authentication or keep it internal.
- **Secrets rotation:** Changing `SECRETS_SYSTEM` invalidates all existing tokens. Rotate only during maintenance windows.
- **Consent/login UI:** Hydra requires external login/consent pages. Build a simple UI (Next.js, Express, etc.) and point `HYDRA_CONSENT_URL`, `HYDRA_LOGIN_URL`, and `HYDRA_LOGOUT_URL` at it.
- **Issuer URL:** Set `HYDRA_ISSUER_URL` to your production domain (e.g., `https://auth.example.com`). This value appears in tokens and cannot be changed without breaking existing clients.

## Troubleshooting

| Symptom                            | Likely Cause                              | Fix                                                          |
|------------------------------------|-------------------------------------------|--------------------------------------------------------------|
| `SECRETS_SYSTEM is required` error | `SECRETS_SYSTEM` not set in `.env`        | Set `SECRETS_SYSTEM` in `.env` and restart with `docker compose up -d` |
| `POSTGRES_PASSWORD is required` error| `POSTGRES_PASSWORD` not set in `.env`   | Set `POSTGRES_PASSWORD` in `.env` and restart                |
| Hydra refuses connections          | PostgreSQL not ready                      | Wait 10–15 seconds for `service_healthy` check, then retry   |
| DB migration fails                 | PostgreSQL already has conflicting tables | Drop the database and rebuild: `docker compose down -v && docker compose up -d` |
| Token introspection fails          | Admin endpoint not accessible             | Ensure port 4445 is accessible from the calling service       |
| Consent/login redirects broken     | `HYDRA_CONSENT_URL`/`HYDRA_LOGIN_URL` wrong| Verify URLs point to your running UI application             |

Official docs: [ory.sh/hydra/docs](https://www.ory.sh/hydra/docs/)
