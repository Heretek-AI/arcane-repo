---
title: "Matrix Server"
description: "Lightweight Matrix homeserver powered by Conduit — a fast Rust implementation of the Matrix protocol for federated chat"
---

# Matrix Server

Lightweight Matrix homeserver powered by Conduit — a fast Rust implementation of the Matrix protocol for federated chat

## Tags

<a href="/categories/chat" class="tag-badge">chat</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/matrix-server/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/matrix-server/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/matrix-server/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `matrix-server` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `aa8e141e55f66747294e0e89953c2944c6e192679ee26cd6374e12f26e2dec2a` |

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Configure your server name** — edit `.env` and set `MATRIX_SERVER_NAME` to your domain (e.g., `matrix.example.com`).

3. **Start the homeserver:**

   ```bash
   docker compose up -d
   ```

4. **Verify the server is running:**

   Open [http://localhost:8448/_matrix/client/versions](http://localhost:8448/_matrix/client/versions) — you should see a JSON response with supported Matrix API versions.

5. **Connect with a Matrix client** (e.g., Element, FluffyChat) using your server name as the homeserver URL.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `MATRIX_PORT` | `8448` | Host port for the homeserver |
| `MATRIX_SERVER_NAME` | `localhost` | Server name / domain |
| `MATRIX_ALLOW_REGISTRATION` | `true` | Allow new user sign-ups |
| `MATRIX_ALLOW_FEDERATION` | `true` | Enable federation with other servers |

## Service Details

- **Homeserver** — Conduit Matrix homeserver on port 8448 (mapped to container port 6167)
- **Storage** — SQLite-backed (no external database required). Data persisted in the `matrix_data` named volume
- **Federation** — Supports federated messaging with other Matrix homeservers
- **Registration** — New user registration enabled by default. Disable after creating your admin account for security

## Upstream

- [Conduit Website](https://conduit.rs/)
- [GitHub Repository](https://github.com/girlbossceo/conduit)
- [Docker Hub](https://hub.docker.com/r/matrixconduit/matrix-conduit)

