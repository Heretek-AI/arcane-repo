---
title: "Daytona"
description: "Open-source development environment manager"
---

# Daytona

Open-source development environment manager

## Tags

<a href="/categories/devops" class="tag-badge">devops</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/daytona/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/daytona/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/daytona/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `daytona` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `7ebbfb6b91f1ec6b5257532142ebc0b7d723b522cec31ec2dd428b9da04d5cb7` |

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

