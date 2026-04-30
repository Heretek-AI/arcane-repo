# Memvid — Serverless Memory Layer for AI Agents

[Memvid](https://github.com/memvid/memvid) is a portable, single-file memory
layer for AI agents. It packages your data, embeddings, search structure, and
metadata into a single `.mv2` file — replacing complex RAG pipelines and
vector databases with instant retrieval and long-term memory.

> **Note:** This template builds Memvid from source using a custom Dockerfile.
> The first build may take several minutes.

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

## Using the Native CLI

For full functionality, use the Memvid CLI directly:

```bash
# Install globally
npm install -g memvid-cli

# Create a memory
memvid create my-memory.mv2

# Add documents
memvid put my-memory.mv2 --input document.pdf

# Search
memvid find my-memory.mv2 --query "search terms"
```

Or in Python:

```python
from memvid_sdk import Memvid

mem = Memvid.create("knowledge.mv2")
mem.put_bytes(b"document content", title="My Doc")
mem.commit()
results = mem.search("search query")
```

## Managing Memvid

**View logs:**

```bash
docker compose logs -f memvid
```

**Reset memory (clears all stored data):**

```bash
curl -X POST http://localhost:8000/reset
```

**Restart after configuration changes:**

```bash
docker compose restart memvid
```

## Troubleshooting

| Symptom                                    | Likely Cause                        | Fix                                                         |
|--------------------------------------------|-------------------------------------|-------------------------------------------------------------|
| Container exits immediately                | pip install failure                 | Run `docker compose logs memvid` for details                |
| Connection refused on port 8000            | Container still building             | Wait 2-3 minutes for first build                            |
| `/health` returns `degraded` status        | memvid-sdk failed to initialize     | Check logs for ImportError or initialization issues         |
| `/search` returns empty results            | No documents stored yet             | Store a document via PUT /memory first                      |
| API embed mode not working                 | Missing OPENAI_API_KEY              | Set OPENAI_API_KEY in .env and set MEMVID_EMBED_MODE=api    |
