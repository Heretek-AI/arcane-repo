---
title: "LobeHub"
description: "Modern AI chat platform with plugin ecosystem and multi-LLM support"
---

# LobeHub

Modern AI chat platform with plugin ecosystem and multi-LLM support

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/chat" class="tag-badge">chat</a> <a href="/categories/llm" class="tag-badge">llm</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lobehub/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lobehub/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lobehub/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `lobehub` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `fc9c4762b3f3554f177684bd149a48c8db476698ed06f9289410045b4e1973d3` |

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

   Open [http://localhost:3210](http://localhost:3210) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

