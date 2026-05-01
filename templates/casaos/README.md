# CasaOS — Personal Cloud Operating System

> **Host-level daemon — NOT deployable via `docker compose up`.**
> [CasaOS](https://www.casaos.io/) is a personal cloud OS installed as a native Go binary
> on the host system. It manages Docker containers, file sharing, and smart home
> integration through an intuitive web UI. This Docker Compose template provides a
> minimal informational API stub.
>
> **Install on your host OS:** `curl -fsSL https://get.casaos.io | sudo bash`

## Why Not Docker Compose?

CasaOS is a **host-level daemon** — it installs as a Go binary directly on the host
filesystem, registers a `casaos.service` systemd unit, and manages Docker containers
from outside Docker. Creating a Docker Compose wrapper for it would:

1. **Misrepresent** the project's architecture — CasaOS is not a service you run *in* Docker,
   it's the layer that manages Docker.
2. **Add unnecessary complexity** — Docker-in-Docker or socket-mount configurations that
   the upstream developers never intended.
3. **Break plugin compatibility** — CasaOS plugins expect host-level filesystem access
   and systemd integration that a containerized wrapper can't provide.

This follows the same rationale as [D009](../.gsd/DECISIONS.md#D009) for K8s-native tools:
Docker Compose wrappers for tools that fundamentally manage Docker/the host OS mislead users.

## Quick Start (Informational API Stub)

```bash
cp .env.example .env
docker compose up -d
```

Verify:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/guide
```

## Full Installation (Recommended — On Your Host OS)

CasaOS is designed to be installed directly on a Linux server or Raspberry Pi:

```bash
# Prerequisites: Ubuntu Server 20.04+ / Debian 11+ / Raspberry Pi OS
sudo apt update && sudo apt install -y curl

# Install CasaOS
curl -fsSL https://get.casaos.io | sudo bash
```

The install script:
1. Downloads the CasaOS Go binary to `/opt/casaos/`
2. Registers `casaos.service` via systemd
3. Starts the web UI on port 80
4. Auto-detects Docker and shows existing containers in the dashboard

### Post-Install

Open `http://<your-server-ip>/` in a browser.

CasaOS provides:
- **File Manager** — drag-and-drop uploads, folder sharing, multi-user
- **App Store** — one-click install for 100+ Docker apps (Plex, Jellyfin, Home Assistant, etc.)
- **Smart Home** — Home Assistant compatible, MQTT integration
- **Monitoring** — system dashboard with CPU, RAM, disk, and network stats
- **Remote Access** — DDNS and CasaConnect for accessing your server from anywhere

## Configuration

| Variable       | Default | Description                              |
|----------------|---------|------------------------------------------|
| `CASAOS_PORT`  | `8000`  | Host port for the informational API stub |

## API Endpoints

| Endpoint  | Method | Description                                                |
|-----------|--------|------------------------------------------------------------|
| `/health` | GET    | Health check + install command + why this isn't a service  |
| `/guide`  | GET    | Full install guide, feature list, and source link           |

## Managing

**View logs:**

```bash
# On your host (after full install):
sudo systemctl status casaos
sudo journalctl -u casaos -f

# For this Docker stub:
docker compose logs -f casaos
```

**Uninstall (host):**

```bash
casaos-uninstall
# or manually:
sudo systemctl stop casaos && sudo systemctl disable casaos
sudo rm -rf /opt/casaos /etc/systemd/system/casaos.service
```

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
