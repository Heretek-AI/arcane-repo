# OpenBB

> **Status: CLI Tool — Sandbox Only**
> OpenBB is primarily a CLI tool and Python library for investment research. No Docker image exists for it. This template provides a documentation/sandbox container. Install natively via `pip install openbb` for real use.

[OpenBB](https://github.com/OpenBB-finance/OpenBB) — Open-source investment research platform with AI-powered trading strategies

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
