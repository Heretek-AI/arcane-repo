# LangChain — LangServe API Server

[LangServe](https://python.langchain.com/docs/langserve) helps developers deploy [LangChain](https://www.langchain.com) chains and runnables as production-ready REST APIs. This template runs a FastAPI server powered by LangServe, exposing chat models, chains, and agents through standard endpoints with built-in streaming, batching, and health checks.

Unlike traditional services, LangServe is **code-defined** — you configure the chain logic by setting environment variables. The server starts with a configurable chat model and provides ready-to-use `/chat/invoke`, `/chat/stream`, and `/chat/batch` endpoints.

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

   Expected response: `{"status":"ok","model":"gpt-4o-mini","framework":"LangChain"}`

3. **Send a chat message:**

   ```bash
   curl -X POST http://localhost:8000/chat/invoke \
     -H "Content-Type: application/json" \
     -d '{"input": {"messages": [{"role": "user", "content": "What is the capital of France?"}]}}'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### Mandatory Variables

| Variable          | Description                                                                    |
|-------------------|--------------------------------------------------------------------------------|
| `OPENAI_API_KEY`  | OpenAI API key for LLM access. Generate at [platform.openai.com/api-keys](https://platform.openai.com/api-keys). |

### Optional Variables

| Variable                  | Default               | Description                                              |
|---------------------------|-----------------------|----------------------------------------------------------|
| `MODEL_NAME`              | `gpt-4o-mini`         | Model to use for chat completions                        |
| `LANGCHAIN_PORT`          | `8000`                | Host port for the LangServe API                          |
| `LANGCHAIN_TRACING_V2`    | `false`               | Enable LangSmith trace collection                        |
| `LANGCHAIN_API_KEY`       | *(empty)*             | LangSmith API key (needed for tracing)                   |
| `LANGCHAIN_PROJECT`       | `Arcane-LangServe`    | LangSmith project name for trace grouping                |

### Model Provider Configuration

By default, the server uses OpenAI via `OPENAI_API_KEY`. To use other providers, modify the `server.py` code inside the docker-compose.yml or build a custom Docker image.

**Anthropic:**

```python
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-3-5-sonnet-20241022")
```

**Ollama (local):**

```python
from langchain_ollama import ChatOllama
model = ChatOllama(model="llama3.1:8b")
```

**Azure OpenAI:**

```python
from langchain_openai import AzureChatOpenAI
model = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2024-02-15-preview"
)
```

## API Endpoints

LangServe auto-generates the following endpoints for the registered chain (at `/chat/`):

| Endpoint              | Method | Description                                |
|-----------------------|--------|--------------------------------------------|
| `/health`             | GET    | Health check — returns server status       |
| `/chat/invoke`        | POST   | Invoke the chain (single request)          |
| `/chat/batch`         | POST   | Batch invoke with multiple inputs          |
| `/chat/stream`        | POST   | Stream responses token by token            |
| `/chat/stream_log`    | POST   | Stream with structured run logs            |
| `/chat/input_schema`  | GET    | JSON Schema for the chain input            |
| `/chat/output_schema` | GET    | JSON Schema for the chain output           |
| `/chat/config_schema` | GET    | JSON Schema for run configuration          |
| `/docs`               | GET    | Swagger UI documentation                   |

Full API reference: [python.langchain.com/docs/langserve](https://python.langchain.com/docs/langserve)

### Invoke Examples

**Single message:**

```bash
curl -X POST http://localhost:8000/chat/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": {"messages": [{"role": "user", "content": "Explain quantum computing in one sentence"}]}}'
```

**Stream a response:**

```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"input": {"messages": [{"role": "user", "content": "Write a haiku about Docker"}]}}'
```

**Batch multiple requests:**

```bash
curl -X POST http://localhost:8000/chat/batch \
  -H "Content-Type: application/json" \
  -d '{"inputs": [{"messages": [{"role": "user", "content": "Say hello"}]}, {"messages": [{"role": "user", "content": "Say goodbye"}]}]}'
```

## Health Check

```bash
curl http://localhost:8000/health
```

A healthy server returns:
```json
{"status":"ok","model":"gpt-4o-mini","framework":"LangChain"}
```

## Managing the Server

**View logs:**

```bash
docker compose logs -f langserve
```

**Restart after configuration changes:**

```bash
docker compose restart langserve
```

**Upgrade to the latest LangChain packages:**

```bash
docker compose up -d --force-recreate langserve
```

This recreates the container, which runs `pip install` on startup with the latest package versions.

## Extending the Server

To add custom chains, tools, or agent logic, modify the `server.py` code inside the `command` section of `docker-compose.yml`. Common extensions:

**Add a system prompt:**

```python
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful coding assistant."),
    ("human", "{input}")
])
chain = prompt | model
add_routes(app, chain, path="/chat")
```

**Add a retrieval chain (RAG):**

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

vectorstore = FAISS.load_local("/app/data/index", OpenAIEmbeddings())
retriever = vectorstore.as_retriever()
rag_chain = {"context": retriever, "question": lambda x: x["question"]} | prompt | model
add_routes(app, rag_chain, path="/rag")
```

**Multiple chains at different paths:**

```python
add_routes(app, model, path="/chat")
add_routes(app, rag_chain, path="/rag")
add_routes(app, agent_executor, path="/agent")
```

## Troubleshooting

| Symptom                                          | Likely Cause                                    | Fix                                                       |
|--------------------------------------------------|-------------------------------------------------|-----------------------------------------------------------|
| `OPENAI_API_KEY is required` error               | API key not set in `.env`                       | Add `OPENAI_API_KEY` to `.env` and restart                |
| `401 AuthenticationError` from OpenAI            | Invalid or expired API key                      | Verify the key at [platform.openai.com](https://platform.openai.com) |
| `ModuleNotFoundError: No module named 'langchain_*'` | Provider-specific package not installed    | Add `pip install langchain-anthropic` (or equivalent) to the command |
| Container exits immediately                      | pip install failure or startup error            | Run `docker compose logs langserve` for details           |
| Connection refused on port 8000                  | Container still starting (pip install takes time)| Wait 30–60 seconds for first startup (packages must install) |
| `/chat/invoke` returns 500                       | Invalid input format or API error               | Check with a minimal "hello" message first                |
