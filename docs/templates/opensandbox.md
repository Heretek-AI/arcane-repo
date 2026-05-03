---
title: "OpenSandbox"
description: "Code execution sandbox environment — secure, isolated code compilation and execution for multiple programming languages with REST API"
---

# OpenSandbox

Code execution sandbox environment — secure, isolated code compilation and execution for multiple programming languages with REST API

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/api" class="tag-badge">api</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/opensandbox/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/opensandbox/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/opensandbox/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `opensandbox` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `311aa8e1fa781f76aeb5b2ab4f128367277aa4b434828ec66dff92cdc91e671e` |

## Quick Start

1. **Start the API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

## Configuration

| Variable              | Default  | Description                            |
|-----------------------|----------|----------------------------------------|
| `OPENSANDBOX_PORT`    | `8000`   | Host port for the informational API    |

## Troubleshooting

| Symptom                                      | Likely Cause               | Fix                                                    |
|----------------------------------------------|----------------------------|--------------------------------------------------------|
| No code execution available                   | This is an informational stub | Deploy Judge0 CE or Piston for full capabilities       |
| Container exits immediately                    | pip install failure         | Run `docker compose logs opensandbox` for details      |
| Need multi-language support                   | Not supported in this stub  | Judge0 CE supports 60+ languages out of the box        |

## API Endpoints

| Endpoint   | Method | Description                                          |
|------------|--------|------------------------------------------------------|
| `/health`  | GET    | Health check + alternative deployment recommendations |

