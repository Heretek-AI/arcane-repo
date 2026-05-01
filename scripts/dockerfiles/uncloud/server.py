#!/usr/bin/env python3
"""Uncloud FastAPI wrapper — exposes the container orchestration daemon as a REST API."""

import os
import subprocess
import sys
from fastapi import FastAPI

app = FastAPI(
    title='Uncloud',
    version='1.0.0',
    description='Uncloud — Lightweight container orchestration with WireGuard mesh (psviderski/uncloud)'
)


@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'Uncloud', 'upstream': 'psviderski/uncloud'}


@app.get('/info')
async def info():
    return {
        'name': 'Uncloud',
        'description': 'Lightweight container orchestration platform deploying apps across Docker hosts with WireGuard mesh networking',
        'binaries': ['uncloudd', 'corrosion'],
        'upstream': 'https://github.com/psviderski/uncloud',
        'stars': '5.1k+'
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('UNCLOUD_PORT', '8000'))

    # Start uncloudd daemon in background
    uncloudd_binary = '/usr/local/bin/uncloudd'
    if os.path.isfile(uncloudd_binary):
        subprocess.Popen(
            [uncloudd_binary],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    uvicorn.run(app, host='0.0.0.0', port=port)
