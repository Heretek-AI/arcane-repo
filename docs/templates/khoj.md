---
title: "Khoj"
description: "Open-source, AI-powered personal search assistant — index your documents, notes, and code, then search and chat with them using local or cloud LLMs"
---

# Khoj

Open-source, AI-powered personal search assistant — index your documents, notes, and code, then search and chat with them using local or cloud LLMs

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/search" class="tag-badge">search</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/khoj/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/khoj/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/khoj/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `khoj` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `61d67aebb95ab5205f2326b1e6add10b3c89780aec9101566b799f108a2574cd` |

## Quick Start

1. **Set your API key and start the server:**

   ```bash
   cp .env.example .env
   # Edit .env — set OPENAI_API_KEY for cloud inference, or configure a local LLM
   docker compose up -d
   ```

2. **Access the web interface:**

   Open [http://localhost:42110](http://localhost:42110) and log in with the admin credentials from `.env` (default: `admin@example.com` / `password`).

3. **Index your content:**

   From the web UI, navigate to the content settings and add folders or files to index. Khoj supports:
   - Markdown files (`.md`)
   - Plain text (`.txt`, `.org`)
   - PDF documents (`.pdf`)
   - Source code files (`.py`, `.js`, `.ts`, `.go`, `.rs`, etc.)

4. **Search or chat:**

   Use the search bar at the top of the page or open the chat panel to ask questions about your indexed content:

   ```
   "What did I write about Docker deployments?"
   "Summarize my notes on project architecture."
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### LLM Backend

At least one LLM backend must be configured:

| Variable                | Default              | Description                              |
|-------------------------|----------------------|------------------------------------------|
| `OPENAI_API_KEY`        | *(empty)*            | OpenAI API key (for cloud models)        |
| `KHOJ_OPENAI_MODEL`     | `gpt-4o-mini`        | OpenAI model to use for chat             |
| `KHOJ_LLM_MODEL_NAME`   | *(empty)*            | Local model name (e.g., `llama3.1:8b`)   |
| `KHOJ_LLM_API_KEY`      | *(empty)*            | API key for the local LLM endpoint       |
| `KHOJ_LLM_API_BASE_URL` | *(empty)*            | Base URL for the local LLM endpoint      |

### Search and Admin

| Variable                | Default                                   | Description                              |
|-------------------------|-------------------------------------------|------------------------------------------|
| `KHOJ_PORT`             | `42110`                                   | Host port for Khoj                       |
| `KHOJ_SEARCH_MODEL`     | `sentence-transformers/all-MiniLM-L6-v2`  | Embedding model for search               |
| `KHOJ_ADMIN_EMAIL`      | `admin@example.com`                       | Admin account email                      |
| `KHOJ_ADMIN_PASSWORD`   | `password`                                | Admin account password                   |

## Troubleshooting

| Symptom                                                | Likely Cause                     | Fix                                                |
|--------------------------------------------------------|----------------------------------|----------------------------------------------------|
| Login page shows but credentials don't work            | Admin credentials not configured | Set `KHOJ_ADMIN_EMAIL` and `KHOJ_ADMIN_PASSWORD` in `.env` |
| `/api/chat` returns 500                                | LLM backend not configured       | Set `OPENAI_API_KEY` or configure a local LLM      |
| Search returns no results                              | No content indexed yet           | Add content folders through the web UI             |
| Container exits immediately                            | Invalid configuration            | Run `docker compose logs khoj` for details         |
| Slow initial startup                                   | Downloading embedding model      | The first startup downloads the search model — this is expected and may take a minute |

## API Endpoints

Khoj exposes a REST API on port 42110:

| Endpoint                    | Method | Description                         |
|-----------------------------|--------|-------------------------------------|
| `/api/health`               | GET    | Health check                        |
| `/api/search`               | POST   | Search indexed content              |
| `/api/chat`                 | POST   | Chat with AI about your content     |
| `/api/config/content`       | GET    | List configured content sources     |
| `/api/config/content`       | PUT    | Update content source configuration |

## Health Check

```bash
curl http://localhost:42110/api/health
```

A healthy server returns:
```json
{"status": "ok", "version": "..."}
```

