# Page Agent — In-Browser GUI Agent

> **CLI tool / browser extension — not a standalone Docker service.**
> [Page Agent](https://github.com/alibaba/page-agent) by Alibaba is a JavaScript
> in-browser GUI agent that controls web interfaces with natural language.
> This Docker template provides a minimal informational API stub.
> Use the npm CLI for full functionality.

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

## Full CLI Usage (Recommended)

Page Agent is primarily used as a Node.js CLI tool or browser extension:

```bash
# Using npx (no installation required)
npx @page-agent/page-agent <target-url> \
  --instruction "describe the action to perform"
```

### Examples

```bash
# Click a button on a page
npx @page-agent/page-agent https://example.com \
  --instruction "click the sign up button"

# Fill a form
npx @page-agent/page-agent https://example.com \
  --instruction "fill the login form with username admin and password pass123"

# Scrape structured data
npx @page-agent/page-agent https://example.com \
  --instruction "extract all product names and prices"
```

### Installation

```bash
# Global install
npm install -g @page-agent/page-agent

# Or use directly in a project
npm install @page-agent/page-agent
```

## Configuration

| Variable           | Default  | Description                                           |
|--------------------|----------|-------------------------------------------------------|
| `PAGE_AGENT_PORT`  | `8000`   | Host port for the informational API stub              |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the CLI tool                         |
| `/guide`   | GET    | CLI usage examples and npm installation instructions            |

## Managing

**View logs:**

```bash
docker compose logs -f page-agent
```

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                               |
|---------------------------------------------|---------------------------|-------------------------------------------------------------------|
| No browser automation features available    | This is a Docker stub     | Use `npx @page-agent/page-agent` directly on your host machine    |
| Container exits immediately                 | pip install failure       | Run `docker compose logs page-agent` for details                  |
| Need headless browser interaction           | Using wrong deployment    | Page Agent runs natively — install Node.js and use npm            |
