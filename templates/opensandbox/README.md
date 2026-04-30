# OpenSandbox — Code Execution Sandbox

> **Informational template — project identity is ambiguous.**
> This template provides a minimal API stub for isolated code execution.
> For production deployments, consider [Judge0 CE](https://github.com/judge0/judge0)
> or [Piston](https://github.com/engineer-man/piston), which are dedicated,
> production-tested code execution engines.

OpenSandbox provides secure, isolated code compilation and execution for multiple programming languages via a REST API. Sandboxed execution is essential for AI coding assistants, online judges, coding education platforms, and any service that runs untrusted user code.

## Quick Start

1. **Start the API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

## Production Alternatives

For production code execution, use a dedicated sandbox engine:

### Judge0 CE

[Judge0 CE](https://github.com/judge0/judge0) is the leading open-source code execution engine, used by 1000+ organizations:

```yaml
services:
  judge0:
    image: judge0/judge0:1.13.0
    ports:
      - "2358:2358"
    environment:
      - JUDGE0_AUTH_TOKEN=your-secret-token
    # Requires PostgreSQL, Redis, and RabbitMQ — see docs
```

### Piston

[Piston](https://github.com/engineer-man/piston) is a lightweight code execution engine:

```yaml
services:
  piston:
    image: ghcr.io/engineer-man/piston
    ports:
      - "2000:2000"
    volumes:
      - piston_data:/piston/packages
```

## Configuration

| Variable              | Default  | Description                            |
|-----------------------|----------|----------------------------------------|
| `OPENSANDBOX_PORT`    | `8000`   | Host port for the informational API    |

## API Endpoints

| Endpoint   | Method | Description                                          |
|------------|--------|------------------------------------------------------|
| `/health`  | GET    | Health check + alternative deployment recommendations |

## Managing OpenSandbox

**View logs:**

```bash
docker compose logs -f opensandbox
```

**Stop the server:**

```bash
docker compose down
```

## Troubleshooting

| Symptom                                      | Likely Cause               | Fix                                                    |
|----------------------------------------------|----------------------------|--------------------------------------------------------|
| No code execution available                   | This is an informational stub | Deploy Judge0 CE or Piston for full capabilities       |
| Container exits immediately                    | pip install failure         | Run `docker compose logs opensandbox` for details      |
| Need multi-language support                   | Not supported in this stub  | Judge0 CE supports 60+ languages out of the box        |
