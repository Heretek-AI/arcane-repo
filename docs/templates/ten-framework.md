---
title: "TEN Framework"
description: "TEN-framework/ten-framework — open-source framework for building conversational voice AI agents. Uses a complex GN/C++ build; this Docker template provides a thin API wrapper with documentation"
---

# TEN Framework

TEN-framework/ten-framework — open-source framework for building conversational voice AI agents. Uses a complex GN/C++ build; this Docker template provides a thin API wrapper with documentation

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/framework" class="tag-badge">framework</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ten-framework/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ten-framework/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ten-framework/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `ten-framework` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1cc54226aca474e71b80a0de54bef1e1bdedab9493acc257e52e131463074c70` |

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

| Variable             | Default  | Description                                           |
|----------------------|----------|-------------------------------------------------------|
| `TEN_FRAMEWORK_PORT` | `8000`   | Host port for the informational API stub              |

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                                    |
|---------------------------------------------|---------------------------|------------------------------------------------------------------------|
| No voice AI agent features available        | This is a Docker stub     | Set up the devcontainer for full development                          |
| Container exits immediately                 | pip install failure       | Run `docker compose logs ten-framework` for details                   |
| Need to build custom agents                 | Using wrong deployment    | Clone the repo and use VS Code Dev Containers with the build image    |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the framework                        |
| `/guide`   | GET    | Development setup guide and port information                   |

