---
title: "Deer-Flow"
description: "Real-time event processing and workflow automation engine"
---

# Deer-Flow

Real-time event processing and workflow automation engine

## Tags

<a href="/categories/automation" class="tag-badge">automation</a> <a href="/categories/workflow" class="tag-badge">workflow</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/deerflow/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/deerflow/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/deerflow/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `deerflow` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e73ce72cb071e82699945eb5e098efd32bda07f07a321a1ff3499db77d3baa40` |

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

