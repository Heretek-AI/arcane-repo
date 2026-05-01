#!/usr/bin/env python3
"""Sunshine FastAPI wrapper — starts LizardByte/Sunshine as a subprocess and exposes /health and /info endpoints."""

import os
import subprocess
import time
import urllib.request
from fastapi import FastAPI

app = FastAPI(
    title='Sunshine',
    version='1.0.0',
    description='Sunshine — Self-hosted game stream host for Moonlight. Stream games to any device.'
)

SUNSHINE_PROCESS = None


def _start_sunshine():
    """Launch Sunshine as a background subprocess."""
    global SUNSHINE_PROCESS
    try:
        SUNSHINE_PROCESS = subprocess.Popen(
            ['/usr/bin/sunshine'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Give it a few seconds to initialize
        time.sleep(3)
    except FileNotFoundError:
        pass


def _sunshine_running() -> bool:
    """Check if Sunshine's web UI is responding."""
    try:
        req = urllib.request.Request('http://127.0.0.1:47990', method='HEAD')
        urllib.request.urlopen(req, timeout=3)
        return True
    except Exception:
        return False


@app.on_event('startup')
async def startup():
    _start_sunshine()


@app.get('/health')
async def health():
    running = _sunshine_running()
    status = 'ok' if running else 'starting'
    return {
        'status': status,
        'sunshine_running': running,
        'framework': 'Sunshine',
        'upstream': 'LizardByte/Sunshine'
    }


@app.get('/info')
async def info():
    return {
        'name': 'Sunshine',
        'description': 'Self-hosted game stream host for Moonlight — stream games, desktop, and apps to any device',
        'upstream': 'https://github.com/LizardByte/Sunshine',
        'web_ui': 'http://localhost:47990',
        'moonlight_pairing': 'Open Moonlight client and pair via the Sunshine web UI PIN',
        'ports': {
            'web_ui': 47990,
            'rtsp': 48010,
            'video_tcp': '47984-47989',
            'video_udp': '47998-48000'
        }
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('SUNSHINE_WRAPPER_PORT', '47991'))
    uvicorn.run(app, host='0.0.0.0', port=port)
