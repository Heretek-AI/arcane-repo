# LiteLLM — Unified AI API Proxy

[LiteLLM](https://github.com/BerriAI/litellm) is a lightweight proxy that provides an OpenAI-compatible API endpoint for 100+ LLM providers. Route requests to OpenAI, Anthropic, Google Gemini, open-source models via Together AI, local models via Ollama, and many more — all through a single endpoint with consistent error handling, rate limiting, and spend tracking.

## Quick Start

1. **Configure your providers:**

   Copy `.env.example` to `.env`, then uncomment and set at least one provider API key:

   ```bash
   cp .env.example .env
   # Edit .env — set OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
   ```

2. **Configure models in `config.yaml`:**

   Edit `config.yaml` to uncomment the model entries for the providers you are using. Each entry maps a model name to a provider-specific model string.

3. **Start the proxy:**

   ```bash
   docker compose up -d
   ```

4. **Test the proxy:**

   ```bash
   curl http://localhost:4000/v1/chat/completions \
     -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gpt-4o",
       "messages": [{"role": "user", "content": "Hello!"}]
     }'
   ```

## Configuration

### Environment Variables

| Variable               | Default                     | Description                                        |
|------------------------|-----------------------------|----------------------------------------------------|
| `LITELLM_PORT`         | `4000`                      | Host port for the proxy API                        |
| `LITELLM_MASTER_KEY`   | `sk-liteLLM-master-key`     | Master key for admin access and API auth           |
| `LITELLM_SALT_KEY`     | `sk-liteLLM-salt-key`       | Salt for encrypting stored credentials             |
| `DATABASE_URL`         | *(empty — uses SQLite)*     | PostgreSQL connection string for persisting data   |

### Provider API Keys

Set at least one provider key in your `.env` file. LiteLLM reads these automatically:

| Variable             | Provider                 |
|----------------------|--------------------------|
| `OPENAI_API_KEY`     | OpenAI                   |
| `ANTHROPIC_API_KEY`  | Anthropic                |
| `GEMINI_API_KEY`     | Google Gemini            |
| `COHERE_API_KEY`     | Cohere                   |
| `TOGETHERAI_API_KEY` | Together AI              |

### Model Configuration (`config.yaml`)

The `config.yaml` file defines which models are available through the proxy. Each entry has:

```yaml
- model_name: gpt-4o              # The name your app sends in requests
  litellm_params:
    model: openai/gpt-4o          # The provider-specific model identifier
    api_key: os.environ/OPENAI_API_KEY  # Reads from environment
```

The included `config.yaml` contains commented examples for OpenAI, Anthropic, Google Gemini, Together AI, Cohere, and local Ollama models. Uncomment the ones you need and restart the container.

### Router Settings

The proxy includes configurable routing:

| Setting             | Default         | Description                                      |
|---------------------|-----------------|--------------------------------------------------|
| `routing_strategy`  | `usage-based`   | How to distribute requests across models         |
| `num_retries`       | `2`             | Number of retries on failure                     |
| `allowed_fails`     | `3`             | Fails before marking an endpoint as unhealthy    |
| `fallbacks`         | `[]`            | Models to fall back to if primary fails          |

## Persistence

By default, LiteLLM stores spend logs and key metadata in a SQLite database inside the container volume (`litellm_data`). For production, set `DATABASE_URL` to a PostgreSQL connection string to persist across container recreations.

## API Endpoints

LiteLLM exposes an OpenAI-compatible API on port 4000:

| Endpoint                     | Method | Description                    |
|------------------------------|--------|--------------------------------|
| `/v1/chat/completions`       | POST   | Chat completions               |
| `/v1/completions`            | POST   | Text completions               |
| `/v1/embeddings`             | POST   | Generate embeddings            |
| `/v1/models`                 | GET    | List configured models         |
| `/health/liveliness`         | GET    | Health check                   |
| `/health/readiness`          | GET    | Readiness check                |

Full API reference: [docs.litellm.ai/docs/proxy/api](https://docs.litellm.ai/docs/proxy/api)

## Managing the Proxy

**View logs:**

```bash
docker compose logs -f litellm
```

**Restart after config change:**

```bash
docker compose restart litellm
```

**Check spend logs (requires PostgreSQL):**

The proxy tracks token usage, API call volume, and spend per key. Access the admin UI at `http://localhost:4000/ui` with your master key.

## Health Check

```bash
curl http://localhost:4000/health/liveliness
```

A successful response returns `{"status": "ok"}`.
