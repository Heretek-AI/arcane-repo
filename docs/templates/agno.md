---
title: "Agno"
description: "Lightweight AI agent framework for multi-modal agents with tool use and memory"
---

# Agno

Lightweight AI agent framework for multi-modal agents with tool use and memory

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/framework" class="tag-badge">framework</a> <a href="/categories/python" class="tag-badge">python</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agno/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agno/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agno/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `agno` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `380663c8ff83db4b06de74a7dd2cc670a5c3c3536e738f2c4d3d31f2f3b9639a` |

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

