# Midscene — AI-Powered UI Automation

> **CLI / npm tool — not a standalone Docker service.**
> Midscene is an npm package that runs UI automation tests using natural language.
> This Docker template provides a minimal API wrapper for integration testing and orchestration.
> For full functionality, use `npx @midscene/web` directly in your project.

[Midscene](https://midscene.js.org/) lets you describe UI interactions in plain English and executes them via Playwright/Puppeteer. It uses AI (LLMs + multimodal models) to visually understand web pages and perform actions like clicking, typing, and asserting.

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

## CLI Usage (Primary)

Midscene is best used as a dev dependency. Install it in your project:

```bash
npm install --save-dev @midscene/web
```

Create a test script (`test.yaml`):

```yaml
- task: Search for "Midscene"
  steps:
    - Open "https://google.com"
    - Type into the search bar: "Midscene AI"
    - Press Enter
    - Assert that results contain "midscene"
```

Run it:

```bash
npx @midscene/web run test.yaml
```

### Integration with Playwright/Jest

```typescript
import { Midscene } from '@midscene/web';
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();
const midscene = new Midscene(page);

await midscene.execute('Click the login button and enter credentials');
```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable            | Default     | Description                                       |
|---------------------|-------------|---------------------------------------------------|
| `MIDSCENE_PORT`     | `8000`      | Host port for the API wrapper                     |
| `OPENAI_API_KEY`    | —           | OpenAI API key for AI-driven UI analysis          |
| `MIDSCENE_TIMEOUT`  | `30000`     | Playwright/puppeteer execution timeout in ms      |

## API Endpoints

| Endpoint   | Method | Description                     |
|------------|--------|---------------------------------|
| `/health`  | GET    | Health check                    |
| `/guide`   | GET    | Usage guidance and CLI examples |

## Managing Midscene

**View logs:**

```bash
docker compose logs -f midscene
```

**Stop the server:**

```bash
docker compose down
```

## Troubleshooting

| Symptom                                 | Likely Cause                    | Fix                                                     |
|-----------------------------------------|---------------------------------|---------------------------------------------------------|
| `/health` returns but no AI features    | This is a CLI wrapper           | Use `npx @midscene/web` directly for full functionality |
| `OPENAI_API_KEY` errors on /guide       | API key not configured          | Set `OPENAI_API_KEY` in `.env`                          |
| Container exits immediately              | pip install failure             | Run `docker compose logs midscene` for details          |
