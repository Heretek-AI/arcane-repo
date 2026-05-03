---
title: "Bishêng"
description: "Open-source LLM application platform — build, deploy, and monitor AI applications with a visual workflow editor, RAG pipelines, and multi-model support"
---

# Bishêng

Open-source LLM application platform — build, deploy, and monitor AI applications with a visual workflow editor, RAG pipelines, and multi-model support

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/llm" class="tag-badge">llm</a> <a href="/categories/platform" class="tag-badge">platform</a> <a href="/categories/low-code" class="tag-badge">low-code</a> <a href="/categories/rag" class="tag-badge">rag</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bisheng/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bisheng/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bisheng/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `bisheng` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6928a66819259bd1bef5856956d423217d97c535925fe3b70b4bd62fdaba05ff` |

## Quick Start

1. **Copy and edit the environment file:**

   ```bash
   cp .env.example .env
   # Set DB_PASSWORD and at least one LLM provider key
   ```

2. **Start all services:**

   ```bash
   docker compose up -d
   ```

3. **Access the frontend:**

   Open [http://localhost:3000](http://localhost:3000) in your browser.

4. **Verify the backend API:**

   ```bash
   curl http://localhost:9001/health
   ```

   Expected response: `{"status":"ok"}` or similar health indication.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable              | Default                               | Description                                     |
|-----------------------|---------------------------------------|-------------------------------------------------|
| `DB_USER`             | `bisheng`                             | PostgreSQL user                                 |
| `DB_PASSWORD`         | — **(required)**                      | PostgreSQL password                             |
| `DB_NAME`             | `bisheng`                             | PostgreSQL database name                        |
| `REDIS_PASSWORD`      | `bishengredis`                        | Redis password                                  |
| `BISHENG_BACKEND_PORT`| `9001`                                | Host port for the backend API                   |
| `BISHENG_FRONTEND_PORT`| `3000`                               | Host port for the frontend UI                   |
| `BISHENG_DB_PORT`     | `5432`                                | Host port for PostgreSQL                        |
| `OPENAI_API_KEY`      | —                                     | OpenAI API key (optional)                       |
| `OLLAMA_BASE_URL`     | `http://host.docker.internal:11434`   | Local Ollama endpoint                           |
| `LLM_MODEL`           | —                                     | Default model (e.g., `gpt-4o`, `llama3`)        |
| `BISHENG_LICENSE`     | —                                     | License key (community edition leaves empty)    |
| `LOG_LEVEL`           | `info`                                | Log level: `debug`, `info`, `warning`, `error`  |

## Troubleshooting

| Symptom                                    | Likely Cause                     | Fix                                                  |
|--------------------------------------------|----------------------------------|------------------------------------------------------|
| Backend can't connect to database          | Wrong DB credentials             | Verify `DB_USER` and `DB_PASSWORD` match `.env`      |
| Frontend shows blank page                  | Backend not ready yet            | Wait for backend health check to pass                |
| `Connection refused` on port 9001          | Backend still starting           | Wait and retry — first start can take 60s+           |
| LLM calls fail                             | Missing API key or model config  | Set `OPENAI_API_KEY` or configure Ollama properly    |
| Ollama returns 404                         | Model not pulled                 | Run `docker exec bisheng-backend ollama pull <model>`|

## API Endpoints

The backend exposes a REST API on port 9001:

| Endpoint          | Method | Description                       |
|-------------------|--------|-----------------------------------|
| `/health`         | GET    | Backend health check              |
| `/api/v1/flows`   | GET    | List workflows                    |
| `/api/v1/flows`   | POST   | Create a workflow                 |
| `/api/v1/run`     | POST   | Execute a workflow                |

## Health Check

```bash
# Backend
curl http://localhost:9001/health

# Frontend
curl http://localhost:3000
```

