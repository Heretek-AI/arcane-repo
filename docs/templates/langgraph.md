---
title: "LangGraph"
description: "Framework for stateful multi-actor agent applications"
---

# LangGraph

Framework for stateful multi-actor agent applications

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/framework" class="tag-badge">framework</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/langgraph/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/langgraph/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/langgraph/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `langgraph` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `9d07a757b846d7d86de8c2a7e8a6cbe333383bc45ff7822a5e273084e45e9e8a` |

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

| Variable           | Default  | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `LANGGRAPH_PORT`   | `8000`   | Host port for the informational API stub              |

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                               |
|---------------------------------------------|---------------------------|-------------------------------------------------------------------|
| No agent functionality available            | This is a Docker stub     | Use `pip install langgraph` in your own Python project            |
| Container exits immediately                 | pip install failure       | Run `docker compose logs langgraph` for details                   |
| Want to run multi-actor agents              | Using wrong deployment    | LangGraph is a library — build your own FastAPI app around it     |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the framework                        |
| `/guide`   | GET    | Usage instructions and quickstart examples                     |

