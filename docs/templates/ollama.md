---
title: "Ollama"
description: "Local LLM inference server with Ollama — pull and run open-source models like Llama 3, Mistral, and Gemma on your own hardware"
---

# Ollama

Local LLM inference server with Ollama — pull and run open-source models like Llama 3, Mistral, and Gemma on your own hardware

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/llm" class="tag-badge">llm</a> <a href="/categories/inference" class="tag-badge">inference</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ollama/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ollama/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ollama/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `ollama` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1b06674a0d30a9401eac9d4694fc62e0e431343c470378f162c5cf842f70f8c3` |

## Quick Start

1. **Start the server:**

   ```bash
   docker compose up -d
   ```

2. **Pull a model:**

   ```bash
   docker compose exec ollama ollama pull llama3.1:8b
   ```

3. **Run inference:**

   ```bash
   docker compose exec ollama ollama run llama3.1:8b "What is the capital of France?"
   ```

   Or via the REST API:

   ```bash
   curl http://localhost:11434/api/generate -d '{
     "model": "llama3.1:8b",
     "prompt": "What is the capital of France?",
     "stream": false
   }'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                  | Default   | Description                                      |
|---------------------------|-----------|--------------------------------------------------|
| `OLLAMA_HOST_PORT`        | `11434`   | Host port for the Ollama API                     |
| `OLLAMA_MODEL`            | `llama3.1:8b` | Default model to pull                       |
| `OLLAMA_KEEP_ALIVE`       | `5m`      | How long to keep models in memory after last use |
| `OLLAMA_NUM_PARALLEL`     | `1`       | Parallel request-processing threads              |
| `OLLAMA_MAX_LOADED_MODELS`| `1`       | Maximum models kept in memory simultaneously     |

## API Endpoints

Ollama exposes a REST API on port 11434:

| Endpoint             | Method | Description                    |
|----------------------|--------|--------------------------------|
| `/api/generate`      | POST   | Generate a completion          |
| `/api/chat`          | POST   | Generate a chat completion     |
| `/api/embed`         | POST   | Generate text embeddings       |
| `/api/tags`          | GET    | List downloaded models         |
| `/api/pull`          | POST   | Download a model               |
| `/api/ps`            | GET    | List loaded models             |

Full API reference: [github.com/ollama/ollama/blob/main/docs/api.md](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Health Check

```bash
curl http://localhost:11434/api/tags
```

A successful response returns a JSON object with a `models` array (may be empty if no models are pulled yet — the server is still healthy).

