---
title: "Memvid"
description: "Memvid — single-file memory layer for AI agents with instant retrieval, long-term memory, and built-in RAG. Serverless memory that replaces complex vector databases"
---

# Memvid

Memvid — single-file memory layer for AI agents with instant retrieval, long-term memory, and built-in RAG. Serverless memory that replaces complex vector databases

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/rag" class="tag-badge">rag</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/memvid/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/memvid/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/memvid/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `memvid` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b3495bb325f5b1c1c5ae72c6e48239b9a89548ca7ea94acacb6a0939e3c27d4a` |

## Quick Start

1. **Start the server:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify the server is running:**

   ```bash
   curl http://localhost:8000/health
   ```

   Expected response: `{"status":"ok","framework":"Memvid","memvid_version":"2.0.x"}`

3. **Store a document in memory:**

   ```bash
   curl -X PUT http://localhost:8000/memory \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Memvid is a portable memory layer for AI agents with sub-5ms recall.",
       "title": "About Memvid",
       "tags": {"project": "memvid", "category": "overview"}
     }'
   ```

4. **Search memory:**

   ```bash
   curl -X POST http://localhost:8000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "portable memory layer", "top_k": 5}'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable              | Default          | Description                                            |
|-----------------------|------------------|--------------------------------------------------------|
| `MEMVID_PORT`         | `8000`           | Host port for the Memvid API                           |
| `MEMVID_DATA_DIR`     | `/app/data`      | Directory for memory file storage                      |
| `MEMVID_FILE`         | `default.mv2`    | Memory file name                                       |
| `MEMVID_EMBED_MODE`   | `local`          | Embedding mode: `local` (ONNX) or `api` (OpenAI)       |
| `MEMVID_LOG_LEVEL`    | `info`           | Log level: info, debug, warn, error                    |
| `OPENAI_API_KEY`      | —                | Required for api embed mode                            |

## Troubleshooting

| Symptom                                    | Likely Cause                        | Fix                                                         |
|--------------------------------------------|-------------------------------------|-------------------------------------------------------------|
| Container exits immediately                | pip install failure                 | Run `docker compose logs memvid` for details                |
| Connection refused on port 8000            | Container still building             | Wait 2-3 minutes for first build                            |
| `/health` returns `degraded` status        | memvid-sdk failed to initialize     | Check logs for ImportError or initialization issues         |
| `/search` returns empty results            | No documents stored yet             | Store a document via PUT /memory first                      |
| API embed mode not working                 | Missing OPENAI_API_KEY              | Set OPENAI_API_KEY in .env and set MEMVID_EMBED_MODE=api    |

## API Endpoints

Memvid exposes a REST API on port 8000:

| Endpoint   | Method | Description                                    |
|------------|--------|------------------------------------------------|
| `/health`  | GET    | Health check + version info                    |
| `/memory`  | PUT    | Store a document in memory                     |
| `/search`  | POST   | Search memory with semantic query              |
| `/reset`   | POST   | Delete and recreate the memory file            |

### PUT /memory

```json
{
  "text": "Document content to store...",
  "title": "Optional title",
  "uri": "optional://uri",
  "tags": {"key": "value"}
}
```

### POST /search

```json
{
  "query": "search query text",
  "top_k": 10,
  "snippet_chars": 200
}
```

## Health Check

```bash
curl http://localhost:8000/health
```

A healthy server returns:
```json
{
  "status": "ok",
  "framework": "Memvid",
  "memory_file": "default.mv2",
  "embed_mode": "local",
  "memvid_version": "2.0.x"
}
```

