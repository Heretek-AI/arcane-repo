# AgentField — Multi-Agent Simulation Environment

> **Python library — not a standalone Docker service.**
> [AgentField](https://github.com/Agent-Field/agentfield) is a multi-agent
> simulation environment for training and evaluating AI agents.
> This Docker template provides a minimal informational API stub.
> Use `pip install agentfield` in your own research project for full functionality.

## Quick Start

1. **Start the informational API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8080/health
   ```

## Full Python Usage (Recommended)

AgentField is primarily used as a Python library in research projects:

```bash
pip install agentfield
```

### Example

```python
from agentfield import Environment

# Create a simulation environment
env = Environment(name="research-lab")

# Register agents and define interactions
# Full API at: https://github.com/Agent-Field/agentfield
```

## Configuration

| Variable           | Default  | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `AGENTFIELD_PORT`  | `8080`   | Host port for the informational API stub              |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the framework                        |
| `/guide`   | GET    | Usage instructions and quickstart examples                     |

## Managing

**View logs:**

```bash
docker compose logs -f agentfield
```

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                               |
|---------------------------------------------|---------------------------|-------------------------------------------------------------------|
| No simulation features available            | This is a Docker stub     | Use `pip install agentfield` in your own Python project           |
| Container exits immediately                 | pip install failure       | Run `docker compose logs agentfield` for details                  |
| Want multi-agent training and evaluation    | Using wrong deployment    | AgentField is a library — build your own research pipeline        |
