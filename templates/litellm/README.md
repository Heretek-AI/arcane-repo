# LiteLLM — Unified AI API Proxy

[LiteLLM](https://github.com/BerriAI/litellm) is a lightweight proxy that provides an OpenAI-compatible API endpoint for 100+ LLM providers. Route requests to OpenAI, Anthropic, Google Gemini, open-source models via Together AI, local models via Ollama, and many more — all through a single endpoint with consistent error handling, rate limiting, and spend tracking.

## Quick Start (3 Steps)

### 1. Create your environment file

```bash
cp .env.example .env
```

Open `.env` and set at least one provider API key. The defaults are fine to get started locally.

### 2. Start the proxy

```bash
docker compose up -d
```

That's it. LiteLLM is running at `http://localhost:4000`.

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

## Environment Variables

| Variable             | Default                              | Description                                      |
|----------------------|--------------------------------------|--------------------------------------------------|
| `LITELLM_MASTER_KEY` | `sk-liteLLM-master-key-change-me`   | Admin auth key — change this in production!      |
| `LITELLM_SALT_KEY`   | `sk-liteLLM-salt-key-change-me`      | Salt for encrypting stored credentials           |
| `DATABASE_URL`       | *(blank — uses SQLite)*             | PostgreSQL connection string for persisting data  |
| `OPENAI_API_KEY`     | *(blank)*                           | OpenAI API key                                   |
| `ANTHROPIC_API_KEY`  | *(blank)*                           | Anthropic API key (Claude)                       |
| `GEMINI_API_KEY`      | *(blank)*                           | Google Gemini API key                             |
| `LITELLM_PORT`       | `4000`                              | Host port for the proxy                          |

## Provider API Keys

Set at least one key in `.env`. LiteLLM auto-detects providers — no config changes needed:

| Variable            | Provider          | Sign up                                 |
|---------------------|-------------------|-----------------------------------------|
| `OPENAI_API_KEY`    | OpenAI            | [platform.openai.com](https://platform.openai.com) |
| `ANTHROPIC_API_KEY` | Anthropic         | [console.anthropic.com](https://console.anthropic.com) |
| `GEMINI_API_KEY`    | Google            | [aistudio.google.com](https://aistudio.google.com) |
| `COHERE_API_KEY`    | Cohere            | [cohere.com](https://cohere.com)        |
| `TOGETHERAI_API_KEY` | Together AI       | [together.ai](https://together.ai)        |

## Managing the Proxy

**View logs:**
```bash
docker compose logs -f litellm
```

**Restart after changing `.env`:**
```bash
docker compose restart litellm
```

**Stop the proxy:**
```bash
docker compose down
```

**Check health:**
```bash
curl http://localhost:4000/health/liveliness
```

## OpenAI-Compatible Endpoints

Once running, use any OpenAI SDK or HTTP client:

```
POST /v1/chat/completions   Chat completions
POST /v1/completions        Text completions
POST /v1/embeddings          Embeddings
GET  /v1/models             List available models
GET  /health/liveliness      Liveness check
GET  /health/readiness       Readiness check
```

Full API reference: [docs.litellm.ai/docs/proxy/api](https://docs.litellm.ai/docs/proxy/api)

## Admin UI

Access the LiteLLM admin dashboard at `http://localhost:4000/ui` — use your `LITELLM_MASTER_KEY` to log in. View key management, spend logs, and model configs.

## Persistence

Without `DATABASE_URL`, LiteLLM stores data in an internal SQLite database. Set it to a PostgreSQL connection string to persist across container recreations:

```bash
echo "DATABASE_URL=postgresql://user:password@host:5432/litellm" >> .env
docker compose restart litellm
```

## Hardened / Offline Deployments

LiteLLM also ships a hardened compose profile for restricted environments (read-only rootfs, no outbound network). See the [upstream Docker guide](https://github.com/BerriAI/litellm/tree/litellm_internal_staging/docker) for details.