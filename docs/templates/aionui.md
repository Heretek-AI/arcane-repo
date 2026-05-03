---
title: "AionUi"
description: "AI-native UI framework — build full-stack AI interfaces with a server-driven rendering approach for React and TypeScript applications"
---

# AionUi

AI-native UI framework — build full-stack AI interfaces with a server-driven rendering approach for React and TypeScript applications

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/framework" class="tag-badge">framework</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/aionui/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/aionui/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/aionui/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `aionui` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b4e2e9b1a382f7f0eb0daf16571dbfce03a0c33c0f9c8037ac2836c462777e40` |

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

## Troubleshooting

| Symptom                                    | Likely Cause                    | Fix                                                |
|--------------------------------------------|---------------------------------|----------------------------------------------------|
| Container exits immediately                 | Build failure                   | Run `docker compose logs aionui` for details       |
| Port conflict                               | Another service on port 3000    | Change `AIONUI_PORT` in `.env`                     |
| Web UI not accessible                       | Firewall or port mapping        | Check `docker ps` to verify container is running   |
| Build takes too long                        | First build clones upstream     | Subsequent builds use Docker cache                |

