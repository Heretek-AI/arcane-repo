# MiroTalk SFU

[MiroTalk SFU](https://github.com/miroslavpejic85/mirotalksfu) — Self-hosted WebRTC video conferencing platform. Multi-party video calls with screen sharing, real-time chat, and optional recording, using a Selective Forwarding Unit (SFU) architecture for efficient media routing.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the web UI:**

   Open [http://localhost:3012](http://localhost:3012).

   Create a new room and share the room link with participants to start a video call.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `MIROTALK_PORT` | `3012` | Host port for the web UI |

## Service Details

- **Web UI** — Conference room interface on port 3012
- **Video Calls** — Multi-party video conferencing with WebRTC
- **Screen Sharing** — Share your entire screen or individual application windows
- **Chat** — Real-time text chat during calls
- **SFU Architecture** — Efficient media routing via Selective Forwarding Unit (one upstream, multiple downstream streams)
- **Recording** — Optional session recording support

## Upstream

- [GitHub Repository](https://github.com/miroslavpejic85/mirotalksfu)
- [Docker Hub](https://hub.docker.com/r/mirotalk/sfu)
