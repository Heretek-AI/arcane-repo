#!/usr/bin/env python3
"""Cog FastAPI wrapper — exposes replicate/cog CLI as a REST API for ML model packaging and prediction."""

import os
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title='Cog',
    version='1.0.0',
    description='Cog — ML container packaging tool (replicate/cog). Build and run ML models in containers.'
)


class PredictRequest(BaseModel):
    model_path: str = '/app/model'
    input_data: dict = {}


class BuildRequest(BaseModel):
    model_path: str = '/app/model'
    image_name: str = 'cog-model'


@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'Cog', 'upstream': 'replicate/cog'}


@app.get('/info')
async def info():
    return {
        'name': 'Cog',
        'description': 'Containerize ML models for reproducible prediction — cog build, cog predict',
        'upstream': 'https://github.com/replicate/cog',
        'commands': ['cog build', 'cog predict', 'cog push']
    }


@app.post('/predict')
async def predict(request: PredictRequest):
    """Run `cog predict` against a model."""
    try:
        result = subprocess.run(
            ['cog', 'predict', '-i', str(request.input_data)],
            cwd=request.model_path,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f'cog predict failed: {result.stderr.strip()}'
            )
        return {
            'status': 'success',
            'output': result.stdout.strip(),
            'model_path': request.model_path
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail='cog predict timed out after 300s')
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail='cog CLI not found — is cog installed?')


@app.post('/build')
async def build(request: BuildRequest):
    """Run `cog build` to containerize a model."""
    try:
        result = subprocess.run(
            ['cog', 'build', '-t', request.image_name],
            cwd=request.model_path,
            capture_output=True,
            text=True,
            timeout=600
        )
        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f'cog build failed: {result.stderr.strip()}'
            )
        return {
            'status': 'built',
            'image': request.image_name,
            'output': result.stdout.strip()
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail='cog build timed out after 600s')
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail='cog CLI not found — is cog installed?')


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('COG_PORT', '8000'))
    uvicorn.run(app, host='0.0.0.0', port=port)
