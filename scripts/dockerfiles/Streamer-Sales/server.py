#!/usr/bin/env python3
"""Streamer-Sales FastAPI wrapper — exposes the live stream sales AI bot as a REST API.

Upstream compose.yaml defines 7+ services; this template simplifies to the core sales bot
with a FastAPI entrypoint. Users needing the full multi-service architecture should reference
the upstream compose.yaml directly.
"""

import os
import subprocess
import sys
from fastapi import FastAPI

app = FastAPI(
    title='Streamer-Sales',
    version='1.0.0',
    description='Streamer-Sales — AI-powered live stream sales assistant bot (PeterH0323/Streamer-Sales, 3.6k★). Simplified from 7+ services to core sales bot.'
)


@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'Streamer-Sales', 'upstream': 'PeterH0323/Streamer-Sales'}


@app.get('/info')
async def info():
    return {
        'name': 'Streamer-Sales',
        'description': 'AI live stream sales assistant — core bot service simplified from upstream 7+ service architecture',
        'upstream': 'https://github.com/PeterH0323/Streamer-Sales',
        'backend': 'Python',
        'stars': '3.6k+',
        'upstream_services': 7,
        'note': 'Simplified to core bot. Full 7-service deployment: see upstream compose.yaml'
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('STREAMER_SALES_PORT', '8000'))

    # Start core sales bot process
    app_dir = '/app'
    entrypoints = ['main.py', 'app.py', 'run.py', 'server.py', 'bot.py']
    for ep in entrypoints:
        ep_path = os.path.join(app_dir, ep)
        if os.path.isfile(ep_path):
            subprocess.Popen(
                [sys.executable, ep_path],
                cwd=app_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            break

    uvicorn.run(app, host='0.0.0.0', port=port)
