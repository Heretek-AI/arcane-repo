---
title: "Cognee"
description: "Open-source, graph-based RAG platform — extract, store, and query knowledge graphs from documents using LLMs, with support for multiple vector stores and LLM providers"
---

# Cognee

Open-source, graph-based RAG platform — extract, store, and query knowledge graphs from documents using LLMs, with support for multiple vector stores and LLM providers

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/rag" class="tag-badge">rag</a> <a href="/categories/llm" class="tag-badge">llm</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cognee/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cognee/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cognee/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cognee` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `58880f587670cab5bf916baefbb585fe799c7f7b9302005afad57ca3abf65af6` |

## Quick Start

1. **Set your API key and start the server:**

   ```bash
   cp .env.example .env
   # Edit .env — set OPENAI_API_KEY to a valid OpenAI API key
   docker compose up -d
   ```

   The first startup installs Cognee and its dependencies — this may take a minute.

2. **Verify the server is running:**

   ```bash
   curl http://localhost:8000/health
   ```

   Expected response: `{"status":"ok","framework":"cognee"}`

3. **Ingest a document:**

   ```bash
   curl -X POST http://localhost:8000/ingest \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity. Marie Curie was a Polish-born physicist and chemist who conducted pioneering research on radioactivity.",
       "dataset_name": "scientists"
     }'
   ```

4. **Query the knowledge graph:**

   ```bash
   curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"query": "Who developed the theory of relativity?"}'
   ```

5. **Search the graph:**

   ```bash
   curl -X POST http://localhost:8000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "Einstein"}'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### Mandatory Variables

| Variable          | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `OPENAI_API_KEY`  | OpenAI API key for LLM access and graph extraction. Get one at [platform.openai.com](https://platform.openai.com/api-keys). |

### Optional Variables

| Variable                       | Default                  | Description                                    |
|--------------------------------|--------------------------|------------------------------------------------|
| `COGNEE_PORT`                  | `8000`                   | Host port for the Cognee API                   |
| `COGNEE_LLM_MODEL`             | `gpt-4o-mini`            | LLM model for knowledge graph extraction       |
| `COGNEE_EMBEDDING_MODEL`       | `text-embedding-3-small` | Embedding model for vector storage             |
| `COGNEE_GRAPH_DATABASE_URL`    | *(empty)*                | URL for external graph DB (Neo4j)              |
| `COGNEE_GRAPH_DATABASE_USER`   | *(empty)*                | Graph database username                        |
| `COGNEE_GRAPH_DATABASE_PASSWORD` | *(empty)*              | Graph database password                        |
| `COGNEE_VECTOR_DATABASE_URL`   | *(empty)*                | URL for external vector store (Qdrant, etc.)   |

By default, Cognee uses embedded SQLite for graph storage and embedded LanceDB for vector storage. For production deployments, configure external Neo4j and Qdrant instances.

## Troubleshooting

| Symptom                                    | Likely Cause                           | Fix                                                 |
|--------------------------------------------|----------------------------------------|-----------------------------------------------------|
| Container exits immediately                | pip install failure                    | Run `docker compose logs cognee` for details        |
| Connection refused on port 8000            | Container still installing packages    | Wait 30–60 seconds for first startup                |
| `OPENAI_API_KEY is required` error         | API key not set in `.env`              | Add `OPENAI_API_KEY` to `.env` and restart          |
| `/ingest` returns 500                      | LLM API error or connectivity issue    | Verify `OPENAI_API_KEY` is valid                    |
| `/search` returns empty results            | No documents ingested yet              | Ingest a document first via the `/ingest` endpoint  |
| Slow first startup                         | pip install on every container create  | This is expected — packages are installed at startup |

## API Endpoints

Cognee exposes a REST API on port 8000:

| Endpoint       | Method | Description                              |
|----------------|--------|------------------------------------------|
| `/health`      | GET    | Health check                             |
| `/ingest`      | POST   | Ingest text content into the knowledge graph |
| `/search`      | POST   | Search the knowledge graph               |
| `/query`       | POST   | Ask a question answered from the graph   |

### Ingest Request

```json
{
  "text": "Document content to ingest...",
  "dataset_name": "my-dataset"
}
```

### Query Request

```json
{
  "query": "What is the relationship between Einstein and relativity?"
}
```

## Health Check

```bash
curl http://localhost:8000/health
```

A healthy server returns:
```json
{"status":"ok","framework":"cognee"}
```

