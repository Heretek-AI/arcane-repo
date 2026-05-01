# Dokploy — Open-Source Platform as a Service

[Dokploy](https://dokploy.com/) is an open-source PaaS that lets you deploy and manage applications, databases, and services on your own infrastructure. Think Vercel or Railway, but running on your own servers.

## Quick Start

1. **Start the service:**

   ```bash
   docker compose up -d
   ```

2. **Access the dashboard** at [http://localhost:3000](http://localhost:3000)

3. **Create your admin account** on first launch.

4. **Enable Docker management** by uncommenting the `/var/run/docker.sock` mount in `docker-compose.yml` — required to manage containers from the dashboard.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable              | Default      | Description                                   |
|-----------------------|--------------|-----------------------------------------------|
| `DOKPLOY_PORT`        | `3000`       | Host port for the web dashboard               |
| `DOKPLOY_NODE_ENV`    | `production` | Node.js environment mode                     |
| `DOKPLOY_SECRET_KEY`  | (empty)      | Session encryption secret — **required**      |

## Architecture

- **dokploy**: Single Node.js container running the complete Dokploy platform — API server, web dashboard, background task runner, and database (internal SQLite, no external DB needed). Self-contained. Optional Docker socket mount enables full container lifecycle management.

## Features

- **Application deployment**: Deploy from Git, Docker images, or Docker Compose files
- **Database provisioning**: One-click PostgreSQL, MySQL, MongoDB, and Redis instances
- **Automatic SSL**: Built-in Let's Encrypt integration for HTTPS
- **Rolling updates**: Zero-downtime deploys with automatic rollback on failure
- **Resource monitoring**: CPU, memory, and network metrics per application
- **Team management**: Role-based access with project-level permissions

## Docker Socket

The Docker socket mount (`/var/run/docker.sock`) is required for:
- Creating and managing containers through the dashboard
- Reading container logs and metrics
- Starting, stopping, and restarting applications

It is **commented by default** — uncomment in `docker-compose.yml` when you want full PaaS functionality.

## Health Check

```bash
curl http://localhost:3000/api/health
```

Full documentation: [dokploy.com/docs](https://dokploy.com/docs)
