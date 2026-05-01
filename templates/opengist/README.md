# OpenGist

[OpenGist](https://github.com/thomiceli/opengist) — Self-hosted pastebin and Git-backed snippet host. Create, share, and manage code snippets with full version control via embedded Git repositories.

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

   Open [http://localhost:6157](http://localhost:6157).

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `OPENGIST_PORT` | `6157` | Host port for the web UI |

## Service Details

- **Web UI** — Browser-based snippet manager on port 6157
- **Git-Backed** — Every gist is a full Git repository with full revision history
- **Syntax Highlighting** — Automatic syntax highlighting for 200+ languages
- **Public & Private** — Create public snippets for sharing or private snippets for personal use
- **Forking** — Fork gists to build on others' snippets
- **Storage** — All data persisted in the `opengist_data` named volume

## Upstream

- [GitHub Repository](https://github.com/thomiceli/opengist)
- [Docker Hub](https://hub.docker.com/r/thomiceli/opengist)
