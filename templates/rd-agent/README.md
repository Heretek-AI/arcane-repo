# RD-Agent — Automated Research & Development Agent

[RD-Agent](https://github.com/microsoft/RD-Agent) by Microsoft is an automated research and development agent that uses LLMs to drive the R&D process autonomously — from idea formulation and literature review to code generation, experimentation, and evaluation.

> **Note:** RD-Agent is primarily a CLI tool. This template wraps it as a REST API server for containerized deployment. The `rdagent` CLI is also available inside the container.

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

## Using the CLI Directly

Since RD-Agent is primarily a CLI tool, you can also execute it directly in the container:

```bash
docker exec -it rd-agent rdagent "Your research prompt"
```

## Managing RD-Agent

**View logs:**

```bash
docker compose logs -f rd-agent
```

**Restart after configuration changes:**

```bash
docker compose restart rd-agent
```

## Troubleshooting

| Symptom                                    | Likely Cause                        | Fix                                               |
|--------------------------------------------|-------------------------------------|---------------------------------------------------|
| Container exits immediately                | pip install failure                 | Run `docker compose logs rd-agent` for details    |
| Connection refused on port 8000            | Container still installing packages | Wait 30-60 seconds for first startup              |
| `OPENAI_API_KEY is required` error         | API key not set in `.env`           | Add `OPENAI_API_KEY` to `.env` and restart        |
| `/run` returns 500                         | LLM API error                       | Verify `OPENAI_API_KEY` is valid                  |
| `rdagent` command not found               | Build failure                       | Check build logs for errors                       |
