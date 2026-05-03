---
title: "Chroma"
description: "Open-source embedding database for RAG and similarity search"
---

# Chroma

Open-source embedding database for RAG and similarity search

## Tags

<a href="/categories/database" class="tag-badge">database</a> <a href="/categories/rag" class="tag-badge">rag</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chroma/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chroma/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chroma/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `chroma` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `dcf292595417ab17b33f26ba07a1738ef531ff9ed2735dca8d8f51fca4a318f2` |

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

