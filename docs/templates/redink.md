---
title: "RedInk"
description: "AI-powered image and text content generator for social media — Xiaohongshu-style content creation with LLM + image generation"
---

# RedInk

AI-powered image and text content generator for social media — Xiaohongshu-style content creation with LLM + image generation

## Tags

<a href="/categories/ai" class="tag-badge">ai</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/redink/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/redink/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/redink/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `redink` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `541a74a1761c836680a2420cd927256024ce9401b43610adaa822a6785d7ade8` |

## Quick Start

1. **Configure your API keys** in `.env`:

   ```bash
   cp .env.example .env
   # Edit .env and set REDINK_API_KEY and REDINK_IMAGE_API_KEY
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the application** at [http://localhost:12398](http://localhost:12398)

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                | Default                    | Description                               |
|-------------------------|----------------------------|-------------------------------------------|
| `REDINK_PORT`           | `12398`                    | Host port for the web application         |
| `REDINK_SECRET_KEY`     | (empty)                    | Session encryption — **required for prod**|
| `REDINK_DB_URL`         | `sqlite:///app/data/redink.db` | Database URL (SQLite or PostgreSQL)   |
| `REDINK_API_PROVIDER`   | `openai`                   | LLM provider (openai, azure, anthropic)   |
| `REDINK_API_KEY`        | (empty)                    | API key for your LLM provider             |
| `REDINK_API_BASE_URL`   | (empty)                    | Custom API endpoint (Azure, proxies)      |
| `REDINK_MODEL_NAME`     | `gpt-4`                    | LLM model for text generation             |
| `REDINK_IMAGE_API_KEY`  | (empty)                    | API key for image generation service      |
| `REDINK_LOG_LEVEL`      | `info`                     | Log verbosity (debug, info, warn, error)  |
| `TZ`                    | `UTC`                      | Timezone                                  |

## Health Check

```bash
curl http://localhost:12398/api/health
```

Full documentation: [github.com/HisMax/RedInk](https://github.com/HisMax/RedInk)

