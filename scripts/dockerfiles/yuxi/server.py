#!/usr/bin/env python3
"""Yuxi FastAPI wrapper — exposes the multi-agent LLM conversation platform as a REST API."""

import os
import subprocess
import sys
from fastapi import FastAPI

app = FastAPI(
    title='Yuxi',
    version='1.0.0',
    description='Yuxi — multi-agent LLM conversation platform with knowledge base integration (xerrors/Yuxi, 5k★)'
)


@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'Yuxi', 'upstream': 'xerrors/Yuxi'}


@app.get('/info')
async def info():
    return {
        'name': 'Yuxi',
        'description': 'Multi-agent LLM conversation platform with modular agent architecture, knowledge base, and tool integration',
        'upstream': 'https://github.com/xerrors/Yuxi',
        'backend': 'Python',
        'stars': '5k+'
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('YUXI_PORT', '8000'))

    # Start Yuxi backend process
    app_dir = '/app'
    # Try common entrypoints
    entrypoints = ['main.py', 'app.py', 'server.py', 'run.py']
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
