---
title: "CrewAI"
description: "Multi-agent orchestration framework for AI agent teams"
---

# CrewAI

Multi-agent orchestration framework for AI agent teams

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/orchestration" class="tag-badge">orchestration</a> <a href="/categories/framework" class="tag-badge">framework</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/crewave/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/crewave/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/crewave/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `crewave` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `0bc845b0960fa9b4d9722d0d4419a02e8e97aebf756ebc47d540357c378882df` |

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

> **Status: Library — Uses python:3.12-slim base image**
> This project is a Python library and does not publish a Docker image.
> The template installs it via `pip install` at container startup.

