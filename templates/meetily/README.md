# Meetily — AI-Powered Meeting Assistant

> **Desktop Electron application — not a standalone Docker service.**
> Meetily is a native desktop app for real-time meeting transcription, summarization,
> and action item extraction. This Docker template provides a minimal informational
> API stub. Install the desktop app for full functionality.

[Meetily](https://meetily.app) is an AI meeting assistant that runs on your desktop. It provides real-time transcription, smart summarization, action item extraction, and integration with platforms like Zoom, Google Meet, and Microsoft Teams.

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

## Desktop App Installation (Recommended)

Download and install the Meetily desktop app from the official website:

**[https://meetily.app](https://meetily.app)**

### Features

- **Real-time transcription** — automatic speech-to-text during meetings
- **AI summaries** — get concise meeting summaries with key points
- **Action items** — automatically extract tasks and assignments
- **Platform support** — works with Zoom, Google Meet, Microsoft Teams
- **Search** — search across all your meeting transcripts
- **Export** — export transcripts and summaries to markdown, PDF, or Notion

## Configuration

| Variable          | Default  | Description                              |
|------------------ |----------|------------------------------------------|
| `MEETILY_PORT`    | `8000`   | Host port for the informational API stub |

## API Endpoints

| Endpoint   | Method | Description                                          |
|------------|--------|------------------------------------------------------|
| `/health`  | GET    | Health check + download link for the desktop app     |

## Managing Meetily

**View logs:**

```bash
docker compose logs -f meetily
```

**Stop the server:**

```bash
docker compose down
```

## Troubleshooting

| Symptom                                          | Likely Cause               | Fix                                                  |
|--------------------------------------------------|----------------------------|------------------------------------------------------|
| No transcription features available              | This is a Docker stub      | Download the desktop app from https://meetily.app    |
| Container exits immediately                       | pip install failure        | Run `docker compose logs meetily` for details        |
| Need to transcribe meetings                      | Using wrong deployment     | Meetily runs natively on macOS, Windows, and Linux   |
