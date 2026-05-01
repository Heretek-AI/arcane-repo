# Dokku — Docker-Powered PaaS

> **Host-level PaaS — NOT deployable via `docker compose up`.**
> [Dokku](https://dokku.com/) is a Docker-powered Platform-as-a-Service installed via
> `bootstrap.sh` to the host operating system. It configures SSH (git-push deploys),
> nginx (per-app virtual hosts), and the plugin system at the host level. This Docker
> Compose template provides a minimal informational API stub.
>
> **Install on your host OS:** `wget -qO- https://dokku.com/install/v0.35.15/bootstrap.sh | sudo bash`

## Why Not Docker Compose?

Although a Docker image exists (`dokku/dokku:latest`), Dokku is fundamentally a
**host-level PaaS** — the `bootstrap.sh` process performs host OS configuration that a
standalone container cannot replicate:

1. **SSH integration** — Dokku adds a `dokku` system user and configures SSH command
   forwarding so `git push dokku main` triggers builds.
2. **Nginx reverse proxy** — Each deployed app gets its own nginx virtual host,
   configured at the host level.
3. **Plugin system** — Plugins (PostgreSQL, Redis, Let's Encrypt) require host-level
   filesystem access and service management.
4. **Systemd integration** — Dokku services run as systemd units managed by the host.

Docker Compose wrappers for tools that fundamentally manage Docker/the host OS
mislead users — this follows the same exclusion rationale as [D009](../.gsd/DECISIONS.md#D009)
for K8s-native tools and the host-level daemon classification extended in MEM063.

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

Dokku requires a fresh Ubuntu server (virtual machine or bare metal):

```bash
# Prerequisites:
#   - Ubuntu 20.04/22.04/24.04 x64 (fresh install)
#   - At least 1 GB RAM
#   - A domain/subdomain pointing to the server IP
#   - SSH access with a key pair

# Install Dokku
wget -qO- https://dokku.com/install/v0.35.15/bootstrap.sh | sudo bash
```

The bootstrap script:
1. Installs Docker Engine
2. Creates the `dokku` system user
3. Configures SSH command forwarding for git-push deploys
4. Sets up nginx as a reverse proxy
5. Initializes the plugin management system
6. Prompts for your domain and SSH key

### Post-Install

Open `http://<your-server-ip>/` in a browser to complete setup:
- Set your domain
- Add your SSH public key
- Configure Let's Encrypt for HTTPS

### Deploying Your First App

```bash
# On your local machine:
git clone https://github.com/heroku/node-js-sample.git
cd node-js-sample
git remote add dokku dokku@<your-server>:myapp
git push dokku main

# Dokku detects the Node.js app, builds it with Heroku buildpacks,
# starts it in a Docker container, and proxies it through nginx.
```

### Common Plugins

```bash
# PostgreSQL
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres
dokku postgres:create mydb
dokku postgres:link mydb myapp

# Let's Encrypt
sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku letsencrypt:enable myapp

# Redis
sudo dokku plugin:install https://github.com/dokku/dokku-redis.git redis
```

## Configuration

| Variable     | Default | Description                              |
|--------------|---------|------------------------------------------|
| `DOKKU_PORT` | `8000`  | Host port for the informational API stub |

## API Endpoints

| Endpoint  | Method | Description                                                         |
|-----------|--------|---------------------------------------------------------------------|
| `/health` | GET    | Health check + install command + why this isn't a standalone service |
| `/guide`  | GET    | Full install guide, feature list, plugin ecosystem, and source link  |

## Managing (Host Install)

```bash
# Check dokku version
dokku version

# List deployed apps
dokku apps:list

# View app logs
dokku logs myapp -t

# Scale app processes
dokku ps:scale myapp web=2 worker=1

# Set environment variables
dokku config:set myapp NODE_ENV=production

# Restart an app
dokku ps:restart myapp
```

For this Docker stub:

```bash
docker compose logs -f dokku
```

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
