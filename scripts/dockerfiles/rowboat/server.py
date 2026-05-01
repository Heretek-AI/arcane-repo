#!/usr/bin/env python3
"""Rowboat FastAPI wrapper — starts Next.js server as subprocess and exposes /healthz and /info endpoints.

Rowboat upstream (rowboatlabs/rowboat) is a Next.js app.
The wrapper starts node server.js (Next.js standalone on port 3000) and provides
health/info endpoints on a separate port (default 8000) exposed to docker-compose.
"""

import os
import subprocess
import time
import urllib.request
from fastapi import FastAPI

app = FastAPI(
    title='Rowboat',
    version='1.0.0',
    description='Rowboat — Open-source AI coworker with knowledge graph'
)

NEXT_PROCESS = None
NEXT_PORT = 3000
WRAPPER_PORT = int(os.environ.get('ROWBOAT_WRAPPER_PORT', '8000'))


def _start_next():
    """Launch Next.js server as a background subprocess."""
    global NEXT_PROCESS
    try:
        NEXT_PROCESS = subprocess.Popen(
            ['node', '/app/server.js'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(5)
    except FileNotFoundError:
        pass


def _next_running() -> bool:
    """Check if Next.js server is responding."""
    try:
        req = urllib.request.Request(
            f'http://127.0.0.1:{NEXT_PORT}',
            method='HEAD'
        )
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False


@app.on_event('startup')
async def startup():
    _start_next()


@app.get('/healthz')
async def healthz():
    """Health check — verifies Next.js server is reachable."""
    running = _next_running()
    return {
        'status': 'ok' if running else 'starting',
        'next_running': running,
        'framework': 'Rowboat',
        'upstream': 'rowboatlabs/rowboat'
    }


@app.get('/info')
async def info():
    return {
        'name': 'Rowboat',
        'description': 'Open-source AI coworker that turns work into a knowledge graph and acts on it',
        'upstream': 'https://github.com/rowboatlabs/rowboat',
        'web_ui': f'http://localhost:{NEXT_PORT}',
        'features': [
            'Knowledge graph from email, calendar, and meeting notes',
            'Meeting prep from prior decisions and threads',
            'Email drafting grounded in history',
            'PDF slide generation from context',
            'Live notes that stay updated automatically',
            'Obsidian-compatible Markdown vault',
            'Bring your own model (local Ollama or hosted API)',
            'MCP tools integration'
        ],
        'ports': {
            'web_ui': NEXT_PORT,
            'mongo': 27017,
            'redis': 6379,
            'qdrant_http': 6333
        }
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=WRAPPER_PORT)
