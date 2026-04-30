# Puck — AI Agent Orchestration

> **Informational template — project could not be fully verified for Docker deployment.**
> This template provides a minimal inline API wrapper for orchestration and health checks.
> For full functionality, install `puck` via pip in your project environment.

Puck orchestrates multi-agent AI workflows with configurable pipelines and event-driven execution. It lets you define agent roles, assign specialized models, chain tools, and manage complex task sequences programmatically.

## Quick Start

1. **Start the API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **Get usage guidance:**

   ```bash
   curl http://localhost:8000/guide
   ```

## Native Installation (Recommended)

```bash
pip install puck
# with extras:
pip install puck[openai,anthropic,all]
```

### Python Usage

```python
from puck import Agent, Workflow

agent = Agent(name="assistant", model="gpt-4")
wf = Workflow(agent)
result = wf.run("Analyze this dataset and generate a report")
```

### CLI Usage

```bash
puck run workflow.yaml
puck serve --port 8080
```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable     | Default     | Description                                    |
|--------------|-------------|------------------------------------------------|
| `PUCK_PORT`  | `8000`      | Host port for the informational API            |

## API Endpoints

| Endpoint   | Method | Description                         |
|------------|--------|-------------------------------------|
| `/health`  | GET    | Health check                        |
| `/guide`   | GET    | Usage guidance and CLI/Python examples |

## Managing Puck

**View logs:**

```bash
docker compose logs -f puck
```

**Stop the server:**

```bash
docker compose down
```

## Troubleshooting

| Symptom                              | Likely Cause                 | Fix                                                |
|--------------------------------------|------------------------------|----------------------------------------------------|
| No agent orchestration available      | This is an informational stub | Install `puck` via pip for full capabilities       |
| Container exits immediately           | pip install failure          | Run `docker compose logs puck` for details         |
| Need advanced pipeline features      | Not available in this stub   | Use pip-installed puck for complete functionality  |
