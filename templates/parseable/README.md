# Parseable — Cloud-Native Log Observability

[Parseable](https://www.parseable.io/) is a high-performance, cloud-native log observability engine. It ingests, stores, and indexes logs using an S3-compatible object store backend, giving you petabyte-scale log management without managing Elasticsearch clusters.

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

## Architecture

- **parseable**: Single-binary log engine — ingests logs, indexes them in real time, stores data on S3-compatible or local storage, and serves the query API and dashboard.

## Features

- **S3-backed storage**: Store logs in MinIO, AWS S3, or any S3-compatible backend
- **OpenTelemetry native**: Ingest OTLP logs directly without translation layers
- **SQL-like queries**: Search and filter logs with a familiar query syntax
- **Schema-on-read**: No rigid index templates — logs are structured at query time
- **Multi-tenancy**: Isolate log streams per team, service, or environment

## Health Check

```bash
curl http://localhost:8000/api/v1/liveness
```

Full documentation: [parseable.io/docs](https://www.parseable.io/docs/introduction)
