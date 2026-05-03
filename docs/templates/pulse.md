---
title: "Pulse"
description: "Real-time infrastructure monitoring with AI-powered insights — track server health, detect anomalies, and get intelligent alerts"
---

# Pulse

Real-time infrastructure monitoring with AI-powered insights — track server health, detect anomalies, and get intelligent alerts

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/observability" class="tag-badge">observability</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pulse/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pulse/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pulse/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pulse` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e13dc511ce4598262ecc2c181590384e942506f76347dc8dc5d2b2c53edaa3e2` |

## Architecture

- **pulse-app**: The main application — web dashboard, API, metric processing, AI anomaly detection
- **pulse-db**: PostgreSQL database — stores metrics, configuration, and user data
- **pulse-redis**: Redis cache — handles real-time metric ingestion, job queues, and session caching

## Quick Start

1. **Start the services:**

   ```bash
   docker compose up -d
   ```

2. **Access the dashboard** at [http://localhost:8080](http://localhost:8080)

3. **Add your servers** from the dashboard to begin monitoring.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable              | Default    | Description                                   |
|-----------------------|------------|-----------------------------------------------|
| `PULSE_PORT`          | `8080`     | Host port for the web dashboard               |
| `PULSE_DB_NAME`       | `pulse`    | PostgreSQL database name                      |
| `PULSE_DB_USER`       | `pulse`    | PostgreSQL user                               |
| `PULSE_DB_PASSWORD`   | `changeme` | PostgreSQL password — **change for production**|
| `PULSE_SECRET_KEY`    | (empty)    | Session encryption secret — **required**      |
| `PULSE_LOG_LEVEL`     | `info`     | Log verbosity (debug, info, warn, error)      |

## Health Check

```bash
curl http://localhost:8080/api/health
```

Full documentation: [github.com/rcourtman/Pulse](https://github.com/rcourtman/Pulse)

