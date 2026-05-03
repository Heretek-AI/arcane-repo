---
title: "Quivr"
description: "Open-source second brain with RAG-powered Q&amp;A and knowledge management"
---

# Quivr

Open-source second brain with RAG-powered Q&amp;A and knowledge management

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/rag" class="tag-badge">rag</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/quivr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/quivr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/quivr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `quivr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `019437bf6de35be7d851cf3e41727328d1a9ec85417ec19b8a2c477a4c1aef48` |

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

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

