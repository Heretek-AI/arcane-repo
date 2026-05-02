# RustScan — The Modern Port Scanner

[RustScan](https://github.com/bee-san/RustScan) (19,698 ★) scans all 65,535 ports in ~3 seconds using adaptive learning and batch scanning. It automatically feeds discovered open ports into Nmap for service fingerprinting.

RustScan is a CLI-only tool — this template runs it as a `sleep infinity` container. All interaction is via `docker compose exec`.

## Quick Start

1. **Start the container:**

   ```bash
   docker compose up -d
   ```

2. **Scan a single host:**

   ```bash
   docker compose exec rustscan rustscan -a 192.168.1.1
   ```

3. **Scan a subnet with Nmap service detection:**

   ```bash
   docker compose exec rustscan rustscan -a 10.0.0.0/24 -- -A
   ```

4. **Scan from a file of targets:**

   ```bash
   docker compose exec rustscan rustscan -a targets.txt
   ```

## Common Commands

| Command | Description |
|---------|-------------|
| `rustscan -a <ip>` | Scan a single IP address |
| `rustscan -a <cidr>` | Scan a subnet (e.g. 192.168.1.0/24) |
| `rustscan -a <file>` | Scan targets from a file |
| `rustscan -a <ip> -- -sV` | Discover open ports, then Nmap service version |
| `rustscan -a <ip> -- -A` | Full Nmap scan (OS, version, scripts, traceroute) |
| `rustscan -p 80,443` | Scan specific ports only |
| `rustscan --help` | Show all options |

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `RUSTSCAN_BATCH_SIZE` | `4500` | Ports scanned simultaneously |
| `RUSTSCAN_TIMEOUT` | `1500` | Response timeout in milliseconds |
| `RUSTSCAN_ULIMIT` | `5000` | File descriptor limit |

## Performance Notes

- **With CAP_NET_RAW** (default): Full-speed SYN scans. Requires `network_mode: host`.
- **Without CAP_NET_RAW**: Falls back to TCP connect mode. Reduce `RUSTSCAN_BATCH_SIZE` to ~500 to avoid rate-limiting.

## ⚠️ Legal Notice

Only scan hosts and networks you own or have explicit written permission to test. Unauthorized port scanning is illegal in most jurisdictions.

Official docs: [github.com/bee-san/RustScan/wiki](https://github.com/bee-san/RustScan/wiki)
