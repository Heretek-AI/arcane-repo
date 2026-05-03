---
title: "AgenticRAG-Survey"
description: "Survey of agentic RAG patterns and architectures"
---

# AgenticRAG-Survey

Survey of agentic RAG patterns and architectures

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/research" class="tag-badge">research</a> <a href="/categories/rag" class="tag-badge">rag</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agenticrag/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agenticrag/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agenticrag/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `agenticrag` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `279d79cade5fe48d1a0279cbcdb212c92bd21513c2079a391ae7d657567a3118` |

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

