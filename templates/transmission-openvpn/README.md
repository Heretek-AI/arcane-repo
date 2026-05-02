# Transmission-OpenVPN -- Self-Hosted Application

Transmission-OpenVPN is a self-hosted application available through the Portainer catalog.

## Quick Start

1. **Copy and edit the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the application:**

   Open [http://localhost:9091](http://localhost:9091) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `TRANSMISSION_OPENVPN_PORT` | `9091` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `transmission-openvpn` | `docker.io/haugene/transmission-openvpn:latest` | 9091 | Transmission-OpenVPN application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f transmission-openvpn
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull transmission-openvpn
docker compose up -d
```

## Source

- Portainer catalog entry: `Transmission-OpenVPN`
