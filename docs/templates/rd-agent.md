---
title: "RD-Agent"
description: "Microsoft RD-Agent — automated research &amp; development agent that uses LLMs to drive the R&amp;D process autonomously, from idea formulation to code generation and evaluation"
---

# RD-Agent

Microsoft RD-Agent — automated research &amp; development agent that uses LLMs to drive the R&amp;D process autonomously, from idea formulation to code generation and evaluation

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/research" class="tag-badge">research</a> <a href="/categories/automation" class="tag-badge">automation</a> <a href="/categories/llm" class="tag-badge">llm</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rd-agent/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rd-agent/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rd-agent/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `rd-agent` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `cbc887199cef3287cdf80b91cfe0b3241ca2dac7d626072ee8f633ac11478646` |

## Quick Start

1. **Set your API key and start the server:**

   ```bash
   cp .env.example .env
   # Edit .env — set OPENAI_API_KEY to a valid OpenAI API key
   docker compose up -d
   ```

2. **Verify the server is running:**

   ```bash
   curl http://localhost:8000/health
   ```

   Expected response: `{"status":"ok","framework":"RD-Agent"}`

3. **Run RD-Agent on a research prompt:**

   ```bash
   curl -X POST http://localhost:8000/run \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Design a simple linear regression in Python"}'
   ```

4. **Run RD-Agent in evaluate mode:**

   ```bash
   curl -X POST http://localhost:8000/evaluate \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Evaluate the linear regression implementation"}'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### Mandatory Variables

| Variable       | Description                                                               |
|----------------|---------------------------------------------------------------------------|
| `OPENAI_API_KEY` | OpenAI API key for LLM access. Get one at [platform.openai.com](https://platform.openai.com/api-keys). |

### Optional Variables

| Variable       | Default   | Description                                    |
|----------------|-----------|------------------------------------------------|
| `RDAGENT_PORT` | `8000`    | Host port for the RD-Agent API                 |
| `OPENAI_MODEL` | `gpt-4o`  | LLM model for driving the R&D process          |

## Troubleshooting

| Symptom                                    | Likely Cause                        | Fix                                               |
|--------------------------------------------|-------------------------------------|---------------------------------------------------|
| Container exits immediately                | pip install failure                 | Run `docker compose logs rd-agent` for details    |
| Connection refused on port 8000            | Container still installing packages | Wait 30-60 seconds for first startup              |
| `OPENAI_API_KEY is required` error         | API key not set in `.env`           | Add `OPENAI_API_KEY` to `.env` and restart        |
| `/run` returns 500                         | LLM API error                       | Verify `OPENAI_API_KEY` is valid                  |
| `rdagent` command not found               | Build failure                       | Check build logs for errors                       |

## API Endpoints

RD-Agent exposes a REST API on port 8000:

| Endpoint    | Method | Description                                        |
|-------------|--------|----------------------------------------------------|
| `/health`   | GET    | Health check                                       |
| `/version`  | GET    | Get installed RD-Agent version                     |
| `/run`      | POST   | Run RD-Agent on a research prompt                  |
| `/evaluate` | POST   | Evaluate an existing result or approach            |

### Run Request

```json
{
  "prompt": "Design a linear regression in Python",
  "workspace": "/workspace"
}
```

### Run Response

```json
{
  "status": "completed",
  "exit_code": 0,
  "stdout": "Running RD-Agent on: Design a linear regression in Python...",
  "stderr": ""
}
```

## Health Check

```bash
curl http://localhost:8000/health
```

A healthy server returns:
```json
{"status":"ok","framework":"RD-Agent"}
```

