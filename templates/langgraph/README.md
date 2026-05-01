# LangGraph — Framework for Stateful Multi-Actor Agents

> **Python framework — not a standalone Docker service.**
> [LangGraph](https://github.com/langchain-ai/langgraph) by LangChain is a Python
> framework for building stateful, multi-actor agent applications with LLMs.
> This Docker template provides a minimal informational API stub.
> Use `pip install langgraph` in your own Python project for full functionality.

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

LangGraph is primarily used as a Python library integrated into your own application:

```bash
pip install langgraph
```

### Example

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list[str]
    next: str | None

graph = StateGraph(AgentState)

def agent_node(state: AgentState) -> AgentState:
    # Your agent logic here
    state["messages"].append("Agent processed")
    state["next"] = END
    return state

graph.add_node("agent", agent_node)
graph.set_entry_point("agent")

compiled = graph.compile()
result = compiled.invoke({"messages": [], "next": None})
```

## Configuration

| Variable           | Default  | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `LANGGRAPH_PORT`   | `8000`   | Host port for the informational API stub              |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the framework                        |
| `/guide`   | GET    | Usage instructions and quickstart examples                     |

## Managing

**View logs:**

```bash
docker compose logs -f langgraph
```

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                               |
|---------------------------------------------|---------------------------|-------------------------------------------------------------------|
| No agent functionality available            | This is a Docker stub     | Use `pip install langgraph` in your own Python project            |
| Container exits immediately                 | pip install failure       | Run `docker compose logs langgraph` for details                   |
| Want to run multi-actor agents              | Using wrong deployment    | LangGraph is a library — build your own FastAPI app around it     |
