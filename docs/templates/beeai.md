---
title: "BeeAI Framework"
description: "IBM framework for production-ready AI agents"
---

# BeeAI Framework

IBM framework for production-ready AI agents

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/framework" class="tag-badge">framework</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/beeai/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/beeai/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/beeai/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `beeai` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a2199d5e933fc5e10c6c4b8f024318ac4e36d76bd60871b9489a393a760f1a27` |

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

## Configuration

| Variable      | Default  | Description                                           |
|---------------|----------|-------------------------------------------------------|
| `BEEAI_PORT`  | `8000`   | Host port for the informational API stub              |

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                               |
|---------------------------------------------|---------------------------|-------------------------------------------------------------------|
| No agent functionality available            | This is a Docker stub     | Use `pip install beeai-framework` in your own project             |
| Container exits immediately                 | pip install failure       | Run `docker compose logs beeai` for details                       |
| Want production-grade agent workflows       | Using wrong deployment    | BeeAI is a library — integrate it into your own FastAPI app       |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the framework                        |
| `/guide`   | GET    | Usage instructions and quickstart examples                     |

