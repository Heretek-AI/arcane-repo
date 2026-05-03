---
title: "Pathway LLM App"
description: "Ready-to-run RAG, AI pipelines, and enterprise search templates — deploy document-aware Q&amp;A, live data indexing, and real-time AI with Pathway"
---

# Pathway LLM App

Ready-to-run RAG, AI pipelines, and enterprise search templates — deploy document-aware Q&amp;A, live data indexing, and real-time AI with Pathway

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/rag" class="tag-badge">rag</a> <a href="/categories/llm" class="tag-badge">llm</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/llm-app-pathway/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/llm-app-pathway/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/llm-app-pathway/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `llm-app-pathway` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b2126e91c742aef5024292b4108345fc92dd2e5aa3ee3aed391f2c58c9841744` |

## Quick Start

1. **Set your OpenAI API key:**

   ```bash
   cp .env.example .env
   # Edit .env and set PATHWAY_OPENAI_API_KEY to your OpenAI key
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the REST API** at [http://localhost:8000](http://localhost:8000)

4. **Query the built-in demo** (or upload your own documents):

   ```bash
   curl http://localhost:8000/v1/retrieval \
     -H "Content-Type: application/json" \
     -d '{"query": "What is Pathway?"}'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                      | Default      | Description                                |
|-------------------------------|--------------|--------------------------------------------|
| `PATHWAY_PORT`                | `8000`       | Host port for the API and dashboard        |
| `PATHWAY_HOST`                | `0.0.0.0`    | Container listen address                   |
| `PATHWAY_PERSISTENT_STORAGE`  | `/app/data`  | Directory for indexed data persistence     |
| `PATHWAY_LICENSE_KEY`         | `demo`       | License key (demo for evaluation)          |
| `PATHWAY_OPENAI_API_KEY`      | (empty)      | OpenAI API key for LLM features            |
| `PATHWAY_LOG_LEVEL`           | `INFO`       | Log verbosity                              |

## API Endpoints

| Endpoint                 | Method | Description                              |
|--------------------------|--------|------------------------------------------|
| `/v1/retrieval`          | POST   | Query the RAG pipeline                   |
| `/v1/index`              | POST   | Index new documents or URLs              |
| `/health`                | GET    | Service health check                     |

## Health Check

```bash
curl http://localhost:8000/health
```

A healthy server returns `{"status": "ok"}`.

Full documentation: [github.com/pathwaycom/llm-app](https://github.com/pathwaycom/llm-app)

