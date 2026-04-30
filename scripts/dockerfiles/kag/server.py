#!/usr/bin/env python3
"""KAG FastAPI wrapper — exposes the knowledge-augmented generation framework as a REST API."""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title='KAG',
    version='1.0.0',
    description='Knowledge-augmented generation framework (OpenSPG/KAG) — build and query knowledge graphs'
)


class QueryRequest(BaseModel):
    query: str
    knowledge_base: str = 'default'


class BuildRequest(BaseModel):
    source: str
    knowledge_base: str = 'default'
    source_type: str = 'text'


@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'KAG', 'open_spg_version': '0.1.0'}


@app.post('/build')
async def build_kb(request: BuildRequest):
    try:
        # KAG uses OpenSPG knowledge base construction pipeline
        from kag.builder import KAGBuilder
        builder = KAGBuilder(request.knowledge_base)
        await builder.build(source=request.source, source_type=request.source_type)
        return {
            'status': 'built',
            'knowledge_base': request.knowledge_base,
            'source_type': request.source_type
        }
    except ImportError:
        raise HTTPException(status_code=500, detail='KAG builder module not available')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/query')
async def query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail='query cannot be empty')

    try:
        from kag.solver import KAGSolver
        solver = KAGSolver(request.knowledge_base)
        answer = await solver.query(request.query)
        return {'query': request.query, 'answer': str(answer)}
    except ImportError:
        raise HTTPException(status_code=500, detail='KAG solver module not available')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('KAG_PORT', '8000'))
    uvicorn.run(app, host='0.0.0.0', port=port)
