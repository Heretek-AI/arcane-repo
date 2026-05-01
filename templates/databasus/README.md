# Databasus

[Databasus](https://hub.docker.com/r/databasus/databasus) — Web-based PostgreSQL database browser. Query, visualize, and manage Postgres databases through a clean, intuitive web interface.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the web UI:**

   Open [http://localhost:5433](http://localhost:5433).

   Connect to your PostgreSQL database by providing host, port, database name, username, and password in the UI.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `DATABASUS_PORT` | `5433` | Host port for the web UI |

## Service Details

- **Web UI** — Browser-based PostgreSQL client on port 5433
- **Connection Manager** — Save and manage multiple database connections
- **Query Editor** — SQL editor with syntax highlighting and results grid
- **Data Browser** — Browse tables, views, and schemas
- **Export** — Export query results to CSV

## Upstream

- [Docker Hub](https://hub.docker.com/r/databasus/databasus)
