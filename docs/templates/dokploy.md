---
title: "Dokploy"
description: "Open-source Platform as a Service — deploy and manage applications, databases, and services on your own infrastructure with a clean dashboard"
---

# Dokploy

Open-source Platform as a Service — deploy and manage applications, databases, and services on your own infrastructure with a clean dashboard

## Tags

<a href="/categories/paas" class="tag-badge">paas</a> <a href="/categories/devops" class="tag-badge">devops</a> <a href="/categories/platform" class="tag-badge">platform</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dokploy/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dokploy/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dokploy/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dokploy` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `160e7d6faeedecb5659211e21930a7b3cb06e9243471d6e754a950e79efd591e` |

## Architecture

- **dokploy**: Single Node.js container running the complete Dokploy platform — API server, web dashboard, background task runner, and database (internal SQLite, no external DB needed). Self-contained. Optional Docker socket mount enables full container lifecycle management.

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

## Health Check

```bash
curl http://localhost:3000/api/health
```

Full documentation: [dokploy.com/docs](https://dokploy.com/docs)

