---
title: "SillyTavern"
description: "LLM chat frontend for interacting with various AI backends — text generation, roleplay, and character management"
---

# SillyTavern

LLM chat frontend for interacting with various AI backends — text generation, roleplay, and character management

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/chat" class="tag-badge">chat</a> <a href="/categories/llm" class="tag-badge">llm</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sillytavern/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sillytavern/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sillytavern/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `sillytavern` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `336d1cce989e6b32c3a93e01fb9d05960a12976933bb571bc00c7b1565222d6a` |

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

> **Status: 🏗️ CI Build Pending**
> The upstream project includes a Dockerfile, but no pre-built image is published. The template currently
> references a non-existent image. A CI pipeline will build and publish to GHCR (planned for future update).

