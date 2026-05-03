---
title: "Parseable"
description: "Cloud-native log observability engine — store, search, and analyze logs at scale with an S3-compatible backend"
---

# Parseable

Cloud-native log observability engine — store, search, and analyze logs at scale with an S3-compatible backend

## Tags

<a href="/categories/observability" class="tag-badge">observability</a> <a href="/categories/analytics" class="tag-badge">analytics</a> <a href="/categories/monitoring" class="tag-badge">monitoring</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/parseable/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/parseable/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/parseable/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `parseable` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c9b5acf26e56c2e5c8603c21c76f6b5c0159d2b0d1c638b11f34bd9df37c608c` |

## Architecture

- **parseable**: Single-binary log engine — ingests logs, indexes them in real time, stores data on S3-compatible or local storage, and serves the query API and dashboard.

## Quick Start

1. **Start the service:**

   ```bash
   docker compose up -d
   ```

2. **Access the dashboard** at [http://localhost:8000](http://localhost:8000)

3. **Log in** with the credentials from your `.env` file (default: `admin` / `changeme`).

4. **Send logs** using the built-in ingestion API, Fluent Bit, Vector, or any OpenTelemetry-compatible agent.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable              | Default    | Description                                   |
|-----------------------|------------|-----------------------------------------------|
| `PARSEABLE_PORT`      | `8000`     | Host port for the web UI and API              |
| `PARSEABLE_USERNAME`  | `admin`    | Admin username for the dashboard              |
| `PARSEABLE_PASSWORD`  | `changeme` | Admin password — **change for production**    |

## Health Check

```bash
curl http://localhost:8000/api/v1/liveness
```

Full documentation: [parseable.io/docs](https://www.parseable.io/docs/introduction)

