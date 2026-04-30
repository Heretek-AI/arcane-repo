# Supabase

[Supabase](https://github.com/supabase/supabase) — Open-source Firebase alternative with PostgreSQL, auth, and real-time

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

> **Status: Multi-Container Platform**
> Supabase is a complex platform requiring multiple services (PostgreSQL, GoTrue, Realtime, Storage).
> It doesn't ship as a single Docker image. The template's `image:` reference is a placeholder —
> a full Supabase deployment requires their CLI or self-hosted docker-compose.

