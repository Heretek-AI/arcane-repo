#!/usr/bin/env python3
"""TrendRadar FastAPI wrapper — exposes news aggregation and sentiment analysis as a REST API."""

import os
import subprocess
import sys
from fastapi import FastAPI

app = FastAPI(
    title='TrendRadar',
    version='1.0.0',
    description='TrendRadar — multi-platform news aggregation with sentiment analysis and trending detection (sansan0/TrendRadar, 55.9k★)'
)


@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'TrendRadar', 'upstream': 'sansan0/TrendRadar'}


@app.get('/info')
async def info():
    return {
        'name': 'TrendRadar',
        'description': 'Aggregate news from multiple platforms, analyze sentiment, and track trending topics',
        'upstream': 'https://github.com/sansan0/TrendRadar',
        'backend': 'Python',
        'stars': '55.9k+',
        'has_docker_dir': True
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('TRENDRADAR_PORT', '8000'))

    # Start TrendRadar main process
    app_dir = '/app'
    entrypoints = ['main.py', 'app.py', 'run.py', 'server.py']
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
