# Rowboat

[Rowboat](https://github.com/rowboatlabs/rowboat) — Open-source AI coworker with knowledge graph (13.2k★)

An AI coworker that connects to your email and meeting notes, builds a long-lived knowledge graph in plain Markdown, and uses that context to help you get work done — privately, on your machine.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Set your LLM API key:**

   Edit `.env` and set `OPENAI_API_KEY` (required for AI features).

3. **Start all services:**

   ```bash
   docker compose up -d
   ```

4. **Access the web UI:**

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Architecture

Rowboat is deployed as a **custom-build** template (MEM036: node-alpine multi-stage build). The Dockerfile clones upstream source at build time and produces a production image pushed to GHCR.

### Core Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `rowboat` | `ghcr.io/heretek-ai/arcane-repo/rowboat:latest` | 8080→8000 | Main Next.js app (custom-built from source) |
| `mongo` | `mongo:7` | 27017 | Document database |
| `redis` | `redis:7-alpine` | 6379 | Job queue / caching |
| `qdrant` | `qdrant/qdrant:latest` | 6333 | Vector database (RAG) |

### Upstream Changes (April 2026)

The upstream `rowboat_agents` and `copilot` services (previously in `docker-compose.yml` with `build:` contexts) no longer exist on the `main` branch. Rowboat has merged the agent runtime into the main Next.js app. Our template uses a single custom Dockerfile for the main app + Docker Hub images for infrastructure services.

## Configuration

Copy `.env.example` to `.env` and edit:

- `OPENAI_API_KEY` — required for AI features
- `ROWBOAT_PORT` — host port for web UI (default: 8080)
- `MONGO_USER` / `MONGO_PASSWORD` — MongoDB credentials
- `USE_RAG` — enable Qdrant vector search (requires QDRANT_API_KEY)
- `USE_COMPOSIO_TOOLS` — enable Composio tool integrations

## Optional Features

Rowboat supports many optional integrations (not required for basic use):

- **RAG (Retrieval-Augmented Generation):** Set `USE_RAG=true` and provide `QDRANT_API_KEY`
- **Composio Tools:** Set `USE_COMPOSIO_TOOLS=true` and provide `COMPOSIO_API_KEY`
- **Auth0 Authentication:** Set `USE_AUTH=true` and configure Auth0 environment variables
- **Chat Widget:** Configure `USE_CHAT_WIDGET` and related variables
- **Voice Input:** Add Deepgram API key (configured via app UI)
- **Voice Output:** Add ElevenLabs API key (configured via app UI)

## Key Features

- **Knowledge graph** from email, calendar, and meeting notes
- **Meeting prep** from prior decisions, threads, and open questions
- **Email drafting** grounded in history and commitments
- **PDF slide generation** from ongoing context
- **Live notes** that stay updated automatically
- **Obsidian-compatible** Markdown vault (inspect and edit any time)
- **Bring your own model** — local via Ollama or hosted API
- **MCP tools** — extend with search, databases, CRMs, and automations

## Build Info

- **Type:** custom-build (MEM036 — node-alpine multi-stage)
- **Base:** `node:18-alpine`
- **Build:** git clone upstream → npm ci → next build
- **Runtime:** Next.js standalone output with Python FastAPI health wrapper
- **Registry:** GHCR (`ghcr.io/heretek-ai/arcane-repo/rowboat:latest`)
