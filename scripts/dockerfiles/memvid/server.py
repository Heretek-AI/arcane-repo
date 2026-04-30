"""Memvid API server — wraps memvid-sdk as a REST API."""

import os
import json
import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.environ.get("MEMVID_LOG_LEVEL", "info").upper()),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("memvid-server")

MEMVID_DATA_DIR = Path(os.environ.get("MEMVID_DATA_DIR", "/app/data"))
MEMVID_DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_MEMVID_FILE = os.environ.get("MEMVID_FILE", "default.mv2")
EMBED_MODE = os.environ.get("MEMVID_EMBED_MODE", "local")

app = FastAPI(
    title="Memvid API",
    version="1.0.0",
    description=(
        "Memvid is a portable, single-file memory layer for AI agents. "
        "This server wraps the memvid-sdk Python library as a REST API, "
        "enabling document storage, semantic search, and knowledge retrieval."
    ),
)


class PutRequest(BaseModel):
    text: str
    title: Optional[str] = None
    uri: Optional[str] = None
    tags: Optional[dict[str, str]] = None


class SearchRequest(BaseModel):
    query: str
    top_k: int = 10
    snippet_chars: int = 200


class PutResponse(BaseModel):
    status: str
    memory_file: str
    title: Optional[str] = None
    document_count: int = 0


class SearchResult(BaseModel):
    title: Optional[str]
    text: str
    score: float


class SearchResponse(BaseModel):
    query: str
    top_k: int
    results: list[SearchResult]


class HealthResponse(BaseModel):
    status: str
    framework: str
    memory_file: str
    embed_mode: str
    data_dir: str
    memvid_version: str


# ── Cached memvid instance ────────────────────────────────────────
_memvid = None


def get_memvid():
    """Get or create the Memvid singleton instance."""
    global _memvid
    if _memvid is None:
        try:
            from memvid_sdk import Memvid

            memory_path = MEMVID_DATA_DIR / DEFAULT_MEMVID_FILE
            if memory_path.exists():
                _memvid = Memvid.open(str(memory_path))
                logger.info("Opened existing memory file: %s", memory_path)
            else:
                _memvid = Memvid.create(str(memory_path))
                logger.info("Created new memory file: %s", memory_path)
        except ImportError as exc:
            logger.warning("memvid-sdk not available: %s", exc)
            return None
        except Exception as exc:
            logger.warning("Failed to initialize memvid: %s", exc)
            return None
    return _memvid


def get_memvid_version() -> str:
    """Get the installed memvid-sdk version."""
    try:
        import importlib.metadata

        return importlib.metadata.version("memvid-sdk")
    except Exception:
        return "unknown"


# ── Routes ────────────────────────────────────────────────────────


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint — returns server and memory status."""
    m = get_memvid()
    return HealthResponse(
        status="ok" if m is not None else "degraded",
        framework="Memvid",
        memory_file=DEFAULT_MEMVID_FILE,
        embed_mode=EMBED_MODE,
        data_dir=str(MEMVID_DATA_DIR),
        memvid_version=get_memvid_version(),
    )


@app.put("/memory", response_model=PutResponse)
async def put_memory(req: PutRequest):
    """Store a document in memory."""
    m = get_memvid()
    if m is None:
        raise HTTPException(503, "memvid-sdk not available (pip install memvid-sdk[full])")

    try:
        opts = {}
        if req.title:
            opts["title"] = req.title
        if req.uri:
            opts["uri"] = req.uri
        if req.tags:
            for k, v in req.tags.items():
                opts[f"tag.{k}"] = v

        if opts:
            from memvid_sdk import PutOptions

            put_opts = PutOptions.builder()
            for key, value in opts.items():
                if key == "title":
                    put_opts.title(value)
                elif key == "uri":
                    put_opts.uri(value)
                elif key.startswith("tag."):
                    put_opts.tag(key[4:], value)
            m.put_bytes_with_options(req.text.encode("utf-8"), put_opts.build())
        else:
            m.put_bytes(req.text.encode("utf-8"))

        m.commit()
        logger.info("Stored document: title=%s uri=%s", req.title, req.uri)
        return PutResponse(
            status="ok", memory_file=DEFAULT_MEMVID_FILE, title=req.title, document_count=1
        )
    except Exception as exc:
        logger.error("Failed to store document: %s", exc)
        raise HTTPException(500, f"Failed to store document: {exc}")


@app.post("/search", response_model=SearchResponse)
async def search_memory(req: SearchRequest):
    """Search memory for documents matching the query."""
    m = get_memvid()
    if m is None:
        raise HTTPException(503, "memvid-sdk not available (pip install memvid-sdk[full])")

    try:
        from memvid_sdk import SearchRequest as SDKSearchRequest

        sdk_req = SDKSearchRequest(
            query=req.query,
            top_k=req.top_k,
            snippet_chars=req.snippet_chars,
        )
        response = m.search(sdk_req)

        results = [
            SearchResult(
                title=hit.title if hasattr(hit, "title") else None,
                text=getattr(hit, "text", ""),
                score=getattr(hit, "score", 0.0),
            )
            for hit in response.hits
        ]

        logger.info("Search query='%s' returned %d results", req.query, len(results))
        return SearchResponse(query=req.query, top_k=req.top_k, results=results)
    except Exception as exc:
        logger.error("Search failed: %s", exc)
        raise HTTPException(500, f"Search failed: {exc}")


@app.post("/reset")
async def reset_memory():
    """Delete and recreate the memory file."""
    m = get_memvid()
    if m is None:
        raise HTTPException(503, "memvid-sdk not available")
    try:
        from memvid_sdk import Memvid

        memory_path = MEMVID_DATA_DIR / DEFAULT_MEMVID_FILE
        if memory_path.exists():
            memory_path.unlink()
        _memvid = Memvid.create(str(memory_path))
        logger.info("Memory file reset: %s", memory_path)
        return {"status": "ok", "memory_file": DEFAULT_MEMVID_FILE}
    except Exception as exc:
        logger.error("Reset failed: %s", exc)
        raise HTTPException(500, f"Reset failed: {exc}")


# ── Main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("MEMVID_PORT", "8000"))
    logger.info("Starting Memvid API server on port %d (embed_mode=%s)", port, EMBED_MODE)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=os.environ.get("MEMVID_LOG_LEVEL", "info"))
