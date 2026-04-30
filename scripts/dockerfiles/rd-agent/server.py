#!/usr/bin/env python3
"""RD-Agent FastAPI wrapper — exposes the CLI tool as a REST API."""

import os
import subprocess
import tempfile
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title='RD-Agent',
    version='1.0.0',
    description='Automated research & development agent — CLI tool with REST wrapper'
)


class RunRequest(BaseModel):
    prompt: str
    workspace: str = '/workspace'


@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'RD-Agent'}


@app.get('/version')
async def version():
    try:
        result = subprocess.run(
            ['rdagent', '--version'],
            capture_output=True, text=True, timeout=15
        )
        return {'version': result.stdout.strip() or 'unknown'}
    except Exception as e:
        return {'version': 'unknown', 'error': str(e)}


@app.post('/run')
async def run(request: RunRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail='prompt cannot be empty')

    workspace_path = Path(request.workspace)
    workspace_path.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            ['rdagent', request.prompt],
            capture_output=True, text=True, timeout=300,
            cwd=request.workspace
        )
        return {
            'status': 'completed' if result.returncode == 0 else 'error',
            'exit_code': result.returncode,
            'stdout': result.stdout[-2000:] if result.stdout else '',
            'stderr': result.stderr[-2000:] if result.stderr else ''
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail='RD-Agent execution timed out (300s)')
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail='rdagent CLI not found — check installation')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/evaluate')
async def evaluate(request: RunRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail='prompt cannot be empty')

    workspace_path = Path(request.workspace)
    workspace_path.mkdir(parents=True, exist_ok=True)

    try:
        result = subprocess.run(
            ['rdagent', 'evaluate', request.prompt],
            capture_output=True, text=True, timeout=300,
            cwd=request.workspace
        )
        return {
            'status': 'completed' if result.returncode == 0 else 'error',
            'exit_code': result.returncode,
            'stdout': result.stdout[-2000:] if result.stdout else '',
            'stderr': result.stderr[-2000:] if result.stderr else ''
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail='RD-Agent evaluation timed out (300s)')


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('RDAGENT_PORT', '8000'))
    uvicorn.run(app, host='0.0.0.0', port=port)
