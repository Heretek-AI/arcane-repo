#!/usr/bin/env python3
"""AstrBot FastAPI wrapper — exposes the AI agent assistant as a REST API."""

import os
import subprocess
import sys
from fastapi import FastAPI

app = FastAPI(
    title='AstrBot',
    version='1.0.0',
    description='AstrBot — AI Agent Assistant integrating IM platforms, LLMs, and plugins (AstrBotDevs/AstrBot)'
)


@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'AstrBot', 'upstream': 'AstrBotDevs/AstrBot'}


@app.get('/info')
async def info():
    return {
        'name': 'AstrBot',
        'description': 'All-in-one AI agent assistant with multi-platform IM integration and plugin system',
        'entrypoint': 'main.py',
        'upstream': 'https://github.com/AstrBotDevs/AstrBot',
        'stars': '31k+'
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('ASTRBOT_PORT', '8000'))

    # Start AstrBot main process in background
    astrbot_main = os.path.join('/app', 'main.py')
    if os.path.isfile(astrbot_main):
        subprocess.Popen(
            [sys.executable, astrbot_main],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    uvicorn.run(app, host='0.0.0.0', port=port)
