# TEN Framework — Conversational Voice AI Platform

> **Development platform — not a standalone Docker service.**
> [TEN Framework](https://github.com/TEN-framework/ten-framework) is an
> open-source framework for building conversational voice AI agents. Due to
> its complex C++ build system (GN toolchain with submodules), it is designed
> for development workspace use. This Docker template provides a minimal
> informational API stub.

## Quick Start

1. **Start the informational API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

## Development Setup (Recommended)

The recommended way to work with TEN Framework is using their devcontainer:

1. **Open in VS Code Dev Container:**

   ```bash
   git clone https://github.com/TEN-framework/ten-framework.git
   cd ten-framework
   code .
   ```

2. **When prompted, "Reopen in Container"** (uses `ghcr.io/ten-framework/ten_agent_build:0.7.14`)

3. **Navigate to the AI Agents workspace:**

   ```bash
   cd /workspaces/ten-framework/ai_agents
   ```

4. **Start an agent:**

   ```bash
   # Using the TMAN tool
   npx tman --config=your_agent_config.json

   # Or using npm scripts
   npm start
   ```

### Ports

| Port   | Service           |
|--------|-------------------|
| 3000   | Agent Example UI  |
| 8080   | TEN API Server    |
| 49483  | TMAN Designer     |
| 49484  | TEN Service Hub   |

## Configuration

| Variable             | Default  | Description                                           |
|----------------------|----------|-------------------------------------------------------|
| `TEN_FRAMEWORK_PORT` | `8000`   | Host port for the informational API stub              |

## API Endpoints

| Endpoint   | Method | Description                                                    |
|------------|--------|----------------------------------------------------------------|
| `/health`  | GET    | Health check + info about the framework                        |
| `/guide`   | GET    | Development setup guide and port information                   |

## Managing

**View logs:**

```bash
docker compose logs -f ten-framework
```

## Troubleshooting

| Symptom                                     | Likely Cause              | Fix                                                                    |
|---------------------------------------------|---------------------------|------------------------------------------------------------------------|
| No voice AI agent features available        | This is a Docker stub     | Set up the devcontainer for full development                          |
| Container exits immediately                 | pip install failure       | Run `docker compose logs ten-framework` for details                   |
| Need to build custom agents                 | Using wrong deployment    | Clone the repo and use VS Code Dev Containers with the build image    |
