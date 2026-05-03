---
title: "Hermes-Agent"
description: "Nous Research autonomous AI agent framework"
---

# Hermes-Agent

Nous Research autonomous AI agent framework

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/framework" class="tag-badge">framework</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hermesagent/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hermesagent/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hermesagent/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `hermesagent` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `06b512d6529a546ba9fb2c807c4a2c060467ff1933cfad9e778ce37e6f078fa4` |

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

