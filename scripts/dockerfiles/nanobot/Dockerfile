# NanoBot — Dockerfile
# Builds HKUDS/nanobot research project
# https://github.com/HKUDS/nanobot

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone --depth 1 https://github.com/HKUDS/nanobot.git /tmp/nanobot && \
    cp -r /tmp/nanobot/* /app/ && \
    rm -rf /tmp/nanobot

RUN mkdir -p nanobot bridge && touch nanobot/__init__.py && \
    uv pip install --system --no-cache-dir .

RUN pip install --no-cache-dir uvicorn fastapi

EXPOSE 8000

CMD ["sh", "-c", "\
cat > /app/server.py << 'PYEOF'
import os
from fastapi import FastAPI

app = FastAPI(title='NanoBot', version='1.0.0', description='HKU NanoBot')

@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'NanoBot'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('NANOBOT_PORT', '8000')))
PYEOF
uvicorn server:app --host 0.0.0.0 --port ${NANOBOT_PORT:-8000}
"]
