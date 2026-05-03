---
title: "WeKnora (Tencent AI Assistant)"
description: "Open-source enterprise AI knowledge assistant by Tencent — deploy a private RAG-powered assistant with document analysis, multi-LLM support, and built-in agent skills"
---

# WeKnora (Tencent AI Assistant)

Open-source enterprise AI knowledge assistant by Tencent — deploy a private RAG-powered assistant with document analysis, multi-LLM support, and built-in agent skills

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/rag" class="tag-badge">rag</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/weknora/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/weknora/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/weknora/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `weknora` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `047915c3dd158af61470a5d521afbb6701629c83c96f20222bcbe13af7cd794d` |

## Quick Start

1. **Prepare the config file:**

   ```bash
   mkdir -p config
   curl -o config/config.yaml https://raw.githubusercontent.com/Tencent/WeKnora/main/config/config.yaml
   ```

2. **Set up environment variables and start:**

   ```bash
   cp .env.example .env
   # Edit .env — set DB_USER, DB_PASSWORD, JWT_SECRET, etc.
   docker compose up -d
   ```

3. **Access the web UI:**

   Navigate to [http://localhost](http://localhost) (port 80 — or `WEKNORA_UI_PORT` if customized).

4. **Register an account:**

   The first user to register becomes the admin. Navigate to the sign-up page and create your account.

5. **Start a conversation:**

   Upload documents, ask questions, or use the built-in agent skills — all powered by your local LLM via Ollama.

## Configuration

Copy `.env.example` to `.env` and edit:

### Mandatory Variables

| Variable        | Description                                         |
|-----------------|-----------------------------------------------------|
| `DB_USER`       | PostgreSQL username                                 |
| `DB_PASSWORD`   | PostgreSQL password — generate with `openssl rand -hex 32` |
| `JWT_SECRET`    | JWT signing secret — generate with `openssl rand -hex 32` |

### Optional Variables

| Variable                | Default                             | Description                                      |
|-------------------------|-------------------------------------|--------------------------------------------------|
| `DB_NAME`               | `weknora`                           | PostgreSQL database name                         |
| `WEKNORA_APP_PORT`      | `8080`                              | Host port for the app backend                    |
| `WEKNORA_UI_PORT`       | `80`                                | Host port for the frontend UI                    |
| `WEKNORA_DB_PORT`       | `5432`                              | Host port for PostgreSQL                         |
| `REDIS_PASSWORD`        | `redispass`                         | Redis password                                   |
| `OLLAMA_BASE_URL`       | `http://host.docker.internal:11434` | Ollama server URL for local LLM inference        |
| `GIN_MODE`              | `release`                           | Go Gin framework mode: `release` or `debug`      |
| `DISABLE_REGISTRATION`  | `false`                             | Prevent new user registration                    |
| `WEKNORA_LANGUAGE`       | `en`                                | UI language: `en` or `zh-CN`                     |
| `MAX_FILE_SIZE_MB`       | `50`                                | Maximum upload file size in MB                   |

## Troubleshooting

| Symptom                                      | Likely Cause                    | Fix                                                      |
|----------------------------------------------|---------------------------------|----------------------------------------------------------|
| Frontend shows "Backend unavailable"         | App container not ready         | Check `docker compose logs -f app` for startup progress  |
| Chat responses are empty or timeout          | Ollama not running              | Verify Ollama is running and reachable at `OLLAMA_BASE_URL` |
| `401 Unauthorized` on API calls              | Invalid JWT or session expired  | Log out and log back in                                   |
| Upload fails with "File too large"           | `MAX_FILE_SIZE_MB` too low      | Increase the value in `.env` and restart                 |
| Registration is disabled                     | `DISABLE_REGISTRATION=true`     | Set to `false` to allow registration, or use the admin account |

## API Endpoints

The WeKnora app backend exposes a REST API on port 8080:

| Endpoint          | Method | Description                    |
|-------------------|--------|--------------------------------|
| `/health`         | GET    | Health check                   |
| `/api/v1/auth/`   | POST   | Login / Register               |
| `/api/v1/chat/`   | POST   | Chat completion (streaming)    |
| `/api/v1/file/`   | POST   | Upload a file                  |
| `/api/v1/knowledge/` | GET  | List knowledge bases           |

Full API reference: [WeKnora API Docs](https://github.com/Tencent/WeKnora/wiki/API)

## Health Check

```bash
curl http://localhost:8080/health
```

A healthy server returns:
```json
{"status": "ok"}
```

