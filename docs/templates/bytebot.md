---
title: "Bytebot"
description: "Browser automation agent with natural language — controls web browsers via AI. Primarily a Python library/CLI; this Docker template provides a thin API wrapper for health checks and documentation"
---

# Bytebot

Browser automation agent with natural language — controls web browsers via AI. Primarily a Python library/CLI; this Docker template provides a thin API wrapper for health checks and documentation

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/web" class="tag-badge">web</a> <a href="/categories/python" class="tag-badge">python</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bytebot/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bytebot/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bytebot/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `bytebot` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `479292eb84d38b0bb45bf985fb3b3b73adec63538b03031ab119b3151b5bd8af` |

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

| Variable         | Default  | Description                       |
|------------------|----------|-----------------------------------|
| `BYTEBOT_PORT`   | `8000`   | Host port for the informational API stub |

## Troubleshooting

| Symptom                                  | Likely Cause              | Fix                                                            |
|------------------------------------------|---------------------------|----------------------------------------------------------------|
| No browser automation features available | This is a Docker stub     | Install `bytebot` via pip on your host machine                 |
| Container exits immediately              | pip install failure       | Run `docker compose logs bytebot` for details                  |
| Need headless browser interaction        | Using wrong deployment    | Bytebot runs natively — install Python and use pip             |

## API Endpoints

| Endpoint  | Method | Description                                          |
|-----------|--------|------------------------------------------------------|
| `/health` | GET    | Health check + tool info                             |
| `/guide`  | GET    | Python library usage examples and pip instructions   |

