# UFW Docker — Fix Docker + UFW Security Flaw

[UFW Docker](https://github.com/chaifeng/ufw-docker) (6,502 ★) solves the long-standing security issue where Docker-managed iptables rules bypass UFW (Uncomplicated Firewall). Without this tool, Docker published ports are accessible from any IP regardless of UFW policies.

UFW Docker is a CLI-only tool — this template runs it as a `sleep infinity` container. All interaction is via `docker compose exec`.

## The Problem

Docker manipulates iptables directly to expose container ports. Since Docker rules take priority over UFW rules in the iptables chain, any `docker run -p 8080:80` makes port 8080 accessible from **all IPs** — even if UFW blocks it.

## The Fix

ufw-docker adds UFW rules that apply correctly to Docker container traffic:

```bash
# After starting any container with published ports:
docker compose exec ufw-docker ufw-docker allow http-container
# Now port 80 is only accessible from IPs allowed by UFW
```

## Quick Start

1. **Ensure UFW is enabled on the host:**

   ```bash
   sudo ufw enable
   sudo ufw default deny incoming
   sudo ufw allow ssh
   ```

2. **Start ufw-docker:**

   ```bash
   docker compose up -d
   ```

3. **Apply UFW rules to a running container:**

   ```bash
   docker compose exec ufw-docker ufw-docker allow my-web-app
   ```

4. **List managed rules:**

   ```bash
   docker compose exec ufw-docker ufw-docker list
   ```

## Common Commands

| Command | Description |
|---------|-------------|
| `ufw-docker allow <container>` | Add UFW rules for a container |
| `ufw-docker delete allow <container>` | Remove UFW rules for a container |
| `ufw-docker list` | List all managed rules |
| `ufw-docker status` | Show status of managed containers |
| `ufw-docker --help` | Show all commands |

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `UFW_MODE` | `managed` | `managed` to apply rules, `check` for dry-run validation |

## Requirements

- **Linux host** with UFW installed (`sudo apt install ufw` on Debian/Ubuntu)
- Docker daemon running
- `ufw enable` must have been run on the host

## ⚠️ Warning

Incorrect UFW rules can lock you out of your server. Test with `UFW_MODE=check` first and ensure SSH access is explicitly allowed.

Official docs: [github.com/chaifeng/ufw-docker](https://github.com/chaifeng/ufw-docker)
