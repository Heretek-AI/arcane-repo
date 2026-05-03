---
title: "Mailcow"
description: "Mailcow mail server suite — full email stack with Postfix, Dovecot, Rspamd, SOGo, and more. The dockerized version is its own compose repo (circular dependency); this template provides an informational API stub"
---

# Mailcow

Mailcow mail server suite — full email stack with Postfix, Dovecot, Rspamd, SOGo, and more. The dockerized version is its own compose repo (circular dependency); this template provides an informational API stub

## Tags

<a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mailcow/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mailcow/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mailcow/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mailcow` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `4df191d250c6fa69ded098b25a0c27a8a04d7a6eed0fce356e35f1fa63e34966` |

## Quick Start

1. **Start the informational API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

## Configuration

| Variable        | Default  | Description                       |
|-----------------|----------|-----------------------------------|
| `MAILCOW_PORT`  | `8000`   | Host port for the informational API stub |

## Troubleshooting

| Symptom                          | Likely Cause              | Fix                                                              |
|----------------------------------|---------------------------|------------------------------------------------------------------|
| No mail server functionality     | This is a Docker stub     | Clone `mailcow/mailcow-dockerized` and deploy directly           |
| Container exits immediately      | pip install failure       | Run `docker compose logs mailcow` for details                    |
| Need full email stack            | Using wrong deployment    | Mailcow provides its own compose — use it directly               |

## API Endpoints

| Endpoint  | Method | Description                                          |
|-----------|--------|------------------------------------------------------|
| `/health` | GET    | Health check + circular dependency info              |
| `/guide`  | GET    | Clone-and-deploy instructions for the upstream repo  |

