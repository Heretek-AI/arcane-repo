#!/usr/bin/env python3
"""cc-gateway FastAPI wrapper — exposes the AI API identity gateway status and health.

cc-gateway is a TypeScript/Node.js project — this server.py provides a health endpoint
and attempts to start the upstream Node server as a subprocess. For production use,
the Node server itself is the primary runtime.
"""

import os
import subprocess
import sys
from fastapi import FastAPI

app = FastAPI(
    title='cc-gateway',
    version='1.0.0',
    description='cc-gateway — AI API identity gateway, privacy-preserving reverse proxy for LLM APIs (motiful/cc-gateway, 2.7k★)'
)


@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'cc-gateway', 'upstream': 'motiful/cc-gateway'}


@app.get('/info')
async def info():
    return {
        'name': 'cc-gateway',
        'description': 'Privacy-preserving AI API reverse proxy with identity forwarding',
        'upstream': 'https://github.com/motiful/cc-gateway',
        'runtime': 'Node.js / TypeScript',
        'stars': '2.7k+'
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('CC_GATEWAY_PORT', '8000'))

    # Attempt to start the upstream Node server alongside
    server_js = os.path.join('/app', 'server.js')
    if os.path.isfile(server_js):
        subprocess.Popen(
            ['node', server_js, '--port', os.environ.get('CC_GATEWAY_PORT', '8000')],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    uvicorn.run(app, host='0.0.0.0', port=port)
