# One API — LLM API Management Proxy

[One API](https://github.com/songquanpeng/one-api) provides a unified interface for 20+ LLM providers (OpenAI, Anthropic, Google, Azure, and more) with built-in load balancing, rate limiting, and cost tracking.

## Quick Start

1. **Start the server:**

   ```bash
   docker compose up -d
   ```

2. **Access the dashboard** at [http://localhost:3000](http://localhost:3000) and log in with the default credentials:
   - Username: `root`
   - Password: `123456`

3. **Add a channel** (API provider) via the Channels page — enter your API key for OpenAI, Anthropic, or any supported provider.

4. **Generate an access token** via the Tokens page, then use it as a drop-in replacement:

   ```bash
   curl http://localhost:3000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{
       "model": "gpt-4",
       "messages": [{"role": "user", "content": "Hello!"}]
     }'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable              | Default       | Description                                      |
|-----------------------|---------------|--------------------------------------------------|
| `ONE_API_PORT`        | `3000`        | Host port for the dashboard and API proxy        |
| `SQL_DSN`             | `one-api.db`  | Database connection — SQLite by default, MySQL supported |
| `SESSION_SECRET`      | (empty)       | Secret for session encryption — **required for production** |
| `LOG_SQL_DSN`         | `false`       | Log SQL queries for debugging                    |
| `BATCH_UPDATE_INTERVAL` | `5`         | Seconds between channel status updates           |
| `THEME`               | `default`     | UI theme: `default`, `berry`, or `air`           |
| `TZ`                  | `UTC`         | Server timezone                                  |

## MySQL Setup (Optional)

For production deployments, use MySQL instead of SQLite:

1. Add a MySQL service to `docker-compose.yml` or use an existing one
2. Set `SQL_DSN=user:password@tcp(mysql-host:3306)/one-api` in `.env`

## Supported Providers

One API supports 20+ providers including:

- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini, PaLM)
- Azure OpenAI
- Meta (Llama)
- Cohere, AI21, Replicate, and more

Full list: [github.com/songquanpeng/one-api#supported-models](https://github.com/songquanpeng/one-api#supported-models)

## API Endpoints

One API is an OpenAI-compatible proxy. All OpenAI endpoints are supported:

| Endpoint                        | Description                         |
|---------------------------------|-------------------------------------|
| `/v1/chat/completions`          | Chat completions (GPT, Claude, etc) |
| `/v1/completions`               | Text completions                    |
| `/v1/embeddings`                | Text embeddings                     |
| `/v1/models`                    | List available models               |

## Health Check

```bash
curl http://localhost:3000/api/status
```

A successful response returns `{"success": true, "message": "One API is running"}`.
