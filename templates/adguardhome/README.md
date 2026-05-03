# AdGuard Home — Network-Wide DNS Ad Blocker

[AdGuard Home](https://github.com/AdguardTeam/AdGuardHome) is a network-wide DNS server that blocks ads, trackers, and malicious domains at the network level. Every device on your network — phones, laptops, smart TVs, IoT gadgets — gets ad blocking without installing anything. It also provides parental controls, safe browsing, and detailed query logging.

This template deploys AdGuard Home as a single Docker container with persistent configuration.

## Project Overview

AdGuard Home acts as a DNS server that sits between your devices and upstream DNS providers (like Google, Cloudflare, or your ISP). When a device asks "what's the IP address for ads.example.com?", AdGuard Home checks it against blocklists and returns nothing — the ad never loads.

**Who it's for:**
- Home users who want whole-network ad blocking without per-device setup
- Parents who want content filtering and safe search enforcement
- Anyone who wants visibility into what domains their devices are contacting
- Self-hosters looking for a lightweight Pi-hole alternative with a modern UI

**Key features:**
- DNS-level ad and tracker blocking with community-maintained blocklists
- Parental controls and safe browsing enforcement
- Per-client configuration and statistics
- DNS-over-HTTPS (DoH) and DNS-over-TLS (DoT) support
- Query log with filtering and statistics dashboard
- Built-in DHCP server (optional)
- HTTPS admin interface

## Architecture

This template runs a single AdGuard Home container.

### Services

| Service        | Image                          | Purpose                        |
|----------------|--------------------------------|--------------------------------|
| `adguardhome`  | `adguard/adguardhome:latest`   | DNS server + admin web UI      |

### Volumes

| Volume                | Container Path | Purpose                                    |
|-----------------------|----------------|--------------------------------------------|
| `adguardhome_data`    | `/data`        | Configuration, filters, query logs, stats  |

All AdGuard Home state — your configuration, blocklists, query history, and client data — lives in the `adguardhome_data` named volume. This survives container restarts and upgrades.

### Ports

| Port  | Protocol | Purpose                  |
|-------|----------|--------------------------|
| `8080`| TCP      | Admin web interface      |

The admin UI is the only port exposed by default. To use AdGuard Home as your actual DNS server, you'll need to expose additional ports — see [Enabling DNS Resolution](#enabling-dns-resolution) below.

### Health Check

The container includes a health check that pings the admin UI on port 8080 every 30 seconds. Docker reports the container as unhealthy if the web interface becomes unresponsive.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the container:**

   ```bash
   docker compose up -d
   ```

3. **Open the admin interface:**

   Navigate to `http://localhost:8080` (or `http://<your-server-ip>:8080`).

4. **Run the setup wizard:**

   On first launch, AdGuard Home walks you through:
   - Setting an admin username and password
   - Choosing an upstream DNS provider (e.g., `https://dns.cloudflare.com/dns-query`)
   - Selecting blocklists to enable

5. **Configure your network:**

   Point your router's DNS settings to your server's IP address. All devices on the network will start using AdGuard Home automatically.

## Enabling DNS Resolution

The default template only exposes the admin UI. To use AdGuard Home as an actual DNS resolver, add port mappings to `docker-compose.yml`:

```yaml
ports:
  - "${ADGUARDHOME_PORT:-8080}:8080"       # Admin UI
  - "53:53/tcp"                             # DNS (TCP)
  - "53:53/udp"                             # DNS (UDP)
```

**Important:** Port 53 is commonly used by `systemd-resolved` on Linux. If port 53 is already in use:

```bash
# Check what's using port 53
sudo lsof -i :53

# If systemd-resolved is using it, disable and configure differently:
sudo systemctl disable systemd-resolved
sudo systemctl stop systemd-resolved
```

For DNS-over-HTTPS and DNS-over-TLS (optional):

```yaml
ports:
  - "${ADGUARDHOME_PORT:-8080}:8080"       # Admin UI
  - "53:53/tcp"                             # DNS (TCP)
  - "53:53/udp"                             # DNS (UDP)
  - "443:443/tcp"                           # DNS-over-HTTPS
  - "853:853/tcp"                           # DNS-over-TLS
```

## Configuration Reference

Copy `.env.example` to `.env` and adjust values as needed.

| Variable             | Default | Description                                          |
|----------------------|---------|------------------------------------------------------|
| `ADGUARDHOME_PORT`   | `8080`  | Host port for the AdGuard Home admin web interface   |

All other configuration (upstream DNS, blocklists, client settings, parental controls) is managed through the AdGuard Home web interface and stored in the `adguardhome_data` volume.

### Upstream DNS Providers

Common upstream DNS providers you can configure in the web UI:

| Provider              | Address                                      |
|-----------------------|----------------------------------------------|
| Cloudflare            | `https://dns.cloudflare.com/dns-query`       |
| Google                | `https://dns.google/dns-query`               |
| Quad9                 | `https://dns.quad9.net/dns-query`            |
| AdGuard               | `https://dns.adguard-dns.com/dns-query`      |
| OpenDNS               | `https://doh.opendns.com/dns-query`          |
| NextDNS               | `https://dns.nextdns.io`                     |

## Troubleshooting

### Container won't start — port 53 already in use

If you've added DNS port mappings and the container fails to start:

```bash
# Find what's occupying port 53
sudo ss -tlnp | grep :53

# On systems with systemd-resolved:
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved
```

### Admin UI not loading

Check container health:

```bash
docker compose ps
docker compose logs adguardhome
```

If the container is restarting, the data volume may be corrupted. Try recreating it:

```bash
docker compose down
docker volume rm adguardhome_data
docker compose up -d
```

**Warning:** This deletes all configuration and query history.

### DNS queries not being blocked

1. Verify your devices are actually using AdGuard Home as their DNS server (check the query log in the admin UI).
2. Ensure blocklists are loaded — go to **Filters > DNS blocklists** and update them.
3. Some devices cache DNS aggressively. Flush DNS on the client:
   - **Windows:** `ipconfig /flushdns`
   - **macOS:** `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
   - **Linux:** `sudo resolvectl flush-caches`

### Slow DNS resolution

AdGuard Home can be slow if upstream DNS is slow. Try switching to a faster provider like Cloudflare (`1.1.1.1`) or Google (`8.8.8.8`). You can also enable caching in the admin UI under **Settings > DNS settings**.

### HTTPS certificate errors for DoH

DNS-over-HTTPS requires a valid TLS certificate. AdGuard Home can use Let's Encrypt if you have a domain pointed at your server. Configure this under **Settings > Encryption settings** in the admin UI.

## Backup & Recovery

### What to back up

All persistent data lives in the `adguardhome_data` Docker volume. This includes:
- AdGuard Home configuration (`AdGuardHome.yaml`)
- DNS filter lists and custom rules
- Query logs and statistics
- Client settings and profiles

### Manual backup

```bash
# Stop the container to ensure consistent state
docker compose down

# Create a tarball of the volume
docker run --rm -v adguardhome_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/adguardhome-backup-$(date +%Y%m%d).tar.gz -C /data .

# Restart
docker compose up -d
```

### Restore from backup

```bash
# Stop the container
docker compose down

# Restore the volume
docker run --rm -v adguardhome_data:/data -v $(pwd):/backup alpine \
  sh -c "rm -rf /data/* && tar xzf /backup/adguardhome-backup-YYYYMMDD.tar.gz -C /data"

# Restart
docker compose up -d
```

### Export configuration from the UI

AdGuard Home also supports exporting configuration directly from the admin interface:
1. Go to **Settings > General settings**
2. Click **Export** to download a YAML configuration file

To restore, use the **Import** button on the same page.

## Links

- **Original project:** [github.com/AdguardTeam/AdGuardHome](https://github.com/AdguardTeam/AdGuardHome)
- **Official documentation:** [github.com/AdguardTeam/AdGuardHome/wiki](https://github.com/AdguardTeam/AdGuardHome/wiki)
- **Docker Hub:** [hub.docker.com/r/adguard/adguardhome](https://hub.docker.com/r/adguard/adguardhome)
- **Blocklists:** [AdGuard DNS filter](https://github.com/AdguardTeam/AdGuardSDNSFilter), [community lists](https://github.com/blocklistproject/Lists)
- **Community:** [AdGuard Home Discussions](https://github.com/AdguardTeam/AdGuardHome/discussions)
