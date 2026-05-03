---
title: "Docker IPSec VPN Server"
description: "Self-hosted IPsec/L2TP VPN server — secure remote access, split tunneling, and multi-platform client support (Windows, macOS, iOS, Android, Linux)"
---

# Docker IPSec VPN Server

Self-hosted IPsec/L2TP VPN server — secure remote access, split tunneling, and multi-platform client support (Windows, macOS, iOS, Android, Linux)

## Tags

<a href="/categories/security" class="tag-badge">security</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docker-ipsec-vpn/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docker-ipsec-vpn/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docker-ipsec-vpn/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `docker-ipsec-vpn` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ea65977c7283587bd2024106063f00e229e43dfce75444d4a66dcd02d3407c85` |

## Quick Start

1. **Copy the environment file and configure credentials:**

   ```bash
   cp .env.example .env
   # Edit .env — set VPN_IPSEC_PSK, VPN_USER, VPN_PASSWORD
   ```

2. **Start the VPN server:**

   ```bash
   docker compose up -d
   ```

3. **Connect clients:**

   Your VPN credentials are:
   - **Server:** Your host's public IP address
   - **IPsec PSK:** `VPN_IPSEC_PSK` value from `.env`
   - **Username:** `VPN_USER` value from `.env`
   - **Password:** `VPN_PASSWORD` value from `.env`

   Set up the VPN connection on each client using the built-in L2TP/IPsec or IKEv2 VPN client. On most platforms (Windows, macOS, iOS, Android), no additional software is needed — use the OS-native VPN settings.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `VPN_IPSEC_PSK` | *(required)* | IPsec Pre-Shared Key — shared secret all clients must present |
| `VPN_USER` | `vpnuser` | VPN username |
| `VPN_PASSWORD` | *(required)* | VPN password |
| `VPN_DNS_SRV1` | `8.8.8.8` | Primary DNS server pushed to VPN clients |
| `VPN_DNS_SRV2` | `8.8.4.4` | Secondary DNS server pushed to VPN clients |
| `VPN_SHA2_TRUNCBUG` | `yes` | Windows 10/11 SHA2 truncation bug workaround. Set to `no` if all Windows clients are fully updated |

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Container fails to start | Kernel modules missing | Ensure `af_key`, `esp4`, `ah4`, `xfrm4_mode_tunnel` modules are loaded: `lsmod \| grep -E 'af_key\|esp4'` |
| Client cannot connect | UDP 500/4500 blocked | Verify firewall allows UDP 500 (IKE) and UDP 4500 (NAT-T). Check with: `nc -u <server-ip> 500` |
| iOS/Mac connects but no internet | DNS not pushed correctly | Try setting `VPN_DNS_SRV1` and `VPN_DNS_SRV2` explicitly |
| Windows clients cannot connect | SHA2 truncation bug | Set `VPN_SHA2_TRUNCBUG=yes` (default) as a workaround |

## Service Details

- **IPsec/L2TP** — Traditional VPN protocol supported by all major OSes natively
- **IKEv2** — Modern, fast, MOBIKE-capable protocol (best for mobile devices that switch networks)
- **Split tunneling** — Configure client-side to route only specific traffic through the VPN
- **Persistent data** — VPN certificates and configuration stored in a named Docker volume

## Upstream

- [GitHub Repository](https://github.com/hwdsl2/docker-ipsec-vpn-server) — 7.0k★
- [Docker Hub](https://hub.docker.com/r/hwdsl2/ipsec-vpn-server)
- [Setup Guide](https://github.com/hwdsl2/setup-ipsec-vpn) — Client setup instructions for all platforms

