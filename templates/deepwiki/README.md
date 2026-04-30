# DeepWiki — AI Knowledge Base

[DeepWiki](https://github.com/AsyncFuncAI/deepwiki-open) is an open-source AI knowledge base by AsyncFuncAI. Ingest, index, and search your documents and codebases with local LLMs and Retrieval-Augmented Generation (RAG). It provides both a web UI and a REST API for querying your knowledge.

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

## Managing DeepWiki

**View logs:**

```bash
docker compose logs -f deepwiki
```

**Reset data:**

```bash
docker compose down -v
docker compose up -d
```

## Troubleshooting

| Symptom                                    | Likely Cause              | Fix                                               |
|--------------------------------------------|---------------------------|---------------------------------------------------|
| API returns errors on ingest               | No LLM configured         | Set `OPENAI_API_KEY` in `.env`                     |
| Web UI not loading                         | Container still starting  | Wait 30s for startup — `docker compose logs -f`   |
| Search returns no results                  | No documents ingested     | Add a repository or document via the web UI       |
