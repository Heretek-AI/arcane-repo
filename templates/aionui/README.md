# AionUi — AI-Native UI Framework

> **Server-driven rendering for AI interfaces.**
> [AionUi](https://github.com/iOfficeAI/AionUi) is an open-source framework that enables AI agents to build
> and render full-stack user interfaces. It provides a server-side rendering engine
> that dynamically creates React/TypeScript UIs based on AI-generated specifications.

## Quick Start

1. **Start the server:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:3000/health
   ```

3. **AionUi is ready** — connect your AI agent or frontend to start rendering
   dynamic interfaces.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable           | Default | Description                              |
|--------------------|---------|------------------------------------------|
| `AIONUI_PORT`      | `3000`  | Host port for the web interface          |
| `OPENAI_API_KEY`   | —       | OpenAI API key for LLM-powered features  |
| `ANTHROPIC_API_KEY`| —       | Anthropic API key for LLM-powered features|
| `GITHUB_CLIENT_ID` | —       | GitHub OAuth client ID (optional)        |
| `GITHUB_CLIENT_SECRET` | —   | GitHub OAuth client secret (optional)    |
| `GOOGLE_CLIENT_ID` | —       | Google OAuth client ID (optional)        |
| `GOOGLE_CLIENT_SECRET` | —   | Google OAuth client secret (optional)    |

## Managing AionUi

**View logs:**

```bash
docker compose logs -f aionui
```

**Stop the server:**

```bash
docker compose down
```

**Rebuild and restart (after configuration changes):**

```bash
docker compose build aionui
docker compose up -d
```

## Troubleshooting

| Symptom                                    | Likely Cause                    | Fix                                                |
|--------------------------------------------|---------------------------------|----------------------------------------------------|
| Container exits immediately                 | Build failure                   | Run `docker compose logs aionui` for details       |
| Port conflict                               | Another service on port 3000    | Change `AIONUI_PORT` in `.env`                     |
| Web UI not accessible                       | Firewall or port mapping        | Check `docker ps` to verify container is running   |
| Build takes too long                        | First build clones upstream     | Subsequent builds use Docker cache                |
