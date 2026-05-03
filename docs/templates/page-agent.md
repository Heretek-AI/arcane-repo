---
title: "Page Agent"
description: "Alibaba Page Agent — JavaScript in-page GUI agent that controls web interfaces with natural language. Primarily a browser-based CLI tool; this Docker template provides a thin API wrapper for orchestration"
---

# Page Agent

Alibaba Page Agent — JavaScript in-page GUI agent that controls web interfaces with natural language. Primarily a browser-based CLI tool; this Docker template provides a thin API wrapper for orchestration

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/web" class="tag-badge">web</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/page-agent/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/page-agent/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/page-agent/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `page-agent` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6238886902128f8d22752ec42e7cd492c9cdaa472634176b97f7c8719cf9c9e5` |

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
| `PAGE_AGENT_PORT`  | `8000`   | Host port for the informational API stub              |

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                               |
|---------------------------------------------|---------------------------|-------------------------------------------------------------------|
| No browser automation features available    | This is a Docker stub     | Use `npx @page-agent/page-agent` directly on your host machine    |
| Container exits immediately                 | pip install failure       | Run `docker compose logs page-agent` for details                  |
| Need headless browser interaction           | Using wrong deployment    | Page Agent runs natively — install Node.js and use npm            |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the CLI tool                         |
| `/guide`   | GET    | CLI usage examples and npm installation instructions            |

