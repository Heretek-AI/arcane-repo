---
title: "Sunshine"
description: "Self-hosted game stream host for Moonlight — stream games to any device"
---

# Sunshine

Self-hosted game stream host for Moonlight — stream games to any device

## Tags

<a href="/categories/web" class="tag-badge">web</a> <a href="/categories/tools" class="tag-badge">tools</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sunshine/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sunshine/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sunshine/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `sunshine` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `9f864eac297dc5e6351924e0dc2906d76c317485d4ada1924f733c5016bd6b1d` |

## Quick Start

1. **Start Sunshine:**

   ```bash
   docker compose up -d
   ```

2. **Pair with Moonlight:**
   - Open the Moonlight client on your device
   - If Sunshine doesn't appear automatically, add the host manually using your machine's IP
   - Pair with the PIN shown in the Sunshine web UI

3. **Access the web UI:**

   Open [http://localhost:47990](http://localhost:47990) to configure Sunshine.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable        | Default | Description                    |
|-----------------|---------|--------------------------------|
| `SUNSHINE_UID`  | `1000`  | User ID for the sunshine process |
| `SUNSHINE_GID`  | `1000`  | Group ID for the sunshine process |
| `SUNSHINE_TZ`   | `UTC`   | Timezone for the container     |

## Upstream

- **Repository:** [LizardByte/Sunshine](https://github.com/LizardByte/Sunshine)
- **Stars:** 36k+
- **License:** GPL-3.0
- **Documentation:** [docs.lizardbyte.dev](https://docs.lizardbyte.dev/projects/sunshine/)

