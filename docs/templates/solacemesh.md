---
title: "Solace Agent Mesh"
description: "Event-driven multi-agent framework with real-time collaboration"
---

# Solace Agent Mesh

Event-driven multi-agent framework with real-time collaboration

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/solacemesh/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/solacemesh/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/solacemesh/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `solacemesh` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8d3ab66af6f65d80e5d3ef9de9b85c884a3a8f09f497ef3a3bc5ed4ffe8d8793` |

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

