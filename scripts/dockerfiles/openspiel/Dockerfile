# OpenSpiel — Multi-stage Dockerfile
# Builds Google DeepMind's OpenSpiel game theory framework
# https://github.com/google-deepmind/open_spiel

FROM python:3.12-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir open-spiel

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN pip install --no-cache-dir uvicorn fastapi

EXPOSE 8080

CMD ["sh", "-c", "\
pip install --no-cache-dir -q uvicorn fastapi && \
cat > /app/server.py << 'PYEOF'
import os
from fastapi import FastAPI

app = FastAPI(title='OpenSpiel', version='1.0.0', description='Google DeepMind OpenSpiel')

@app.get('/health')
async def health():
    import pyspiel
    games = pyspiel.registered_games()
    return {'status': 'ok', 'games_available': len(games), 'framework': 'OpenSpiel'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('OPENSPIEL_PORT', '8080')))
PYEOF
uvicorn server:app --host 0.0.0.0 --port ${OPENSPIEL_PORT:-8080}
"]
