# InsForge — Agentic Backend

> **Database + REST API layer — postgres and PostgREST.**
> [InsForge](https://github.com/InsForge/InsForge) gives AI agents everything they need to build full-stack apps:
> a postgres database with schema auto-generated REST APIs via PostgREST.
> This template provides the data and API layer using published images.
> For the full InsForge experience (web UI, Deno runtime), clone the upstream repo.

## Quick Start

1. **Start the database and API:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify the database is healthy:**

   ```bash
   docker compose exec postgres pg_isready -U postgres
   ```

3. **Explore the auto-generated API:**

   ```bash
   curl http://localhost:3000/
   ```

   PostgREST serves an OpenAPI spec at `/` and exposes database tables as REST endpoints.

## Default Credentials

| Service    | Username | Password | Port |
|------------|----------|----------|------|
| PostgreSQL | postgres | postgres | 5432 |
| PostgREST  | —        | JWT auth | 3000 |

## API Usage

PostgREST automatically exposes any tables/schemas in the `public` schema as RESTful endpoints.

**Query a table:**

```bash
curl "http://localhost:3000/your_table"
```

**Filter with query parameters:**

```bash
curl "http://localhost:3000/your_table?column=eq.value"
```

**Mutate with POST/PATCH/DELETE:**

```bash
curl -X POST http://localhost:3000/your_table \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${JWT_SECRET}" \
  -d '{"column": "value"}'
```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable            | Default                             | Description                        |
|---------------------|-------------------------------------|------------------------------------|
| `POSTGRES_PORT`     | `5432`                              | Host port for PostgreSQL           |
| `POSTGRES_USER`     | `postgres`                          | Database user                      |
| `POSTGRES_PASSWORD` | `postgres`                          | Database password                  |
| `POSTGRES_DB`       | `insforge`                          | Database name                      |
| `POSTGREST_PORT`    | `3000`                              | Host port for REST API             |
| `JWT_SECRET`        | `dev-secret-please-change-in-production` | JWT signing secret           |
| `ENCRYPTION_KEY`    | —                                   | Encryption key for secrets         |

## Full InsForge Stack

This template provides only the data and API layer. To run the full InsForge stack
(web dashboard, Deno serverless functions), clone the upstream repository:

```bash
git clone https://github.com/InsForge/InsForge.git
cd InsForge
docker compose up -d
```

The upstream compose includes:
- **InsForge App** — Admin dashboard and builder UI on port 7130
- **Deno Runtime** — Serverless edge functions on port 7133
- **PostgreSQL** — Database (also provided here)
- **PostgREST** — Auto-generated REST API (also provided here)

## Managing InsForge

**View logs:**

```bash
docker compose logs -f postgrest
```

**Stop services:**

```bash
docker compose down
```

**Reset the database:**

```bash
docker compose down -v
docker compose up -d
```

## Troubleshooting

| Symptom                                    | Likely Cause                    | Fix                                                |
|--------------------------------------------|---------------------------------|----------------------------------------------------|
| PostgREST won't connect to postgres        | Postgres not healthy yet        | Wait 10s and retry                                 |
| `pg_isready` fails                         | Wrong credentials in `.env`     | Check `POSTGRES_USER` / `POSTGRES_PASSWORD`        |
| PostgREST returns 503                      | Schema not initialized          | Create tables in the `public` schema via psql      |
| Need the full UI dashboard                 | Using simplified template       | Clone upstream and run its full `docker-compose.yml` |
