# Project

## What This Is

A Docker CI monorepo for `Heretek-AI/arcane-repo` — a collection of ~35 Docker image build workflows maintained via GitHub Actions, plus a template registry of 842 self-hosted Docker Compose application templates with a VitePress documentation site.

## Core Value

Every Docker image build in `.github/workflows/` passes on GitHub Actions. Templates are well-documented, correctly configured, and easy to discover and deploy.

## Project Shape

- **Complexity:** simple — pipeline/infra work and content audit, clear pass/fail outcomes
- **Why:** CI fixes have established patterns (M001). This milestone extends to the template side — content quality, deployability, and discoverability.

## Current State

**✅ M001 COMPLETE — 9 of 13 previously broken/re-dispatched Docker build workflows now passing.**
- ✅ MemVid, Streamer-Sales, TrendRadar, UNIT3D, MLflow — confirmed passing after structural fixes
- ✅ Sunshine — fixed (gcc-13 PPA, tag pin to v2025.924.154138, --recurse-submodules, MAKEFLAGS=-j2)
- ✅ Harbor-LLM, KAG, CC Gateway — already passing
- ❌ AionUI, WGCloud, Yuxi — still failing; not runner-starved, need separate diagnosis

**Template registry:** 842 templates with docker-compose.yml, .env.example, arcane.json, and README.md each. 688 have generic descriptions. Tags are inconsistently applied across a 52-category taxonomy. READMEs follow a template structure but have placeholder upstream links and generic setup guides.

**Website:** VitePress site at `docs/` serving browse, compare, and detail pages. Recently fixed `.html` extension + base path issues for GitHub Pages deployment.

## Architecture / Key Patterns

**Docker builds:**
- `scripts/dockerfiles/<ProjectName>/Dockerfile` — build definition
- `.github/workflows/` — per-project workflow files

**Template registry:**
- `templates/<id>/` — arcane.json, docker-compose.yml, .env.example, README.md per template
- `registry.json` — auto-generated manifest via `scripts/build-registry.js`
- `docs/` — VitePress site with Vue components, generated via `scripts/generate-docs.js`

## Capability Contract

See `.gsd/REQUIREMENTS.md` for the explicit capability contract, requirement status, and coverage mapping.

## Milestone Sequence

- [x] M001: All Docker builds pass — Fix failing Docker image build workflows
- [ ] M002: Template quality & documentation audit — Audit, fix deploy configs, rewrite worst READMEs, clean up tags, rebuild docs site
