---
title: "Meilisearch"
description: "Fast open-source search engine with typo-tolerant full-text search"
---

# Meilisearch

Fast open-source search engine with typo-tolerant full-text search

## Tags

<a href="/categories/database" class="tag-badge">database</a> <a href="/categories/search" class="tag-badge">search</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/meilisearch/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/meilisearch/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/meilisearch/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `meilisearch` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `03ca51e0e98d9e0d2fb2cce8f76f7511e80a6db921fc9d3aa8557cefe524a2ed` |

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

   Open [http://localhost:7700](http://localhost:7700) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

