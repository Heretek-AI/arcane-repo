# MemOS

Self-hosted [MemOS](https://github.com/MemTensor/MemOS) (Memory Operating System) for LLMs and AI agents. MemOS provides scalable, self-evolving memory with Neo4j graph storage, Qdrant vector retrieval, and REST/Chat APIs.

## Deployment

1. Deploy this template from your Arcane registry.
2. In `.env`, provide your LLM API credentials:
   - `OPENAI_API_KEY`: API key for your LLM and embedding provider (OpenAI or compatible endpoint).
   - `NEO4J_PASSWORD`: Set a secure password for the Neo4j database instance.
3. (Optional) Adjust the service port (default: `8000`) or model parameters:
   - `MOS_CHAT_MODEL`: Chat model name (default: `gpt-4o-mini`).
   - `MOS_EMBEDDER_MODEL`: Embedding model (default: `text-embedding-3-small`).
   - `EMBEDDING_DIMENSION`: Vector dimensions matching your embedder (default: `1536`).
4. Start the stack. Once initialized:
   - The MemOS REST API is available at `http://<host>:8000`.
   - The interactive OpenAPI documentation is accessible at `http://<host>:8000/docs`.
   - Neo4j Browser is accessible at `http://<host>:7474`.
   - Qdrant REST API is accessible at `http://<host>:6333/dashboard`.

## Architecture & Storage

- **MemOS Server** (`ghcr.io/heretek-ai/memos:latest`): Fast FastAPI/Uvicorn server providing the core memory API, cube management, and agent memory scheduling.
- **Neo4j** (`neo4j:5.26-community`): Graph database storing entity relationships, hierarchy, and episodic memory structures. State is persisted in the `neo4j-data` volume.
- **Qdrant** (`qdrant/qdrant:latest`): High-performance vector database indexing semantic chunks and memories. State is persisted in the `qdrant-data` volume.
- **MemOS Data**: Working cubes and cached memory state are persisted in the `memos-data` volume.

## Production Notes

- **Initial Startup**: On the first start, Neo4j and Qdrant will initialize their storage directories before the MemOS API begins accepting requests. Healthchecks ensure MemOS only starts once both backends are healthy.
- **Model Providers**: MemOS defaults to OpenAI-compatible endpoints (`OPENAI_API_BASE=https://api.openai.com/v1`). You can point this to self-hosted Ollama, vLLM, or LiteLLM gateways by updating `OPENAI_API_BASE` and `MOS_CHAT_MODEL_PROVIDER`.
- **Backups**: Ensure regular snapshots of the named volumes `memos-data`, `neo4j-data`, and `qdrant-data`.
