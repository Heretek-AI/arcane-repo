# Botpress — Chatbot Platform

[Botpress](https://botpress.com/) is an open-source chatbot platform that enables you to build, deploy, and manage conversational AI agents with a visual flow editor, built-in NLU engine, and multi-channel support (web, WhatsApp, Messenger, Slack, Telegram, and more).

## Quick Start

1. **Copy and edit the environment file:**

   ```bash
   cp .env.example .env
   # Set DB_USER and DB_PASSWORD
   ```

2. **Start all services:**

   ```bash
   docker compose up -d
   ```

3. **Access Botpress Studio:**

   Open [http://localhost:3000](http://localhost:3000) in your browser.

4. **Verify the API:**

   ```bash
   curl http://localhost:3000/api/v1/health
   ```

   Expected response: `{"status":"ok"}` or similar health indication.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable           | Default                               | Description                                     |
|--------------------|---------------------------------------|-------------------------------------------------|
| `DB_USER`          | `botpress`                            | PostgreSQL user                                 |
| `DB_PASSWORD`      | — **(required)**                      | PostgreSQL password                             |
| `DB_NAME`          | `botpress`                            | PostgreSQL database name                        |
| `BOTPRESS_PORT`    | `3000`                                | Host port for Botpress UI and API               |
| `BOTPRESS_DB_PORT` | `5432`                                | Host port for PostgreSQL                        |
| `BP_PRODUCTION`    | `true`                                | Production mode flag                            |
| `EXTERNAL_URL`     | `http://localhost:3000`               | Public URL for webhook callbacks                |
| `BP_SERVER_HOST`   | `0.0.0.0`                             | Bind address                                    |
| `BP_LICENSE_KEY`   | —                                     | Pro/Enterprise license key (optional)           |

## Services

| Service    | Image                   | Port  | Description                        |
|------------|-------------------------|-------|------------------------------------|
| `botpress` | `botpress/server:latest`| 3000  | Botpress server with Studio UI     |
| `postgres` | `postgres:16`           | 5432  | Primary database                   |

## API Endpoints

The Botpress API is available on port 3000:

| Endpoint                | Method | Description                       |
|-------------------------|--------|-----------------------------------|
| `/api/v1/health`        | GET    | Health check                      |
| `/api/v1/bots`          | GET    | List bots                         |
| `/api/v1/bots`          | POST   | Create a bot                      |
| `/studio`               | GET    | Botpress Studio UI                |

## Health Check

```bash
# Botpress server
curl http://localhost:3000/api/v1/health

# PostgreSQL
docker compose exec postgres pg_isready -U ${DB_USER:-botpress}
```

## Managing Botpress

**View logs:**

```bash
docker compose logs -f botpress
```

**Stop all services:**

```bash
docker compose down
```

**Reset the database:**

```bash
docker compose down -v botpress-postgres
docker compose up -d
```

## Troubleshooting

| Symptom                                    | Likely Cause                     | Fix                                                  |
|--------------------------------------------|----------------------------------|------------------------------------------------------|
| Botpress can't connect to database         | Wrong DB credentials             | Verify `DB_USER` and `DB_PASSWORD` match `.env`      |
| Studio shows loading spinner               | Database not ready yet           | Wait for postgres health check to pass               |
| `Connection refused` on port 3000          | Botpress still starting          | Wait and retry — first start can take 30s+           |
| Webhook callbacks fail                     | Wrong `EXTERNAL_URL`             | Set `EXTERNAL_URL` to the publicly reachable URL     |
