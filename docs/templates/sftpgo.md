---
title: "SFTPGo"
description: "Fully featured SFTP server with web admin UI"
---

# SFTPGo

Fully featured SFTP server with web admin UI

## Tags

<a href="/categories/storage" class="tag-badge">storage</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sftpgo/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sftpgo/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sftpgo/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `sftpgo` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d496762095612a0d2808011ed42abc69f3259eaf0564c32732221237f3a94166` |

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` to set secure credentials:**

   ```ini
   SFTPGO_ADMIN_USER=admin
   SFTPGO_ADMIN_PASSWORD=your-secure-password
   ```

3. **Start the service:**

   ```bash
   docker compose up -d
   ```

4. **Access the web admin UI:**

   Open [http://localhost:8080](http://localhost:8080) and log in with the admin credentials from `.env`.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `SFTPGO_WEB_PORT` | `8080` | Host port for web admin UI |
| `SFTPGO_SFTP_PORT` | `2022` | Host port for SFTP service |
| `SFTPGO_ADMIN_USER` | `admin` | Default admin username |
| `SFTPGO_ADMIN_PASSWORD` | `password` | Default admin password (change in production) |

## Service Details

- **Web Admin UI** — Full management of users, groups, folders, virtual folders, event rules, and quotas on port 8080
- **SFTP Service** — SFTP/SCP access on port 2022
- **Storage** — SQLite-backed database (no external DB required). Data persisted in the `sftpgo_data` named volume
- **Optional backends** — SFTPGo supports S3, GCS, Azure Blob, WebDAV, FTP/S, and HTTP/S endpoints. Configure in the admin UI after startup

## Upstream

- [GitHub Repository](https://github.com/drakkan/sftpgo)
- [Documentation](https://docs.sftpgo.com/)

