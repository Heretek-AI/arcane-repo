# LiteLLM — Unified AI API Proxy

[LiteLLM](https://github.com/BerriAI/litellm) is a lightweight proxy that provides an OpenAI-compatible API endpoint for 100+ LLM providers. Route requests to OpenAI, Anthropic, Google Gemini, open-source models via Together AI, local models via Ollama, and many more — all through a single endpoint with consistent error handling, rate limiting, and spend tracking.

## What's Included (All-in-One)

| Service      | Port  | Description                                    |
|-------------|-------|------------------------------------------------|
| LiteLLM     | 4000  | OpenAI-compatible proxy API                   |
| PostgreSQL  | 5432  | Persistent database for spend logs and keys     |
| Prometheus  | 9090  | Metrics and observability dashboard            |

## Quick Start (3 Steps)

### 1. Create your environment file

```bash
cp .env.example .env
```

Open `.env` and set at least one provider API key. The defaults are fine to get started locally.

### 2. Start everything

```bash
docker compose up -d
```

Docker Compose starts all three services (LiteLLM, PostgreSQL, Prometheus) and waits for the database to be healthy before starting the proxy.

### 3. Test it

```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-liteLLM-master-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

> **Tip:** Get an API key from [platform.openai.com](https://platform.openai.com) (or [console.anthropic.com](https://console.anthropic.com) for Claude) and paste it into `.env` before testing.

## Services

### LiteLLM Proxy (port 4000)
OpenAI-compatible API. Health check endpoint:
```bash
curl http://localhost:4000/health/liveliness
```

Admin UI at `http://localhost:4000/ui` — use your `LITELLM_MASTER_KEY` to log in.

### PostgreSQL (port 5432)
Bundled PostgreSQL 16 stores spend logs, API keys, and model configs. Data persists in the `litellm_postgres_data` named volume.

### Prometheus (port 9090)
Pre-configured to scrape LiteLLM metrics. Access the Prometheus UI at `http://localhost:9090`. Metrics include request latency, token usage, error rates, and cost per model.

## Environment Variables

| Variable             | Default                          | Description                                 |
|----------------------|----------------------------------|---------------------------------------------|
| `LITELLM_MASTER_KEY` | `sk-liteLLM-master-key-change-me` | Admin auth key — change this in production! |
| `LITELLM_SALT_KEY`   | `sk-liteLLM-salt-key-change-me`   | Salt for encrypting stored credentials       |
| `OPENAI_API_KEY`      | *(blank)*                        | OpenAI API key                              |
| `ANTHROPIC_API_KEY`   | *(blank)*                        | Anthropic API key (Claude)                  |
| `GEMINI_API_KEY`       | *(blank)*                        | Google Gemini API key                        |
| `LITELLM_PORT`       | `4000`                           | Proxy host port                             |
| `LITELLM_DB_PORT`    | `5432`                           | PostgreSQL host port                        |
| `LITELLM_PROM_PORT`  | `9090`                           | Prometheus host port                        |

## Provider API Keys

LiteLLM auto-detects providers from environment variables — no config changes needed:

| Variable            | Provider          | Sign up                                    |
|---------------------|-------------------|--------------------------------------------|
| `OPENAI_API_KEY`    | OpenAI            | [platform.openai.com](https://platform.openai.com) |
| `ANTHROPIC_API_KEY` | Anthropic         | [console.anthropic.com](https://console.anthropic.com) |
| `GEMINI_API_KEY`    | Google            | [aistudio.google.com](https://aistudio.google.com) |
| `COHERE_API_KEY`    | Cohere            | [cohere.com](https://cohere.com)           |
| `TOGETHERAI_API_KEY` | Together AI       | [together.ai](https://together.ai)           |

Full provider list: [docs.litellm.ai/docs/providers](https://docs.litellm.ai/docs/providers)

## Managing the Stack

**View logs:**
```bash
docker compose logs -f litellm      # Proxy logs
docker compose logs -f db          # Database logs
docker compose logs -f prometheus  # Prometheus logs
```

**Restart after changing `.env`:**
```bash
docker compose restart litellm
```

**Stop everything:**
```bash
docker compose down
```

**Re-build:**
```bash
docker compose up -d --build
```

## Prometheus Metrics

Prometheus scrapes LiteLLM every 15 seconds with 15-day retention. Example queries in the Prometheus UI:

```
# Request rate per model
rate(litellm_requests_total[5m])

# Average latency per model
rate(litellm_request_duration_seconds_sum[5m]) / rate(litellm_request_duration_seconds_count[5m])

# Spend per key
litellm_spend_usd_total
```

## OpenAI-Compatible Endpoints

```
POST /v1/chat/completions   Chat completions
POST /v1/completions        Text completions
POST /v1/embeddings         Embeddings
GET  /v1/models             List available models
GET  /health/liveliness     Liveness check
GET  /health/readiness      Readiness check
```

Full API reference: [docs.litellm.ai/docs/proxy/api](https://docs.litellm.ai/docs/proxy/api)

## Hardened / Offline Deployments

LiteLLM also ships a hardened compose profile for restricted environments (read-only rootfs, no outbound network). See the [upstream Docker guide](https://github.com/BerriAI/litellm/tree/litellm_internal_staging/docker) for details.