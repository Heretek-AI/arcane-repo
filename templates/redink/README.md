# RedInk — AI Content Generator

[RedInk](https://github.com/HisMax/RedInk) is an AI-powered content generator designed for creating Xiaohongshu-style (RED) social media posts. It combines LLM text generation with AI image creation to produce complete, platform-optimized content.

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

## Tech Stack

- **Backend**: Python / Flask
- **Frontend**: Vue.js
- **AI**: OpenAI (or compatible) API for text, DALL-E for images
- **Database**: SQLite (default) or PostgreSQL

## API Providers

RedInk supports multiple LLM backends:

- **OpenAI**: Set `REDINK_API_PROVIDER=openai` and provide an OpenAI API key
- **Azure**: Set `REDINK_API_PROVIDER=azure`, `REDINK_API_BASE_URL` to your Azure endpoint, and use your Azure API key
- **Anthropic**: Set `REDINK_API_PROVIDER=anthropic` and provide your Anthropic API key
- **Custom** (OpenAI-compatible): Set `REDINK_API_BASE_URL` to any OpenAI-compatible endpoint (localai, ollama proxy, etc.)

## Health Check

```bash
curl http://localhost:12398/api/health
```

Full documentation: [github.com/HisMax/RedInk](https://github.com/HisMax/RedInk)
