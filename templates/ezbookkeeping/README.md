# ezBookkeeping — Upstream Project Removed

> **Non-serviceable:** The ezBookkeeping upstream repository (`ezbookkeeping/ezbookkeeping`) has been removed from GitHub and is no longer available. This template serves as a historical reference placeholder.

## What This Template Does

This template deploys a minimal FastAPI informational server on `python:3.12-slim` that documents the project's removal and suggests alternatives. It exposes `/health` for registry validation and `/guide` for alternative recommendations.

## Quick Start

```bash
cp .env.example .env
docker compose up -d
curl http://localhost:8000/health
```

## Why This Is Non-Serviceable

The upstream project no longer exists. No container image, source code, or documentation is available. The GitHub organization (`ezbookkeeping`) and repository (`ezbookkeeping/ezbookkeeping`) both return 404 errors.

## Alternatives

If you're looking for self-hosted personal finance or bookkeeping tools, consider:

| Tool | Description | Link |
|------|-------------|------|
| **Firefly III** | Self-hosted personal finance manager with double-entry bookkeeping | [firefly-iii.org](https://www.firefly-iii.org) |
| **Actual Budget** | Self-hosted budgeting app with envelope-based budgeting | [actualbudget.org](https://actualbudget.org) |
| **GnuCash** | Desktop double-entry accounting with SQL backend option | [gnucash.org](https://www.gnucash.org) |
| **Ledger** | Plain-text accounting with powerful CLI reporting | [ledger-cli.org](https://www.ledger-cli.org) |

## Health Check

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok","note":"placeholder — upstream repository removed"}`
