---
title: "Harness"
description: "Open-source CI/CD and DevOps platform — automate builds, tests, deployments, and infrastructure provisioning from a single dashboard"
---

# Harness

Open-source CI/CD and DevOps platform — automate builds, tests, deployments, and infrastructure provisioning from a single dashboard

## Tags

<a href="/categories/devops" class="tag-badge">devops</a> <a href="/categories/automation" class="tag-badge">automation</a> <a href="/categories/paas" class="tag-badge">paas</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/harness/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/harness/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/harness/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `harness` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ba338f9d4ab52bde45e0f013faacd7626fbed76680a3b1d452e99204dee31f31` |

## Architecture

- **harness**: Single Docker container running the complete Harness platform — manager, delegate, pipeline engine, and web UI. Self-contained; no external DB required for standalone mode. Optional Docker socket mount enables pipeline execution on the host.

## Quick Start

1. **Start the service:**

   ```bash
   docker compose up -d
   ```

2. **Access the dashboard** at [http://localhost:3000](http://localhost:3000)

3. **Log in** with the admin password from your `.env` file (default: `changeme`).

4. **Enable Docker-in-Docker** by uncommenting the `/var/run/docker.sock` mount in `docker-compose.yml` — required for pipeline execution.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                | Default      | Description                                   |
|-------------------------|--------------|-----------------------------------------------|
| `HARNESS_WEB_PORT`      | `3000`       | Host port for the web dashboard               |
| `HARNESS_SSH_PORT`      | `3022`       | Host port for SSH-based deployments           |
| `HARNESS_MODE`          | `standalone` | Deployment mode (standalone or cluster)       |
| `HARNESS_ADMIN_PASSWORD`| `changeme`   | Admin password — **change for production**    |

## Health Check

```bash
curl http://localhost:3000/api/health
```

Full documentation: [developer.harness.io](https://developer.harness.io/docs/self-managed-enterprise-edition)

