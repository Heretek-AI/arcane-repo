# Pathway LLM App — RAG & AI Pipelines

[Pathway](https://github.com/pathwaycom/llm-app) provides ready-to-run templates for building RAG (Retrieval-Augmented Generation) applications, AI data pipelines, and enterprise search systems. Deploy document-aware Q&A, live data indexing, and real-time AI pipelines with a single container.

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

## Use Cases

Pathway's llm-app templates support:

- **Document Q&A**: Upload PDFs, text files, and web pages — query them with natural language
- **Real-time RAG**: Index live data streams (Kafka, databases, APIs) for always-fresh answers
- **Enterprise search**: Combine keyword and semantic search with LLM-powered summaries
- **Alerting pipelines**: Classify and route incoming data with LLM intelligence

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
