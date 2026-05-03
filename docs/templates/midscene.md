---
title: "Midscene"
description: "AI-powered UI automation and testing tool — visually understand and interact with web UI using natural language, run via npx or integrate into Playwright/Jest test suites"
---

# Midscene

AI-powered UI automation and testing tool — visually understand and interact with web UI using natural language, run via npx or integrate into Playwright/Jest test suites

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/automation" class="tag-badge">automation</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/midscene/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/midscene/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/midscene/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `midscene` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e1ef2f6a70fcba39d3d6158fa51cac538bde1ff65f32c8835e8961b06a3a8f1f` |

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

3. **Get usage guidance:**

   ```bash
   curl http://localhost:8000/guide
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable            | Default     | Description                                       |
|---------------------|-------------|---------------------------------------------------|
| `MIDSCENE_PORT`     | `8000`      | Host port for the API wrapper                     |
| `OPENAI_API_KEY`    | —           | OpenAI API key for AI-driven UI analysis          |
| `MIDSCENE_TIMEOUT`  | `30000`     | Playwright/puppeteer execution timeout in ms      |

## Troubleshooting

| Symptom                                 | Likely Cause                    | Fix                                                     |
|-----------------------------------------|---------------------------------|---------------------------------------------------------|
| `/health` returns but no AI features    | This is a CLI wrapper           | Use `npx @midscene/web` directly for full functionality |
| `OPENAI_API_KEY` errors on /guide       | API key not configured          | Set `OPENAI_API_KEY` in `.env`                          |
| Container exits immediately              | pip install failure             | Run `docker compose logs midscene` for details          |

## API Endpoints

| Endpoint   | Method | Description                     |
|------------|--------|---------------------------------|
| `/health`  | GET    | Health check                    |
| `/guide`   | GET    | Usage guidance and CLI examples |

