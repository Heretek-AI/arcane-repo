# Sunshine — Game Stream Host

[Sunshine](https://github.com/LizardByte/Sunshine) (36k+ ★) is a self-hosted game stream host for Moonlight. Stream games, desktop, and applications to any Moonlight client — PC, phone, tablet, or TV — with low-latency hardware-accelerated encoding.

> **⚠️ Host Networking Required**  
> Sunshine uses `network_mode: host` so it can advertise itself via mDNS and accept RTSP connections from Moonlight clients on your local network. Without host networking, clients won't discover the host automatically.

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

## GPU / Hardware Encoding

Sunshine uses GPU hardware encoding for low-latency streaming. Uncomment the appropriate section in `docker-compose.yml`:

**Intel / AMD GPUs (VA-API):**

```yaml
devices:
  - /dev/dri:/dev/dri
```

**NVIDIA GPUs:**

```yaml
runtime: nvidia
environment:
  - NVIDIA_VISIBLE_DEVICES=all
```

> Requires the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).

## Gamepad Passthrough

To pass game controllers through to the container:

```yaml
devices:
  - /dev/uinput:/dev/uinput
```

## Network Ports

Sunshine uses the following ports (all handled automatically by `network_mode: host`):

| Port Range        | Protocol | Purpose              |
|-------------------|----------|----------------------|
| `47984–47990`     | TCP      | RTSP, control, video |
| `48010`           | TCP      | Web UI               |
| `47998–48000`     | UDP      | Video streaming      |

## Upstream

- **Repository:** [LizardByte/Sunshine](https://github.com/LizardByte/Sunshine)
- **Stars:** 36k+
- **License:** GPL-3.0
- **Documentation:** [docs.lizardbyte.dev](https://docs.lizardbyte.dev/projects/sunshine/)
