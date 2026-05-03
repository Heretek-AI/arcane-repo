---
title: "DeepWiki"
description: "Open-source AI knowledge base powered by AsyncFuncAI — ingest, index, and search your documents and codebases with local LLMs and Retrieval-Augmented Generation"
---

# DeepWiki

Open-source AI knowledge base powered by AsyncFuncAI — ingest, index, and search your documents and codebases with local LLMs and Retrieval-Augmented Generation

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/rag" class="tag-badge">rag</a> <a href="/categories/search" class="tag-badge">search</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/deepwiki/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/deepwiki/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/deepwiki/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `deepwiki` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c8cc170f552f6e78dcfe7f6be7e69d5e3040185faa8b8142ab1d9980962f9546` |

## Quick Start

1. **Set up environment variables and start:**

   ```bash
   cp .env.example .env
   # Edit .env — set OPENAI_API_KEY if using OpenAI, or configure a
   # local LLM endpoint.
   docker compose up -d
   ```

2. **Access the web UI:**

   Navigate to [http://localhost:3000](http://localhost:3000).

3. **Access the API:**

   ```bash
   curl http://localhost:8001/health
   ```

4. **Ingest a repository for indexing:**

   Use the web UI or the API to add code repositories or documents for RAG-based search and question answering.

## Configuration

Copy `.env.example` to `.env` and edit:

### Optional Variables

| Variable             | Default                    | Description                                          |
|----------------------|----------------------------|------------------------------------------------------|
| `DEEPWIKI_API_PORT`  | `8001`                     | Host port for the API server                         |
| `DEEPWIKI_UI_PORT`   | `3000`                     | Host port for the Next.js web UI                     |
| `LOG_LEVEL`          | `INFO`                     | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`   |
| `OPENAI_API_KEY`     | (empty)                    | OpenAI API key for LLM and embedding calls           |
| `EMBEDDING_MODEL`    | `text-embedding-3-small`   | Embedding model for document indexing                |

## Troubleshooting

| Symptom                                    | Likely Cause              | Fix                                               |
|--------------------------------------------|---------------------------|---------------------------------------------------|
| API returns errors on ingest               | No LLM configured         | Set `OPENAI_API_KEY` in `.env`                     |
| Web UI not loading                         | Container still starting  | Wait 30s for startup — `docker compose logs -f`   |
| Search returns no results                  | No documents ingested     | Add a repository or document via the web UI       |

## API Endpoints

DeepWiki exposes a REST API on port 8001:

| Endpoint    | Method | Description                   |
|-------------|--------|-------------------------------|
| `/health`   | GET    | Health check                  |
| `/api/ingest` | POST | Add a repository or document  |
| `/api/search` | POST | Semantic search               |
| `/api/query`  | POST | Question answering (RAG)      |

## Health Check

```bash
curl http://localhost:8001/health
```

