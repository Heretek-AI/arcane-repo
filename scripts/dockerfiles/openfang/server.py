#!/usr/bin/env python3
"""OpenFang FastAPI wrapper — health-check gateway for the Rust binary.

Starts the upstream openfang binary (agent operating system / FL attack platform)
in a background subprocess and exposes a FastAPI /health endpoint.
"""

import os
import subprocess
import sys
import time

from fastapi import FastAPI

app = FastAPI(
    title='OpenFang',
    version='1.0.0',
    description='OpenFang — Federated Learning Attack Platform (RightNow-AI/openfang)'
)


def start_openfang() -> subprocess.Popen:
    """Start the openfang binary in background."""
    home = os.environ.get('OPENFANG_HOME', '/data')
    os.makedirs(home, exist_ok=True)

    print(f'[openfang] Starting openfang binary (OPENFANG_HOME={home})...')
    proc = subprocess.Popen(
        ['openfang', 'start'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env={**os.environ, 'OPENFANG_HOME': home}
    )
    # Give it a moment to bind the port
    time.sleep(2)
    return proc


_openfang_proc: subprocess.Popen | None = None


@app.on_event('startup')
async def startup():
    global _openfang_proc
    _openfang_proc = start_openfang()


@app.get('/health')
async def health():
    global _openfang_proc
    binary_ok = _openfang_proc is not None and _openfang_proc.poll() is None
    return {
        'status': 'ok' if binary_ok else 'degraded',
        'framework': 'OpenFang',
        'upstream': 'RightNow-AI/openfang',
        'binary_running': binary_ok
    }


@app.get('/info')
async def info():
    return {
        'name': 'OpenFang',
        'description': 'Open-source Agent Operating System — Federated Learning Attack Platform',
        'entrypoint': 'openfang start',
        'upstream': 'https://github.com/RightNow-AI/openfang',
        'stars': '1k+',
        'default_port': 4200
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('OPENFANG_PORT', '8000'))
    host = os.environ.get('OPENFANG_HOST', '0.0.0.0')

    print(f'[openfang] Starting FastAPI wrapper on {host}:{port}...')
    uvicorn.run(app, host=host, port=port, log_level='info')
