# txtai

[txtai](https://github.com/neuml/txtai) — AI-powered semantic search and RAG platform

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

> **Status: Library — Uses python:3.12-slim base image**
> This project is a Python library and does not publish a Docker image.
> The template installs it via `pip install` at container startup.

