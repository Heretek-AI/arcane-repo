# Bytebot — Browser Automation Agent

> **Python library / CLI — not a standalone Docker service.**
> [Bytebot](https://github.com/bytebot-ai/bytebot) is a browser automation agent
> that controls web browsers with natural language. No public Docker image or
> upstream Dockerfile exists. This Docker template provides a minimal
> informational API stub. Use pip for the full Python library experience.

## Quick Start

1. **Start the informational API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

## Full Python Usage (Recommended)

Bytebot is primarily used as a Python library:

```bash
pip install bytebot
```

### Example

```python
from bytebot import Bytebot

bot = Bytebot(api_key="your-key")

# Navigate and interact with a website
result = bot.navigate(
    "https://example.com",
    instruction="click the sign up button"
)
```

### CLI Usage

```bash
bytebot "https://example.com" --instruction "fill the login form"
```

## Configuration

| Variable         | Default  | Description                       |
|------------------|----------|-----------------------------------|
| `BYTEBOT_PORT`   | `8000`   | Host port for the informational API stub |

## API Endpoints

| Endpoint  | Method | Description                                          |
|-----------|--------|------------------------------------------------------|
| `/health` | GET    | Health check + tool info                             |
| `/guide`  | GET    | Python library usage examples and pip instructions   |

## Managing

**View logs:**

```bash
docker compose logs -f bytebot
```

## Troubleshooting

| Symptom                                  | Likely Cause              | Fix                                                            |
|------------------------------------------|---------------------------|----------------------------------------------------------------|
| No browser automation features available | This is a Docker stub     | Install `bytebot` via pip on your host machine                 |
| Container exits immediately              | pip install failure       | Run `docker compose logs bytebot` for details                  |
| Need headless browser interaction        | Using wrong deployment    | Bytebot runs natively — install Python and use pip             |
