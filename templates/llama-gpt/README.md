# llama-gpt -- Self-Hosted Application

llama-gpt is a self-hosted application available through the Umbrel catalog.

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

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `LLAMA_GPT_PORT` | `8000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `llama-gpt` | `docker.io/nativeplanet/llama-gpt:latest` | 8000 | llama-gpt application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f llama-gpt
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull llama-gpt
docker compose up -d
```

## Source

- Umbrel catalog entry: `llama-gpt`
