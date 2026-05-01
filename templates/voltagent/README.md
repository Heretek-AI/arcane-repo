# VoltAgent — Multi-Agent Framework for Autonomous AI Workflows

> **Python library — not a standalone Docker service.**
> [VoltAgent](https://github.com/VoltAgent/voltagent) is a multi-agent framework
> for building autonomous AI workflows.
> This Docker template provides a minimal informational API stub.
> Use `pip install voltagent` in your own application for full functionality.

## Quick Start

1. **Start the informational API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

## Full Python Usage (Recommended)

VoltAgent is primarily used as a Python library:

```bash
pip install voltagent
```

### Example

```python
from voltagent import Agent

# Define agents with custom tools
agent = Agent(
    name="workflow-agent",
    tools=[my_custom_tool],
    instructions="Automate the given workflow"
)

# Run autonomous workflows
# Full API at: https://github.com/VoltAgent/voltagent
```

## Configuration

| Variable           | Default  | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `VOLTAGENT_PORT`   | `8000`   | Host port for the informational API stub              |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the framework                        |
| `/guide`   | GET    | Usage instructions and quickstart examples                     |

## Managing

**View logs:**

```bash
docker compose logs -f voltagent
```

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                               |
|---------------------------------------------|---------------------------|-------------------------------------------------------------------|
| No workflow automation available            | This is a Docker stub     | Use `pip install voltagent` in your own Python project            |
| Container exits immediately                 | pip install failure       | Run `docker compose logs voltagent` for details                   |
| Want autonomous multi-agent workflows       | Using wrong deployment    | VoltAgent is a library — build your own orchestrator around it    |
