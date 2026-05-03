---
title: "VoltAgent"
description: "Multi-agent framework for autonomous AI workflows"
---

# VoltAgent

Multi-agent framework for autonomous AI workflows

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/workflow" class="tag-badge">workflow</a> <a href="/categories/automation" class="tag-badge">automation</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/voltagent/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/voltagent/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/voltagent/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `voltagent` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f6cd0b8d1aa843de52f7bb6ac5355dc83829c147a17abc962c347b3407ea5bbc` |

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
| `VOLTAGENT_PORT`   | `8000`   | Host port for the informational API stub              |

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                               |
|---------------------------------------------|---------------------------|-------------------------------------------------------------------|
| No workflow automation available            | This is a Docker stub     | Use `pip install voltagent` in your own Python project            |
| Container exits immediately                 | pip install failure       | Run `docker compose logs voltagent` for details                   |
| Want autonomous multi-agent workflows       | Using wrong deployment    | VoltAgent is a library — build your own orchestrator around it    |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the framework                        |
| `/guide`   | GET    | Usage instructions and quickstart examples                     |

