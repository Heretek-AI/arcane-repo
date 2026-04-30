#!/usr/bin/env python3
"""OM1 FastAPI wrapper — health-check + info gateway for the multi-modal AI runtime.

OM1 (OpenMind/OM1) is a modular AI runtime for robots. Full functionality requires
hardware devices (cameras, microphones, speakers) and PulseAudio. This wrapper
provides API observability in headless/development mode.
"""

import os
from fastapi import FastAPI

app = FastAPI(
    title='OM1',
    version='1.0.0',
    description='OM1 — Modular AI Runtime for Robots (OpenMind/OM1) — Headless Mode'
)


@app.get('/health')
async def health():
    headless = os.environ.get('OM1_HEADLESS', 'true').lower() == 'true'
    return {
        'status': 'ok',
        'framework': 'OM1',
        'upstream': 'OpenMind/OM1',
        'mode': 'headless' if headless else 'hardware',
        'warning': 'Hardware devices (cameras, mics, speakers) not available in container mode' if headless else None
    }


@app.get('/info')
async def info():
    return {
        'name': 'OM1',
        'description': 'Modular AI Runtime for Robots — multi-modal agent with vision, audio, and speech',
        'entrypoint': 'python src/run.py',
        'upstream': 'https://github.com/OpenMind/OM1',
        'stars': '1.5k+',
        'hardware_requirements': {
            'audio_output': 'PulseAudio speaker (pactl)',
            'audio_input': 'microphone (ALSA/PulseAudio)',
            'video': 'camera (/dev/video0 via V4L2)',
            'container_support': 'Limited — requires device passthrough (--device /dev/video0, --device /dev/snd, -v /run/user/1000/pulse:/run/user/1000/pulse)'
        }
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('OM1_PORT', '8000'))
    host = os.environ.get('OM1_HOST', '0.0.0.0')

    print(f'[om1] Starting FastAPI headless wrapper on {host}:{port}...')
    print('[om1] NOTE: Full OM1 functionality requires hardware devices. See README for details.')
    uvicorn.run(app, host=host, port=port, log_level='info')
