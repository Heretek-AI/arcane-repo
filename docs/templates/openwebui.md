---
title: "Open WebUI"
description: "Self-hosted ChatGPT-like interface with RAG and multi-user"
---

# Open WebUI

Self-hosted ChatGPT-like interface with RAG and multi-user

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/chat" class="tag-badge">chat</a> <a href="/categories/llm" class="tag-badge">llm</a> <a href="/categories/self-hosted" class="tag-badge">self-hosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openwebui/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openwebui/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openwebui/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `openwebui` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `81b0ac71e34ca8b56e0ce818e899fa5c5b6681f2bfaff0eade5fb9e417f56fcf` |

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

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

