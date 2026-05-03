---
title: "Mem0"
description: "Memory layer for AI applications with entity extraction and retrieval"
---

# Mem0

Memory layer for AI applications with entity extraction and retrieval

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/rag" class="tag-badge">rag</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mem0/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mem0/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mem0/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mem0` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `5560d4839481dd02e382470a4f5f66852ed9fd4eb0accd292daaed721650a826` |

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

