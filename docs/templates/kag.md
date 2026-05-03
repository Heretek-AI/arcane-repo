---
title: "KAG"
description: "OpenSPG Knowledge-Augmented Generation framework — build, query, and traverse knowledge graphs enhanced by LLM reasoning for more accurate and explainable AI responses"
---

# KAG

OpenSPG Knowledge-Augmented Generation framework — build, query, and traverse knowledge graphs enhanced by LLM reasoning for more accurate and explainable AI responses

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/rag" class="tag-badge">rag</a> <a href="/categories/llm" class="tag-badge">llm</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kag/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kag/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kag/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `kag` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `31ff1254c1b53823920db57c2bf448e23cee2d72bb4b290dce39e8e41dbd154f` |

## Quick Start

1. **Set your API key and start the server:**

   ```bash
   cp .env.example .env
   # Edit .env — set OPENAI_API_KEY to a valid OpenAI API key
   docker compose up -d
   ```

2. **Verify the server is running:**

   ```bash
   curl http://localhost:8000/health
   ```

   Expected response: `{"status":"ok","framework":"KAG","open_spg_version":"0.1.0"}`

3. **Build a knowledge base:**

   ```bash
   curl -X POST http://localhost:8000/build \
     -H "Content-Type: application/json" \
     -d '{
       "source": "Albert Einstein developed the theory of relativity. Marie Curie conducted pioneering research on radioactivity.",
       "knowledge_base": "scientists",
       "source_type": "text"
     }'
   ```

4. **Query the knowledge base:**

   ```bash
   curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What did Einstein develop?", "knowledge_base": "scientists"}'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### Mandatory Variables

| Variable       | Description                                                               |
|----------------|---------------------------------------------------------------------------|
| `OPENAI_API_KEY` | OpenAI API key for LLM access. Get one at [platform.openai.com](https://platform.openai.com/api-keys). |

### Optional Variables

| Variable                  | Default             | Description                                    |
|---------------------------|---------------------|------------------------------------------------|
| `KAG_PORT`                | `8000`              | Host port for the KAG API                      |
| `OPENAI_MODEL`            | `gpt-4o`            | LLM model for graph reasoning                  |
| `KAG_KNOWLEDGE_BASE_DIR`  | `/app/knowledge`    | Directory for knowledge base storage           |

## Troubleshooting

| Symptom                                    | Likely Cause                        | Fix                                               |
|--------------------------------------------|-------------------------------------|---------------------------------------------------|
| Container exits immediately                | pip install failure                 | Run `docker compose logs kag` for details         |
| Connection refused on port 8000            | Container still building from source| Wait 2-3 minutes for first build                  |
| `OPENAI_API_KEY is required` error         | API key not set in `.env`           | Add `OPENAI_API_KEY` to `.env` and restart        |
| `/build` returns 500                       | KAG builder module error            | Verify `OPENAI_API_KEY` is valid and KAG is built |
| `/query` returns empty results             | No knowledge base built yet         | Build a knowledge base via `/build` first         |

## API Endpoints

KAG exposes a REST API on port 8000:

| Endpoint    | Method | Description                                    |
|-------------|--------|------------------------------------------------|
| `/health`   | GET    | Health check                                   |
| `/build`    | POST   | Build a knowledge base from source text        |
| `/query`    | POST   | Query a knowledge base with a natural language question |

### Build Request

```json
{
  "source": "Document content to build the knowledge base from...",
  "knowledge_base": "my-kb",
  "source_type": "text"
}
```

### Query Request

```json
{
  "query": "What is the relationship between X and Y?",
  "knowledge_base": "my-kb"
}
```

## Health Check

```bash
curl http://localhost:8000/health
```

A healthy server returns:
```json
{"status":"ok","framework":"KAG","open_spg_version":"0.1.0"}
```

