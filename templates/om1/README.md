# OM1 — Modular AI Runtime for Robots

[OM1](https://github.com/OpenMind/OM1) (1.5k+ ★) is a multi-modal AI agent runtime designed for robots and embodied AI systems. It combines vision, audio, speech, and language models into a unified agent framework.

## ⚠️ Hardware Requirements

OM1 is designed for **hardware-integrated environments**. Full functionality requires:
- **Camera**: USB/webcam accessible at `/dev/video0` (V4L2)
- **Microphone**: ALSA/PulseAudio input device
- **Speaker**: PulseAudio output sink (default_output_aec)
- **GPU**: Optional — CUDA or ROCm for accelerated inference

## Container Limitations

This container runs in **headless mode** by default — it provides a FastAPI health/info API but **cannot exercise OM1's full AI runtime** without hardware passthrough. For full functionality:

```bash
# Expose hardware devices to the container:
docker compose -f docker-compose.hw.yml up -d
```

Or modify `docker-compose.yml` to uncomment the `devices` and `volumes` sections.

## Quick Start (Headless)

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Check health:**

   ```bash
   curl http://localhost:8000/health
   ```

4. **View service details:**

   ```bash
   curl http://localhost:8000/info
   ```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OM1_PORT` | `8000` | Host port for the FastAPI wrapper |
| `OM1_HEADLESS` | `true` | Run in headless mode (no hardware) |
| `OM1_SKIP_INTERNET_CHECK` | `true` | Skip startup internet check |

## Architecture

This template uses a custom Dockerfile (`scripts/dockerfiles/om1/Dockerfile`) that builds OM1's upstream source with cyclonedds, ffmpeg, PulseAudio, and ALSA system dependencies. The image is published to GHCR via CI (`.github/workflows/build-om1.yml`). A FastAPI wrapper provides health-check and info endpoints.

## API Endpoints

| Endpoint  | Method | Description                  |
|-----------|--------|------------------------------|
| `/health` | GET    | Health check + mode status   |
| `/info`   | GET    | Upstream details + hardware requirements |

## Upstream

- **Repository:** [OpenMind/OM1](https://github.com/OpenMind/OM1)
- **Stars:** 1.5k+
- **License:** MIT
