---
title: "Ory Hydra — OAuth 2.0 &amp; OpenID Connect Provider"
description: "Hardened, OpenID Certified OAuth 2.0 and OpenID Connect provider trusted by OpenAI — self-hosted authorization server with PostgreSQL persistence"
---

# Ory Hydra — OAuth 2.0 &amp; OpenID Connect Provider

Hardened, OpenID Certified OAuth 2.0 and OpenID Connect provider trusted by OpenAI — self-hosted authorization server with PostgreSQL persistence

## Tags

<a href="/categories/security" class="tag-badge">security</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ory-hydra/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ory-hydra/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ory-hydra/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `ory-hydra` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `11854a249aa3f282df616cdf29f115576d5ea4268300f945a6b2a2e8ef69ae8e` |

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

