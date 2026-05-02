# Jina — Cloud-Native AI Serving

[Jina](https://github.com/jina-ai/serve) provides a cloud-native framework for building multimodal AI applications. Deploy embeddings, rerankers, neural search pipelines, and custom executors with a scalable gateway + executor architecture.

## Quick Start

1. **Start the services:**

   ```bash
   docker compose up -d
   ```

2. **Check the gateway is running:**

   ```bash
   curl http://localhost:8080/status
   ```

3. **Send a test request** (requires a Flow definition — see the [Jina docs](https://docs.jina.ai)):

   ```bash
   curl http://localhost:8080/post \
     -H "Content-Type: application/json" \
     -d '{"data": [{"text": "Hello world"}]}'
   ```

## Architecture

This template uses a two-service architecture:

- **Gateway** (`jina-gateway`): The public-facing entry point that accepts client requests and routes them to executors
- **Executor** (`jina-executor`): The worker service that processes documents, runs models, and returns results

Communication between gateway and executor uses gRPC by default (configurable via `JINA_PROTOCOL`).

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable             | Default  | Description                                      |
|----------------------|----------|--------------------------------------------------|
| `JINA_GATEWAY_PORT`  | `8080`   | Host port for the gateway API                    |
| `JINA_PROTOCOL`      | `grpc`   | Gateway-executor protocol (grpc, http, websocket)|
| `JINA_LOG_LEVEL`     | `INFO`   | Log verbosity level                              |

## Using with Custom Flows

To deploy a custom Jina Flow with specific executors:

1. Create a Flow YAML file and mount it to `/workspace`
2. Update the gateway and executor commands in `docker-compose.yml`
3. Use the Jina CLI to manage flows:

   ```bash
   docker compose exec jina-gateway jina flow --help
   ```

## Common Use Cases

- **Document search**: Index and search documents with semantic understanding
- **Cross-modal retrieval**: Search images by text, or text by images
- **RAG pipelines**: Build retrieval-augmented generation backends
- **API unification**: Proxy multiple AI models behind a single endpoint

Full documentation: [docs.jina.ai](https://docs.jina.ai)
