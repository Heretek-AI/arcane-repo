# ElizaOS — AI Agent Framework

[ElizaOS](https://elizaos.ai/) is an open-source AI agent framework for creating, deploying, and managing autonomous AI agents. It features a modular plugin architecture, multi-model support (OpenAI, Anthropic, Google Gemini), and cross-platform integrations.

## Quick Start

1. **Copy and edit the environment file:**

   ```bash
   cp .env.example .env
   # Set at least one LLM provider API key
   ```

2. **Start ElizaOS:**

   ```bash
   docker compose up -d
   ```

3. **Verify it's running:**

   ```bash
   curl http://localhost:3000/health
   ```

   Expected response: `{"status":"ok"}` or similar.

4. **Interact with your agent:**

   ```bash
   curl -X POST http://localhost:3000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello, who are you?"}'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable               | Default                     | Description                                    |
|------------------------|-----------------------------|------------------------------------------------|
| `ELIZAOS_PORT`         | `3000`                      | Host port for the ElizaOS API                  |
| `OPENAI_API_KEY`       | —                           | OpenAI API key (optional)                      |
| `ANTHROPIC_API_KEY`    | —                           | Anthropic API key (optional)                   |
| `GOOGLE_GEMINI_API_KEY`| —                           | Google Gemini API key (optional)               |
| `ELIZA_CHARACTER`      | —                           | Character name or path (optional)              |
| `LOG_LEVEL`            | `info`                      | Log level: `debug`, `info`, `warning`, `error` |
| `NODE_ENV`             | `production`                | Node environment                               |

### Characters

ElizaOS agents are defined by character files. Place custom character JSON files in the mounted `characters/` volume directory. Set `ELIZA_CHARACTER` to the character name (without `.json` extension) to load a specific character at startup.

## API Endpoints

| Endpoint        | Method | Description                       |
|-----------------|--------|-----------------------------------|
| `/health`       | GET    | Health check                      |
| `/api/chat`     | POST   | Send a message to your agent      |
| `/api/agents`   | GET    | List registered agents            |

## Health Check

```bash
curl http://localhost:3000/health
```

Expected response:
```json
{"status":"ok"}
```

## Managing ElizaOS

**View logs:**

```bash
docker compose logs -f elizaos
```

**Stop the agent:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull elizaos
docker compose up -d
```

## Troubleshooting

| Symptom                                    | Likely Cause                     | Fix                                                  |
|--------------------------------------------|----------------------------------|------------------------------------------------------|
| Agent returns empty responses              | No LLM API key configured        | Set at least one provider API key in `.env`          |
| `Connection refused` on port 3000          | Container still starting          | Wait a few seconds and retry                         |
| Agent doesn't use custom character         | Character file not found         | Verify character name matches a file in the volume   |
