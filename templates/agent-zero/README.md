# Agent Zero — AI Agent Framework

[Agent Zero](https://github.com/frdel/agent-zero) is an open-source AI agent framework that enables autonomous agents with tool use, memory, multi-model support (OpenAI, Anthropic, Groq), and a built-in web interface for interactive control.

## Quick Start

1. **Copy and edit the environment file:**

   ```bash
   cp .env.example .env
   # Set at least one LLM provider API key
   ```

2. **Start Agent Zero:**

   ```bash
   docker compose up -d
   ```

3. **Access the web interface:**

   Open [http://localhost:5000](http://localhost:5000) in your browser.

4. **Verify the API:**

   ```bash
   curl http://localhost:5000/health
   ```

   Expected response: `{"status":"ok"}` or similar.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable          | Default                     | Description                                    |
|-------------------|-----------------------------|------------------------------------------------|
| `AGENT_ZERO_PORT` | `5000`                      | Host port for the Agent Zero UI and API        |
| `OPENAI_API_KEY`  | —                           | OpenAI API key (optional)                      |
| `ANTHROPIC_API_KEY`| —                          | Anthropic API key (optional)                   |
| `GROQ_API_KEY`    | —                           | Groq API key (optional)                        |
| `AGENT_ZERO_HOST` | `0.0.0.0`                   | Bind address                                   |
| `LOG_LEVEL`       | `info`                      | Log level: `debug`, `info`, `warning`, `error` |

## Services

| Service      | Image                         | Port  | Description                        |
|--------------|-------------------------------|-------|------------------------------------|
| `agent-zero` | `agent0ai/agent-zero:latest`  | 5000  | Agent Zero server with web UI      |

## API Endpoints

| Endpoint        | Method | Description                       |
|-----------------|--------|-----------------------------------|
| `/health`       | GET    | Health check                      |
| `/api/agents`   | GET    | List active agents                |
| `/api/tasks`    | POST   | Create a task for an agent        |
| `/api/chat`     | POST   | Send a message to an agent        |

## Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status":"ok"}
```

## Managing Agent Zero

**View logs:**

```bash
docker compose logs -f agent-zero
```

**Stop the agent:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull agent-zero
docker compose up -d
```

## Troubleshooting

| Symptom                                    | Likely Cause                     | Fix                                                  |
|--------------------------------------------|----------------------------------|------------------------------------------------------|
| Agent returns empty responses              | No LLM API key configured        | Set at least one provider API key in `.env`          |
| `Connection refused` on port 5000          | Container still starting          | Wait a few seconds and retry                         |
| Web interface not loading                  | Port conflict                    | Change `AGENT_ZERO_PORT` in `.env`                   |
