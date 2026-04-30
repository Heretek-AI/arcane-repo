# DocsGPT — Documentation Q&A Platform

[DocsGPT](https://docsgpt.ai/) is an open-source platform that turns your documentation, codebase, and knowledge base into a natural-language Q&A system. Index your content and ask questions with LLM-powered answers and source citations.

## Quick Start

1. **Copy and edit the environment file:**

   ```bash
   cp .env.example .env
   # Set SECRET_KEY, DOCSGPT_DB_PASSWORD, and at least one LLM provider key
   ```

2. **Start the services:**

   ```bash
   docker compose up -d
   ```

3. **Access the web UI:**

   Open [http://localhost:3000](http://localhost:3000) in your browser.

4. **Verify the API:**

   ```bash
   curl http://localhost:3000/api/health
   ```

   Expected response: `{"status":"ok"}` or similar health indication.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable               | Default                               | Description                                     |
|------------------------|---------------------------------------|-------------------------------------------------|
| `SECRET_KEY`           | — **(required)**                      | Application secret key (generate with `openssl rand -hex 32`) |
| `DOCSGPT_DB_PASSWORD`  | — **(required)**                      | PostgreSQL password                             |
| `DOCSGPT_DB_USER`      | `docsgpt`                             | PostgreSQL user                                 |
| `DOCSGPT_DB_NAME`      | `docsgpt`                             | PostgreSQL database name                        |
| `DOCSGPT_PORT`         | `3000`                                | Host port for the web UI and API                |
| `DOCSGPT_DB_PORT`      | `5432`                                | Host port for PostgreSQL                        |
| `LLM_NAME`             | `gpt-4o`                              | LLM model to use for answering questions        |
| `OPENAI_API_KEY`       | —                                     | OpenAI API key (required for OpenAI models)     |
| `OLLAMA_BASE_URL`      | `http://host.docker.internal:11434`   | Local Ollama endpoint                           |
| `EMBEDDINGS_NAME`      | —                                     | Override embedding model (optional)             |
| `EMBEDDINGS_KEY`       | —                                     | Embedding API key (optional)                    |
| `APP_ENV`              | `production`                          | Application environment                         |

## API Endpoints

| Endpoint                 | Method | Description                                |
|--------------------------|--------|--------------------------------------------|
| `/api/health`            | GET    | Health check                               |
| `/api/train`             | POST   | Index documentation (train on new content) |
| `/api/ask`               | POST   | Ask a question against indexed content     |
| `/api/training-examples` | GET    | List indexed documents                     |
| `/api/chat`              | POST   | Chat with context (conversation mode)      |

### Ask a Question

```bash
curl -X POST http://localhost:3000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I install the CLI?",
    "history": []
  }'
```

### Index Documentation

```bash
curl -X POST http://localhost:3000/api/train \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com/getting-started"
  }'
```

## Health Check

```bash
curl http://localhost:3000/api/health
```

Expected response:
```json
{"status":"ok"}
```

## Managing DocsGPT

**View logs:**

```bash
docker compose logs -f docsgpt
```

**Re-index content:**

```bash
curl -X POST http://localhost:3000/api/train \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-docs-site.com"}'
```

**Stop the services:**

```bash
docker compose down
```

## Troubleshooting

| Symptom                                    | Likely Cause                      | Fix                                                  |
|--------------------------------------------|-----------------------------------|------------------------------------------------------|
| `Connection refused` on port 3000          | Container still starting          | Wait and retry — first start can take 60s+           |
| `401 Unauthorized` when asking questions   | No API key configured             | Set `OPENAI_API_KEY` in `.env`                       |
| Answers are low quality                    | Wrong model or no RAG content     | Index documentation first, or change `LLM_NAME`      |
| Database connection error                  | Wrong DB credentials              | Verify `DOCSGPT_DB_PASSWORD` matches between services|
| Ollama returns 404                         | Model not pulled                  | Run `docker exec docsgpt ollama pull <model>`        |
