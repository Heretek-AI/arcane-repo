---
title: "CasaOS"
description: "Personal cloud operating system for home servers — host-level daemon for managing Docker containers, file sharing, and smart home integration via an intuitive web UI"
---

# CasaOS

Personal cloud operating system for home servers — host-level daemon for managing Docker containers, file sharing, and smart home integration via an intuitive web UI

## Tags

<a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/casaos/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/casaos/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/casaos/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `casaos` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `749ba043a9a3d8ce0184f9de99b4e3481518578604f0723ceb30cfbec0fdc457` |

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

| Variable       | Default | Description                              |
|----------------|---------|------------------------------------------|
| `CASAOS_PORT`  | `8000`  | Host port for the informational API stub |

## Troubleshooting

| Symptom                              | Likely Cause                | Fix                                                                 |
|--------------------------------------|-----------------------------|----------------------------------------------------------------------|
| `curl` returns JSON docs             | Working as intended          | This is an informational stub, not the real CasaOS                    |
| Want the real dashboard              | Using Docker Compose         | Install on your host: `curl -fsSL https://get.casaos.io \| sudo bash` |
| `casaos.service` not found           | Not installed on host        | Run the curl install command above                                   |
| Port 80 already in use               | Conflict with other service  | CasaOS uses port 80 by default — stop the conflicting service first  |
| "Permission denied" during install   | No sudo access               | CasaOS install requires root; use `sudo`                             |

## Links

- [Official Site](https://www.casaos.io/)
- [Wiki & Docs](https://wiki.casaos.io/)
- [GitHub](https://github.com/IceWhaleTech/CasaOS)
- [App Store](https://casaos-appstore.paodayag.dev/)

## API Endpoints

| Endpoint  | Method | Description                                                |
|-----------|--------|------------------------------------------------------------|
| `/health` | GET    | Health check + install command + why this isn't a service  |
| `/guide`  | GET    | Full install guide, feature list, and source link           |

