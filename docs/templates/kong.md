---
title: "Kong"
description: "Cloud-native API gateway with plugins for auth, rate limiting, and logging"
---

# Kong

Cloud-native API gateway with plugins for auth, rate limiting, and logging

## Tags

<a href="/categories/api" class="tag-badge">api</a> <a href="/categories/gateway" class="tag-badge">gateway</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kong/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kong/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kong/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `kong` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `05f14f854f1563974e6a88b62020b63d266533d780f8ea64b9b90ce7477257a1` |

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the service:**

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

