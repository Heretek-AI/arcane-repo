---
title: "Voicebox"
description: "AI voice synthesis and speech generation platform — create natural, expressive speech from text with voice cloning, emotion control, and multi-language support"
---

# Voicebox

AI voice synthesis and speech generation platform — create natural, expressive speech from text with voice cloning, emotion control, and multi-language support

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/voicebox/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/voicebox/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/voicebox/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `voicebox` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `7ad52e26023ae3f01fdaeaa0662b3d5d87c0062a12e54812d96ba1d9d55d8f53` |

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

| Variable         | Default     | Description                                    |
|------------------|-------------|------------------------------------------------|
| `VOICEBOX_PORT`  | `8000`      | Host port for the informational API            |

## Troubleshooting

| Symptom                              | Likely Cause                     | Fix                                                    |
|--------------------------------------|----------------------------------|--------------------------------------------------------|
| No speech synthesis available         | This is an informational stub    | Install voicebox-ai on GPU hardware for full features  |
| Container exits immediately           | pip install failure              | Run `docker compose logs voicebox` for details         |
| GPU not detected in Docker            | GPU passthrough not configured   | Add `deploy: resources: reservations: devices: ...`    |
| Models fail to download               | Insufficient disk space          | Ensure 10GB+ free space for models and dependencies    |

## API Endpoints

| Endpoint   | Method | Description                         |
|------------|--------|-------------------------------------|
| `/health`  | GET    | Health check                        |
| `/guide`   | GET    | Usage guidance and setup notes      |

