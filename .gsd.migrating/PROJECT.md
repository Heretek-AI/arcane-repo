# Project

## What This Is

A Docker CI monorepo for `Heretek-AI/arcane-repo` — a collection of ~35 Docker image build workflows maintained via GitHub Actions. Each workflow builds a Docker image from an upstream open-source project and pushes it to a container registry.

## Core Value

Every Docker image build in `.github/workflows/` passes on GitHub Actions. Images are built reliably on every push to `main` and on-demand via workflow dispatch.

## Project Shape

- **Complexity:** simple — pipeline/infra work with clear pass/fail outcomes
- **Why:** Well-defined scope (fix failing builds), established patterns (same Dockerfile + workflow structure repeated), known unknowns (upstream version changes, runner memory limits)

## Current State

32 of 37 Docker builds pass. Five are broken:
- **MemVid, Streamer-Sales, TrendRadar, UNIT3D, MLflow** — fixes applied, awaiting re-run confirmation
- **Sunshine** — blocked on upstream cmake interface change
- **AionUI, Harbor-LLM, KAG, WGCloud, Yuxi, CC Gateway** — runner-starved in a large concurrent batch; need re-dispatch

Dockerfile conventions established: shallow upstream clones (`--depth 1`), `uv` for Python, `npm` for Node, Debian-slim base images, platform-specific build arguments.

## Architecture / Key Patterns

Each project has:
- `scripts/dockerfiles/<ProjectName>/Dockerfile` — the build definition
- `.github/workflows/` — one workflow file per project or group of projects

Pattern: clone upstream at shallow depth → apt dependencies → uv/npm install → entrypoint/verify → push image.

## Capability Contract

See `.gsd/REQUIREMENTS.md` for the explicit capability contract, requirement status, and coverage mapping.

## Milestone Sequence

- [ ] M001: All Docker builds pass — Fix failing Docker image build workflows for MemVid, Streamer-Sales, TrendRadar, UNIT3D, MLflow (runner-starved), Sunshine (cmake), and re-dispatch the runner-starved batch
- [ ] M002: Docker build hardening — Improve build caching, layer optimization, and upstream version pinning for long-term stability
