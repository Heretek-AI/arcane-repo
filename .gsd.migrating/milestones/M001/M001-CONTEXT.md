# M001: Fix All Failing Docker Builds

**Gathered:** 2026-01-20
**Status:** Ready for planning

## Project Description

Fix all failing Docker image build workflows in the `Heretek-AI/arcane-repo` GitHub Actions CI. 32 of 37 builds pass. Five need structural fixes; two more need re-dispatch.

## Why This Milestone

The CI is currently broken — five workflows are red. All of them have known root causes identified and fixes committed. This milestone completes the fix cycle by confirming all builds are green, unblocking Sunshine (which needs upstream investigation), and re-dispatching runner-starved builds.

## User-Visible Outcome

When this milestone is complete, the user can see all Docker build workflows passing on GitHub Actions.

## Entry point / environment

- Entry point: GitHub Actions — `.github/workflows/` run
- Environment: GitHub-hosted runners (ubuntu-latest, possibly large/ARM64)
- Live dependencies involved: GitHub API (dispatch/rerun workflows)

## Completion Class

- Contract complete means: All Docker images build without errors
- Integration complete means: Workflow dispatch runs show green status for all projects
- Operational complete means: N/A — no live system, just CI

## Final Integrated Acceptance

To call this milestone complete, we must prove:

- All 5 previously fixed builds (MemVid, Streamer-Sales, TrendRadar, UNIT3D, MLflow) show green status on GitHub Actions
- Sunshine cmake issue is resolved (upstream tag pinning or script patch applied, build passes)
- Runner-starved batch (AionUI, Harbor-LLM, KAG, WGCloud, Yuxi, CC Gateway) re-dispatched and passing

## Architectural Decisions

No architectural decisions — infrastructure/Pipeline work.

## Error Handling Strategy

- Shallow clone fails without `package-lock.json` → fallback to `npm install`
- Python package extra conflicts → pin exact extras needed, remove conflicting extras
- COPY path mismatches → use lowercase directory names matching the actual filesystem
- Runner OOM → reduce build parallelism or dispatch smaller batches
- Upstream cmake interface changes → pin to known-working upstream tag

## Risks and Unknowns

- **Sunshine upstream compatibility** — cmake interface changed in v2025.924.154138; pinning to an older tag may work but version compatibility is unknown
- **UNIT3D OOM on frontend-builder** — if the `npm install && npm run build` step exhausts the runner memory again, may need to skip frontend build or reduce Vite parallelism
- **Runner starvation** — re-dispatching 6 workflows in parallel may hit the same memory limit; may need to dispatch 1-2 at a time

## Existing Codebase / Prior Art

- `.github/workflows/` — Docker build workflow definitions
- `scripts/dockerfiles/` — per-project Dockerfile definitions
- Prior successful builds (32 passing) provide the template for what works

## Scope

### In Scope

- Confirm all 5 applied fixes are green (re-run and verify)
- Fix Sunshine cmake compatibility (upstream tag pin or script patch)
- Re-dispatch and verify runner-starved batch (AionUI, Harbor-LLM, KAG, WGCloud, Yuxi, CC Gateway)

### Out of Scope / Non-Goals

- Building new Docker images (only fixing existing ones)
- Improving build caching or layer optimization (deferred to M002)
- Adding new workflows

## Technical Constraints

- Shallow clones (`--depth 1`) for all upstream repos
- Use `uv` for Python packages, `npm` for Node packages
- GitHub Actions on `ubuntu-latest` (standard and large runners available)

## Integration Points

- GitHub Actions — workflow dispatch, run status polling
- Docker Hub / GHCR — image push targets
- Upstream open-source projects — cloned at `--depth 1`

## Testing Requirements

Run each workflow via `gh workflow run` or GitHub UI dispatch and confirm green status.

## Acceptance Criteria

For each workflow:
- GitHub Actions run completes with exit 0
- Final step (push or verify) succeeds
- No red X indicators in the Actions UI

## Open Questions

- What upstream tag should Sunshine pin to? Need to test `v2024.924.154138` or similar to find a working version.
- Should UNIT3D skip the frontend build entirely if OOM persists?
