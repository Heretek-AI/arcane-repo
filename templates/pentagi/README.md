# PentaGI

[PentaGI](https://github.com/vxcontrol/pentagi) — AI penetration testing with autonomous security assessment

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

The docker-compose.yml exposes environment variables documented in `.env.example`. The container includes a healthcheck on port 8080 with a 60s start period.

