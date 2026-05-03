---
title: "Meetily"
description: "AI-powered meeting assistant — native desktop Electron app for real-time transcription, summarization, and action item extraction from meetings"
---

# Meetily

AI-powered meeting assistant — native desktop Electron app for real-time transcription, summarization, and action item extraction from meetings

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/meetily/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/meetily/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/meetily/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `meetily` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b2f09b5f157ac35290e738919d26897a19972c9665ca92e299743d313193d95e` |

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

| Variable          | Default  | Description                              |
|------------------ |----------|------------------------------------------|
| `MEETILY_PORT`    | `8000`   | Host port for the informational API stub |

## Troubleshooting

| Symptom                                          | Likely Cause               | Fix                                                  |
|--------------------------------------------------|----------------------------|------------------------------------------------------|
| No transcription features available              | This is a Docker stub      | Download the desktop app from https://meetily.app    |
| Container exits immediately                       | pip install failure        | Run `docker compose logs meetily` for details        |
| Need to transcribe meetings                      | Using wrong deployment     | Meetily runs natively on macOS, Windows, and Linux   |

## API Endpoints

| Endpoint   | Method | Description                                          |
|------------|--------|------------------------------------------------------|
| `/health`  | GET    | Health check + download link for the desktop app     |

