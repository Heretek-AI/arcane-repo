---
title: "Agent Zero"
description: "Open-source AI agent framework — autonomous agents with tool use, memory, multi-model support, and a built-in web interface"
---

# Agent Zero

Open-source AI agent framework — autonomous agents with tool use, memory, multi-model support, and a built-in web interface

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/framework" class="tag-badge">framework</a> <a href="/categories/tools" class="tag-badge">tools</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agent-zero/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agent-zero/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agent-zero/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `agent-zero` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ba634cc41042d569b236264c3f77840faf3fd3f554a9fd5d90006b9841743ea4` |

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

## Troubleshooting

| Symptom                                    | Likely Cause                     | Fix                                                  |
|--------------------------------------------|----------------------------------|------------------------------------------------------|
| Agent returns empty responses              | No LLM API key configured        | Set at least one provider API key in `.env`          |
| `Connection refused` on port 5000          | Container still starting          | Wait a few seconds and retry                         |
| Web interface not loading                  | Port conflict                    | Change `AGENT_ZERO_PORT` in `.env`                   |

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

