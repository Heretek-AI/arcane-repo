---
title: "LocalAI"
description: "Self-hosted OpenAI-compatible API for LLMs and embeddings"
---

# LocalAI

Self-hosted OpenAI-compatible API for LLMs and embeddings

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/llm" class="tag-badge">llm</a> <a href="/categories/inference" class="tag-badge">inference</a> <a href="/categories/self-hosted" class="tag-badge">self-hosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/localai/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/localai/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/localai/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `localai` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `93180edb5fe80efe909b866aeccadba41f644d499864f705198427b829b8b909` |

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

