---
title: "Dify"
description: "Open-source LLM application development platform — build AI apps with visual workflows, RAG pipelines, agent capabilities, and model management"
---

# Dify

Open-source LLM application development platform — build AI apps with visual workflows, RAG pipelines, agent capabilities, and model management

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/llm" class="tag-badge">llm</a> <a href="/categories/platform" class="tag-badge">platform</a> <a href="/categories/low-code" class="tag-badge">low-code</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dify/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dify/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dify/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dify` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `be905100cc537c464b5071aad4e99a57ea618ef700b48b7128cc54e0382b075c` |

## Quick Start

1. **Set required configuration:**

   Copy `.env.example` to `.env` and set at least the two mandatory values:

   ```bash
   cp .env.example .env
   # Edit .env — set SECRET_KEY and POSTGRES_PASSWORD
   ```

2. **Start the stack:**

   ```bash
   docker compose up -d
   ```

3. **Access Dify:**

   Open [http://localhost:5001](http://localhost:5001) in your browser and follow the first-time setup flow to create your admin account.

4. **Verify the API:**

   ```bash
   curl http://localhost:5001/health
   ```

   A successful response returns JSON indicating the API server is running.

## Configuration

Copy `.env.example` to `.env` and edit:

### Mandatory Variables

| Variable              | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `SECRET_KEY`          | Encrypts session data, tokens, and API keys. Set to a fixed value before first run — changing it invalidates all existing sessions. Generate with `openssl rand -hex 32`. |
| `POSTGRES_PASSWORD`   | PostgreSQL superuser password. Set to a strong, unique value.               |

### Optional Variables

| Variable              | Default     | Description                                        |
|-----------------------|-------------|----------------------------------------------------|
| `POSTGRES_DB`         | `dify`      | PostgreSQL database name                           |
| `POSTGRES_USER`       | `dify`      | PostgreSQL user name                               |
| `POSTGRES_PORT`       | `5432`      | Host port for PostgreSQL                           |
| `REDIS_PORT`          | `6379`      | Host port for Redis                                |
| `DIFY_PORT`           | `5001`      | Host port for the Dify API server                  |
| `DIFY_DEBUG`          | `false`     | Enable debug mode (detailed error messages)        |
| `INIT_PASSWORD`       | *(empty)*   | Initial admin password for first-time setup        |

## Troubleshooting

| Symptom                              | Likely Cause                                  | Fix                                                       |
|--------------------------------------|-----------------------------------------------|-----------------------------------------------------------|
| `SECRET_KEY is required` error       | `SECRET_KEY` not set in `.env`                | Add `SECRET_KEY` to `.env` and restart                    |
| `POSTGRES_PASSWORD is required` error| `POSTGRES_PASSWORD` not set in `.env`         | Add `POSTGRES_PASSWORD` to `.env` and restart             |
| API refuses connection               | `postgres` or `redis` not healthy yet         | Wait 10–15 seconds, then retry — depends_on waits for health |
| Login page loops / sessions lost     | `SECRET_KEY` changed between runs             | Restore the original `SECRET_KEY` value                   |
| Worker not processing jobs           | Worker container stopped or crashed           | Run `docker compose logs worker` and check for errors     |

## API Endpoints

Dify exposes a REST API on port 5001:

| Endpoint                      | Method | Description                           |
|-------------------------------|--------|---------------------------------------|
| `/health`                     | GET    | Health check                          |
| `/v1/chat-messages`           | POST   | Send a chat message                   |
| `/v1/completion-messages`     | POST   | Send a completion request             |
| `/v1/datasets`                | GET    | List knowledge base datasets          |
| `/v1/datasets`                | POST   | Create a knowledge base dataset       |
| `/v1/workflows`               | GET    | List workflows                        |
| `/v1/workflows`               | POST   | Create a workflow                     |
| `/console/api/workspaces/current` | GET | Get current workspace info            |
| `/console/api/account/login`  | POST   | Login (returns access token)          |

Full API reference: [docs.dify.ai/api-reference](https://docs.dify.ai/api-reference)

## Health Check

```bash
curl http://localhost:5001/health
```

A successful response returns a JSON object indicating the API server is operational. To check individual services:

```bash
# PostgreSQL
docker compose exec postgres pg_isready -U dify

# Redis
docker compose exec redis redis-cli ping
# Should return: PONG
```

