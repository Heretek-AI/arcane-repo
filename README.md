# Arcane Template Registry

A curated registry of Docker Compose templates for Arcane. Template folders serve as the single source of truth — CI validates their structure, assembles `registry.json` from on-disk state, and publishes it to GitHub Pages. No manual registry edits, no stale entries, no sync drift between folders and the index.

## Badges

![Validate](https://github.com/Heretek-AI/arcane-repo/actions/workflows/validate.yml/badge.svg)
![Deploy](https://github.com/Heretek-AI/arcane-repo/actions/workflows/deploy.yml/badge.svg)

## Quick Start

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add, modify, or remove templates.

## How It Works

1. Each template lives in its own directory under `templates/` with an `arcane.json` metadata file and a `docker-compose.yml`.
2. All **6 templates** are available — see the [Templates](#templates) section below.
3. A CI workflow (`validate.yml`) runs on every PR touching `templates/**`, executing `node scripts/build-registry.js --validate-only` to check structure, metadata, and file integrity.
4. On push to `main`, the `deploy.yml` workflow runs `node scripts/build-registry.js` to assemble `registry.json` and publishes it to GitHub Pages.
5. The generated `registry.json` is consumed by Arcane clients. No manual registry edits, no stale entries, no sync drift between folders and the index.

## Templates

| Template | Description |
|----------|-------------|
| [Ollama](templates/ollama/) | Run large language models locally with persistent storage and optional GPU acceleration. |
| [LiteLLM](templates/litellm/) | Unified AI API proxy providing an OpenAI-compatible endpoint for 100+ LLM providers. |
| [n8n](templates/n8n/) | Fair-code workflow automation with 400+ integrations and AI agent capabilities. |
| [Dify](templates/dify/) | Open-source platform for building AI apps with visual workflows, RAG pipelines, and custom chatbots. |
| [LangChain](templates/langchain/) | LangServe API server deploying LangChain chains and runnables as REST APIs. |
| [OpenClaw](templates/openclaw/) | Foundation template for a community and event platform API server (Node.js + PostgreSQL). |

## License

MIT
