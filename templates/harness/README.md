# Harness — Open-Source CI/CD & DevOps Platform

[Harness](https://www.harness.io/) is a modern CI/CD platform that automates the full software delivery pipeline — from code commit through build, test, deploy, and infrastructure provisioning. This is the self-hosted community edition.

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

## Architecture

- **harness**: Single Docker container running the complete Harness platform — manager, delegate, pipeline engine, and web UI. Self-contained; no external DB required for standalone mode. Optional Docker socket mount enables pipeline execution on the host.

## Features

- **Pipeline automation**: Visual pipeline builder with CI, CD, and custom workflow stages
- **Git triggers**: Start pipelines automatically on push, PR, tag, or schedule
- **Secret management**: Encrypted secrets scoped to projects and environments
- **Approval gates**: Manual and automated approval steps within deployment pipelines
- **Infrastructure as code**: Provision cloud resources directly from pipeline steps

## Docker Socket

The Docker socket mount (`/var/run/docker.sock`) is required for:
- Building Docker images inside pipelines
- Running containers for test or build steps
- Deploying to local Docker hosts

It is **commented by default** — uncomment in `docker-compose.yml` when you need pipeline execution.

## Health Check

```bash
curl http://localhost:3000/api/health
```

Full documentation: [developer.harness.io](https://developer.harness.io/docs/self-managed-enterprise-edition)
