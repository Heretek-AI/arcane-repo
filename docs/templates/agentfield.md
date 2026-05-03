---
title: "AgentField"
description: "Multi-agent environment for training and evaluating AI agents"
---

# AgentField

Multi-agent environment for training and evaluating AI agents

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/research" class="tag-badge">research</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agentfield/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agentfield/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agentfield/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `agentfield` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `09f627e602d2798ec59b8c6527de51ed3f25ee93a0ef2e75e44fdb58521e9594` |

## Quick Start

1. **Start the informational API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8080/health
   ```

## Configuration

| Variable           | Default  | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `AGENTFIELD_PORT`  | `8080`   | Host port for the informational API stub              |

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                               |
|---------------------------------------------|---------------------------|-------------------------------------------------------------------|
| No simulation features available            | This is a Docker stub     | Use `pip install agentfield` in your own Python project           |
| Container exits immediately                 | pip install failure       | Run `docker compose logs agentfield` for details                  |
| Want multi-agent training and evaluation    | Using wrong deployment    | AgentField is a library — build your own research pipeline        |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the framework                        |
| `/guide`   | GET    | Usage instructions and quickstart examples                     |

