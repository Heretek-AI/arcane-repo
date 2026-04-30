# Plexe

[Plexe](https://github.com/plexe-ai/plexe) — AI agent orchestration with observability and debugging

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the service:**

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

> **Status: 🔍 Needs Investigation**
> This template references a Docker image (`image:` in docker-compose.yml) that doesn't exist on any public registry.
> The upstream project may have moved, renamed, or not publish Docker images. Use with caution — `docker compose up`
> will fail at image pull until the reference is corrected.

