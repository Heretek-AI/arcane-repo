---
title: "TensorZero"
description: "Open-source AI inference gateway — unified API for OpenAI, Anthropic, AWS Bedrock, Ollama, and more with fallbacks, load balancing, and observability"
---

# TensorZero

Open-source AI inference gateway — unified API for OpenAI, Anthropic, AWS Bedrock, Ollama, and more with fallbacks, load balancing, and observability

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/llm" class="tag-badge">llm</a> <a href="/categories/gateway" class="tag-badge">gateway</a> <a href="/categories/inference" class="tag-badge">inference</a> <a href="/categories/observability" class="tag-badge">observability</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tensorzero/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tensorzero/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tensorzero/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tensorzero` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ca8fa25cbeb282c4f52768feb7ff6fb92655da49e87f0989395a9aafc61e5afb` |

## Quick Start

1. **Create your config file:** TensorZero requires a `config/tensorzero.toml` to define your model gateways and functions. See [TensorZero's configuration guide](https://www.tensorzero.com/docs/reference/tensorzero.toml).

2. **Copy and edit the environment file:**

   ```bash
   cp .env.example .env
   # Add at least one API key
   ```

3. **Start the gateway:**

   ```bash
   docker compose up -d
   ```

4. **Verify it's running:**

   ```bash
   curl http://localhost:3000/health
   ```

   Expected response: `{"status":"ok"}`

5. **Route an inference:**

   ```bash
   curl -X POST http://localhost:3000/inference \
     -H "Content-Type: application/json" \
     -d '{
       "function_name": "basic_chat",
       "input": {
         "messages": [
           {"role": "user", "content": "Hello, world!"}
         ]
       }
     }'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                     | Default                            | Description                                     |
|------------------------------|------------------------------------|-------------------------------------------------|
| `TENSORZERO_PORT`            | `3000`                             | Host port for the gateway HTTP API              |
| `OPENAI_API_KEY`             | —                                  | OpenAI API key (optional)                       |
| `ANTHROPIC_API_KEY`          | —                                  | Anthropic API key (optional)                    |
| `GOOGLE_API_KEY`             | —                                  | Google / Gemini API key (optional)              |
| `AWS_ACCESS_KEY_ID`          | —                                  | AWS access key for Bedrock (optional)           |
| `AWS_SECRET_ACCESS_KEY`      | —                                  | AWS secret key for Bedrock (optional)           |
| `AWS_DEFAULT_REGION`         | `us-east-1`                        | AWS region for Bedrock                          |
| `OLLAMA_BASE_URL`            | `http://host.docker.internal:11434`| Local Ollama endpoint                           |
| `TENSORZERO_CLICKHOUSE_URL`  | —                                  | ClickHouse URL for inference observability      |

### Configuration File

TensorZero reads `/app/config/tensorzero.toml` from the mounted `./config` directory. Create this file to define your model gateways, functions, and provider routing. Example:

```toml
[gateways.default]
type = "openai"
model_name = "gpt-4o"
```

## Troubleshooting

| Symptom                                         | Likely Cause                       | Fix                                                    |
|-------------------------------------------------|------------------------------------|--------------------------------------------------------|
| `401 Unauthorized`                              | No API key configured              | Set at least one provider API key in `.env`            |
| `Connection refused` on port 3000               | Container still starting           | Wait a few seconds and retry                           |
| Model not found                                 | Missing config entry               | Add the model to `config/tensorzero.toml`              |
| Ollama connection error                         | Ollama not running locally         | Start Ollama or update `OLLAMA_BASE_URL`               |

## API Endpoints

| Endpoint       | Method | Description                                       |
|----------------|--------|---------------------------------------------------|
| `/health`      | GET    | Readiness check                                   |
| `/inference`   | POST   | Route an inference request                        |
| `/openai/*`    | POST   | OpenAI-compatible chat completions endpoint       |

## Health Check

```bash
curl http://localhost:3000/health
```

Expected response:
```json
{"status":"ok"}
```

