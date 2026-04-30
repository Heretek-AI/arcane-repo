# SillyTavern

[SillyTavern](https://github.com/SillyTavern/SillyTavern) — LLM chat frontend for interacting with various AI backends, featuring text generation, roleplay, and character management

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

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

> **Status: 🏗️ CI Build Pending**
> The upstream project includes a Dockerfile, but no pre-built image is published. The template currently
> references a non-existent image. A CI pipeline will build and publish to GHCR (planned for future update).
