#!/usr/bin/env python3
"""Xiaomusic healthcheck wrapper — monitors the xiaomusic process and exposes /health."""

import os
import subprocess
from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title='Xiaomusic',
    version='1.0.0',
    description='Xiaomusic — Xiaomi smart speaker music player with LLM integration for natural language music control'
)


@app.get('/health')
async def health():
    """Health check — verify xiaomusic process is running."""
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'xiaomusic.py'],
            capture_output=True,
            text=True,
            timeout=5
        )
        running = result.returncode == 0
        return {
            'status': 'ok' if running else 'degraded',
            'process': 'xiaomusic.py',
            'running': running,
            'web_port': 8090,
            'upstream': 'hanxi/xiaomusic'
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}


if __name__ == '__main__':
    port = int(os.environ.get('XIAOMUSIC_HEALTH_PORT', '8091'))
    uvicorn.run(app, host='0.0.0.0', port=port)
