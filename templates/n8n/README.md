# n8n — Fair-Code Workflow Automation

[n8n](https://n8n.io) is a fair-code workflow automation platform that lets you connect apps, APIs, and services with a drag-and-drop visual editor. With over 400 integrations, built-in AI agent capabilities, and full code mode for custom logic, it serves as a powerful automation backbone for everything from simple data pipelines to complex multi-step workflows.

## Quick Start

1. **Set the encryption key (mandatory — see warning below):**

   ```bash
   cp .env.example .env
   # Edit .env and set N8N_ENCRYPTION_KEY to a strong random value
   ```

2. **Start n8n:**

   ```bash
   docker compose up -d
   ```

3. **Open the editor:**

   Visit [http://localhost:5678](http://localhost:5678) in your browser.

## ⚠️  Encryption Key — Critical

n8n encrypts all stored credentials using `N8N_ENCRYPTION_KEY`. This includes database connections, API keys, OAuth tokens, and any other secrets saved through the n8n editor.

**If `N8N_ENCRYPTION_KEY` changes after credentials have been saved, they become permanently unrecoverable.** There is no recovery mechanism.

```bash
# Generate a strong key before first run:
openssl rand -hex 32
```

Set `N8N_ENCRYPTION_KEY` to a fixed, strong value in your `.env` file and **never change it** for the same n8n instance.

## Configuration

### Environment Variables

| Variable                      | Default                     | Description                                            |
|-------------------------------|-----------------------------|--------------------------------------------------------|
| `N8N_ENCRYPTION_KEY`          | *(required, no default)*    | Key for credential encryption — set to a strong value  |
| `N8N_PORT`                    | `5678`                      | Host port for the n8n web UI and API                   |
| `N8N_PROTOCOL`                | `http`                      | Protocol for webhook URLs (`http` or `https`)          |
| `N8N_HOST`                    | `localhost`                 | Public hostname where n8n is reachable                 |
| `N8N_WEBHOOK_URL`             | *(empty)*                   | Full webhook URL override (overrides protocol + host)  |
| `N8N_BASIC_AUTH_ACTIVE`       | `false`                     | Enable basic auth for the editor                       |
| `N8N_BASIC_AUTH_USER`         | *(empty)*                   | Basic auth username                                    |
| `N8N_BASIC_AUTH_PASSWORD`     | *(empty)*                   | Basic auth password                                    |

### Webhook Configuration

For n8n to receive incoming webhooks from external services (GitHub, Stripe, Slack, etc.), n8n must be reachable from the internet.

**With a public domain and reverse proxy (recommended):**

```bash
N8N_PROTOCOL=https
N8N_HOST=n8n.example.com
N8N_WEBHOOK_URL=https://n8n.example.com/
```

**Behind ngrok for testing:**

```bash
N8N_WEBHOOK_URL=https://your-ngrok-subdomain.ngrok.io/
```

**Local-only development:**

Webhooks work on `localhost` for testing but external services cannot reach them. Use a tool like [ngrok](https://ngrok.com) or [bore](https://github.com/ekzhang/bore) to expose localhost during development.

### External Database (Optional)

By default, n8n stores data in a SQLite database inside the container volume (`n8n_data`). For production, you can switch to PostgreSQL for better performance, reliability, and external backups.

Uncomment the `DB_TYPE` and `DB_POSTGRESDB_*` variables in `docker-compose.yml` and add a PostgreSQL service:

```yaml
services:
  n8n:
    # ... existing config ...
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=your-password

  postgres:
    image: postgres:16-alpine
    container_name: n8n-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=your-password
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  postgres_data:
```

## Basic Authentication

To protect the n8n editor with a username and password:

```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password
```

After enabling, restart the container:

```bash
docker compose restart n8n
```

## Managing n8n

**View logs:**

```bash
docker compose logs -f n8n
```

**Restart after configuration changes:**

```bash
docker compose restart n8n
```

**Upgrade to the latest version:**

```bash
docker compose pull n8n
docker compose up -d
```

**Export all workflows (JSON backup):**

```bash
# Install n8n CLI inside the container
docker compose exec n8n npx n8n export:workflow --all --output=/home/node/.n8n/backups
```

## API Endpoints

n8n exposes a comprehensive REST API on port 5678:

| Endpoint                     | Method | Description                      |
|------------------------------|--------|----------------------------------|
| `/webhook/:id`               | ANY    | Incoming webhook endpoint        |
| `/webhook-test/:id`          | ANY    | Webhook test endpoint            |
| `/webhook-waiting/:id`       | ANY    | Manual webhook trigger           |
| `/rest/workflows`            | GET    | List all workflows               |
| `/rest/workflows/:id`        | GET    | Get a specific workflow          |
| `/rest/executions`           | GET    | List execution history           |
| `/rest/credentials`          | GET    | List stored credentials          |
| `/health`                    | GET    | Health check                     |

Full API reference: [docs.n8n.io/api](https://docs.n8n.io/api/)

## Health Check

```bash
curl http://localhost:5678/health
```

A healthy n8n instance returns `{"status":"ok","startedAt":"..."}`.
