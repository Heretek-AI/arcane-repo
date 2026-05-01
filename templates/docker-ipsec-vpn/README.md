# Docker IPSec VPN Server

[Docker IPSec VPN](https://github.com/hwdsl2/docker-ipsec-vpn-server) (7.0k★) — Self-hosted IPsec/L2TP VPN server that provides secure remote access from any device. Supports Windows, macOS, iOS, Android, and Linux clients with built-in IKEv2 and L2TP/IPsec.

> **⚠️ Host Networking Required**  
> This template uses `network_mode: host` — the VPN server requires raw access to the host network stack to handle IPsec protocols (ESP, AH, IKE on ports 500/4500). This bypasses Docker's network isolation. Review the Security Implications section below.
>
> **⚠️ NET_ADMIN Privilege Required**  
> The container runs with `cap_add: [NET_ADMIN]` and `privileged: true`, granting it the ability to modify kernel network settings and load kernel modules. This is required for IPsec but represents elevated risk.

## Security Implications

Before deploying, understand what you're granting:

- **Host networking** (`network_mode: host`) — The container shares the host's network namespace. All ports it binds (500/udp, 4500/udp) are exposed directly on the host. No Docker-proxied port mappings exist.
- **NET_ADMIN capability** — Allows the container to modify routing tables, iptables rules, and kernel network parameters. Required for IPsec to create tunnels.
- **Privileged mode** — Grants access to all devices and enables kernel module loading for IPsec crypto modules.

**Recommendations:**
- Run in an isolated network segment (VLAN/VM) where possible
- Never expose this on a public cloud host without additional firewall rules (restrict UDP 500/4500 to known client IPs)
- Use strong `VPN_IPSEC_PSK` (32+ random characters) and complex `VPN_PASSWORD` values
- Consider WireGuard as a simpler, less privileged alternative for basic VPN needs

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

## Service Details

- **IPsec/L2TP** — Traditional VPN protocol supported by all major OSes natively
- **IKEv2** — Modern, fast, MOBIKE-capable protocol (best for mobile devices that switch networks)
- **Split tunneling** — Configure client-side to route only specific traffic through the VPN
- **Persistent data** — VPN certificates and configuration stored in a named Docker volume

## Client Setup

### Windows 10/11

Settings → Network & Internet → VPN → Add a VPN connection:
- VPN provider: Windows (built-in)
- Connection name: Any name
- Server name or address: Your server's IP
- VPN type: L2TP/IPsec with pre-shared key
- Pre-shared key: Your `VPN_IPSEC_PSK`
- User name: Your `VPN_USER`
- Password: Your `VPN_PASSWORD`

### macOS

System Preferences → Network → + → VPN:
- VPN Type: L2TP over IPSec
- Server Address: Your server's IP
- Account Name: Your `VPN_USER`
- Authentication Settings → Password: `VPN_PASSWORD`, Shared Secret: `VPN_IPSEC_PSK`

### iOS / Android

Use the built-in VPN settings. Both platforms support L2TP/IPsec natively with the same credentials.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Container fails to start | Kernel modules missing | Ensure `af_key`, `esp4`, `ah4`, `xfrm4_mode_tunnel` modules are loaded: `lsmod \| grep -E 'af_key\|esp4'` |
| Client cannot connect | UDP 500/4500 blocked | Verify firewall allows UDP 500 (IKE) and UDP 4500 (NAT-T). Check with: `nc -u <server-ip> 500` |
| iOS/Mac connects but no internet | DNS not pushed correctly | Try setting `VPN_DNS_SRV1` and `VPN_DNS_SRV2` explicitly |
| Windows clients cannot connect | SHA2 truncation bug | Set `VPN_SHA2_TRUNCBUG=yes` (default) as a workaround |

## Upstream

- [GitHub Repository](https://github.com/hwdsl2/docker-ipsec-vpn-server) — 7.0k★
- [Docker Hub](https://hub.docker.com/r/hwdsl2/ipsec-vpn-server)
- [Setup Guide](https://github.com/hwdsl2/setup-ipsec-vpn) — Client setup instructions for all platforms
