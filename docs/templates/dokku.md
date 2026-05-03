---
title: "Dokku"
description: "Docker-powered PaaS for single-server deployments — Git-push workflow, plugin system, and Heroku-compatible buildpacks for hosting apps on your own infrastructure"
---

# Dokku

Docker-powered PaaS for single-server deployments — Git-push workflow, plugin system, and Heroku-compatible buildpacks for hosting apps on your own infrastructure

## Tags

<a href="/categories/paas" class="tag-badge">paas</a> <a href="/categories/platform" class="tag-badge">platform</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dokku/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dokku/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dokku/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dokku` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b537747aed1814251238266ba2f1c2b47f8cc45107f46cb9ecdb3529a090729e` |

## Quick Start

```bash
cp .env.example .env
docker compose up -d
```

Verify:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/guide
```

## Configuration

| Variable     | Default | Description                              |
|--------------|---------|------------------------------------------|
| `DOKKU_PORT` | `8000`  | Host port for the informational API stub |

## Troubleshooting

| Symptom                              | Likely Cause                 | Fix                                                                          |
|--------------------------------------|------------------------------|------------------------------------------------------------------------------|
| `curl` returns JSON docs              | Working as intended           | This is an informational stub, not the real dokku daemon                      |
| Want to deploy apps                   | Using Docker Compose          | Install on your host: `wget bootstrap.sh \| sudo bash`                       |
| `dokku` command not found             | Not installed on host         | Run the bootstrap.sh command above                                           |
| `git push dokku main` fails           | SSH key not added             | Run `cat ~/.ssh/id_rsa.pub \| ssh root@<server> dokku ssh-keys:add admin`    |
| "Please install dokku first"          | Plugin requires host install  | Plugins only work with the host-level dokku installation                     |
| Docker image `dokku/dokku:latest` exists | Intended for daemon use    | The image is used by bootstrap.sh internally, not for standalone deployment  |

## Links

- [Official Site](https://dokku.com/)
- [Documentation](https://dokku.com/docs/)
- [GitHub](https://github.com/dokku/dokku)
- [Plugin Directory](https://dokku.com/docs/community/plugins/)

## API Endpoints

| Endpoint  | Method | Description                                                         |
|-----------|--------|---------------------------------------------------------------------|
| `/health` | GET    | Health check + install command + why this isn't a standalone service |
| `/guide`  | GET    | Full install guide, feature list, plugin ecosystem, and source link  |

