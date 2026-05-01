# Streamer Sales — AI Live Stream Sales Assistant

[Streamer Sales](https://github.com/PeterH0323/Streamer-Sales) (3.6k+ ★) is an AI-powered live streaming sales assistant that automates product demonstrations, answers customer questions, and drives e-commerce conversions during live streams.

## Quick Start

1. **Start the sales bot:**

   ```bash
   docker compose up -d
   ```

2. **Check health:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **View bot info:**

   ```bash
   curl http://localhost:8000/info
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                | Default | Description                      |
|-------------------------|---------|----------------------------------|
| `STREAMER_SALES_PORT`   | `8000`  | Host port for the sales bot API  |

## Simplified Architecture

Upstream's `compose.yaml` defines **7+ services** for a full production deployment. This template simplifies to the **core sales bot service only**. Omitted services:

| Omitted              | Purpose                                            | How to Replace                         |
|----------------------|----------------------------------------------------|----------------------------------------|
| MySQL / Redis        | Data persistence and caching                       | Contact end-user for upstream compose  |
| Web frontend         | Admin dashboard and configuration UI               | API-first operation via REST           |
| TTS / ASR services   | Text-to-speech and speech recognition              | Text-only mode by default              |
| RabbitMQ / Celery    | Task queue and background workers                  | Synchronous mode for core functionality|
| Additional microservices | Analytics, monitoring, etc.                     | Minimal viable deployment              |

The full 7+ service deployment is available in [upstream's compose.yaml](https://github.com/PeterH0323/Streamer-Sales/blob/master/compose.yaml). Use that for production-scale streaming with all features enabled.

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/Streamer-Sales/Dockerfile`) built with the uv-python pattern. The FastAPI wrapper provides health and info documenting the simplification from 7+ services to core bot. Image is built and pushed to GHCR via CI (`.github/workflows/build-Streamer-Sales.yml`).

## API Endpoints

| Endpoint  | Method | Description              |
|-----------|--------|--------------------------|
| `/health` | GET    | Health check             |
| `/info`   | GET    | Bot and simplification info |

## Upstream

- **Repository:** [PeterH0323/Streamer-Sales](https://github.com/PeterH0323/Streamer-Sales)
- **Stars:** 3.6k+
- **Backend:** Python
- **Upstream services:** 7+
