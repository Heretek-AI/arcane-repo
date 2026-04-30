#!/usr/bin/env python3
"""Clawith FastAPI wrapper — serves backend API + frontend static assets.

Wraps the upstream dataelement/Clawith backend (FastAPI on app.main:app)
and frontend (React/Vite SPA) in a single container.
"""

import os
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# ── Alembic migrations ──────────────────────────────────────────────────

def run_migrations() -> None:
    """Run alembic upgrade head to apply all outstanding DB migrations."""
    print('[clawith] Running alembic migrations...')
    result = subprocess.run(
        [sys.executable, '-m', 'alembic', 'upgrade', 'head'],
        capture_output=True,
        text=True,
        cwd='/app'
    )
    if result.returncode != 0:
        print(f'[clawith] WARNING: Alembic migration failed (exit {result.returncode})')
        print(result.stderr[:500])
        print('[clawith] Continuing startup despite migration failure...')
    else:
        print('[clawith] Alembic migrations completed successfully.')
        print(result.stdout[-300:] if len(result.stdout) > 300 else result.stdout)


# ── Build combined FastAPI app ──────────────────────────────────────────

def create_app() -> FastAPI:
    """Create FastAPI app that wraps upstream backend + serves static frontend."""

    # Import the upstream FastAPI app
    from app.main import app as upstream_app

    # Serve frontend static assets
    static_dir = Path('/app/static')
    if static_dir.is_dir():
        upstream_app.mount('/static', StaticFiles(directory=str(static_dir)), name='static')

        # SPA fallback: serve index.html for any non-API route
        @upstream_app.middleware('http')
        async def spa_fallback(request, call_next):
            from fastapi.responses import Response
            from starlette.types import Scope
            # Only intercept GET requests that aren't /api/* or /static/*
            if request.method == 'GET':
                scope: Scope = request.scope
                path = scope.get('path', '')
                if not path.startswith('/api/') and not path.startswith('/static/'):
                    # Try to serve; if 404, return index.html for SPA routing
                    try:
                        response = await call_next(request)
                        if response.status_code == 404:
                            index_path = static_dir / 'index.html'
                            if index_path.exists():
                                return FileResponse(str(index_path))
                        return response
                    except Exception:
                        index_path = static_dir / 'index.html'
                        if index_path.exists():
                            return FileResponse(str(index_path))
                        raise
            return await call_next(request)

    return upstream_app


# ── Entrypoint ──────────────────────────────────────────────────────────

if __name__ == '__main__':
    import uvicorn

    run_migrations()

    app = create_app()
    port = int(os.environ.get('CLAWITH_PORT', '8000'))
    host = os.environ.get('CLAWITH_HOST', '0.0.0.0')

    print(f'[clawith] Starting uvicorn on {host}:{port}...')
    uvicorn.run(app, host=host, port=port, log_level='info')
