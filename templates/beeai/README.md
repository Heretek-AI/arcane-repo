# BeeAI Framework — IBM Framework for Production-Ready AI Agents

> **Python/TypeScript framework — not a standalone Docker service.**
> [BeeAI Framework](https://github.com/i-am-bee/beeai-framework) by IBM is a
> framework for building production-ready AI agents in Python and TypeScript.
> This Docker template provides a minimal informational API stub.
> Use `pip install beeai-framework` or `npm install beeai-framework` in your own project.

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

BeeAI is primarily used as a Python or TypeScript library:

### Python

```bash
pip install beeai-framework
```

```python
from beeai_framework import Agent

agent = Agent(name="my-agent", instructions="You are a helpful assistant")
result = agent.run("Tell me about AI agents")
print(result)
```

### TypeScript

```bash
npm install beeai-framework
```

```typescript
import { Agent } from "beeai-framework";

const agent = new Agent({ name: "my-agent", instructions: "You are a helpful assistant" });
const result = await agent.run({ prompt: "Tell me about AI agents" });
console.log(result);
```

## Configuration

| Variable      | Default  | Description                                           |
|---------------|----------|-------------------------------------------------------|
| `BEEAI_PORT`  | `8000`   | Host port for the informational API stub              |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the framework                        |
| `/guide`   | GET    | Usage instructions and quickstart examples                     |

## Managing

**View logs:**

```bash
docker compose logs -f beeai
```

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                               |
|---------------------------------------------|---------------------------|-------------------------------------------------------------------|
| No agent functionality available            | This is a Docker stub     | Use `pip install beeai-framework` in your own project             |
| Container exits immediately                 | pip install failure       | Run `docker compose logs beeai` for details                       |
| Want production-grade agent workflows       | Using wrong deployment    | BeeAI is a library — integrate it into your own FastAPI app       |
