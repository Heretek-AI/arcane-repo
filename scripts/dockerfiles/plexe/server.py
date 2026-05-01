#!/usr/bin/env python3
"""Plexe FastAPI wrapper — exposes plexe-ai/plexe as a REST API for building ML models from natural language prompts."""

import os
import subprocess
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title='Plexe',
    version='1.0.0',
    description='Plexe — Build machine learning models from natural language. Describe what you want, provide a dataset, and AI agents build a fully functional model.'
)


class BuildRequest(BaseModel):
    intent: str
    dataset_path: str = '/data/dataset.parquet'
    max_iterations: int = 5
    model_types: list[str] | None = None


class BuildResponse(BaseModel):
    status: str
    work_dir: str
    output: str


@app.get('/health')
async def health():
    """Health check — verify Plexe is installed and importable."""
    try:
        import plexe  # noqa: F401
        return {
            'status': 'ok',
            'framework': 'Plexe',
            'upstream': 'plexe-ai/plexe',
            'version': 'v1.4.4'
        }
    except ImportError:
        return {
            'status': 'degraded',
            'framework': 'Plexe',
            'error': 'plexe module not importable'
        }


@app.get('/info')
async def info():
    return {
        'name': 'Plexe',
        'description': 'Build ML models from natural language — 14 specialized AI agents across a 6-phase workflow',
        'upstream': 'https://github.com/plexe-ai/plexe',
        'install': 'pip install plexe',
        'requires': ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY'],
        'frameworks': ['XGBoost', 'CatBoost', 'LightGBM', 'Keras', 'PyTorch'],
        'cli': 'python -m plexe.main --train-dataset-uri /data/dataset.parquet --intent "predict ..." --max-iterations 5',
        'volumes': {
            '/data': 'input datasets (Parquet, CSV, ORC, Avro)',
            '/workdir': 'model output + evaluation reports'
        }
    }


@app.post('/build', response_model=BuildResponse)
async def build_model(request: BuildRequest):
    """Build an ML model from a natural language intent."""
    work_dir = f'/workdir/{request.intent.replace(" ", "_")[:60]}'
    os.makedirs(work_dir, exist_ok=True)

    cmd = [
        sys.executable, '-m', 'plexe.main',
        '--train-dataset-uri', request.dataset_path,
        '--intent', request.intent,
        '--max-iterations', str(request.max_iterations),
        '--work-dir', work_dir,
    ]

    if request.model_types:
        cmd += ['--allowed-model-types'] + request.model_types

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,  # ML builds can take a while
            cwd='/app/plexe-src'
        )
        return BuildResponse(
            status='success' if result.returncode == 0 else 'failed',
            work_dir=work_dir,
            output=(result.stdout + '\n' + result.stderr)[-8000:]
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=504,
            detail='Model build timed out after 3600s — try reducing max_iterations'
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail='plexe CLI not found — is the package installed?'
        )


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PLEXE_PORT', '8000'))
    uvicorn.run(app, host='0.0.0.0', port=port)
