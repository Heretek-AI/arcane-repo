# S01: S01

**Goal:** Re-run all 13 previously fixed and runner-starved Docker build workflows on GitHub Actions and confirm each shows green/pass status, so the CI dashboard shows all builds passing.
**Demo:** All Docker image build workflows show green/pass status on GitHub Actions — including the previously broken builds and the runner-starved batch.

## Must-Haves

- All 13 Docker build workflows (5 fixed, 6 re-dispatched, Sunshine fixed) show green/pass status on GitHub Actions. Run IDs for each confirmed passing workflow are recorded.

## Proof Level

- This slice proves: contract — each workflow run on GitHub Actions is the ground truth; local gh CLI commands query the API for run status.

## Integration Closure

No downstream integration — this slice closes the CI loop entirely. Each workflow's final step (docker build + push) is the acceptance signal.

## Verification

- Runtime signals: GitHub Actions run status (success/failure/timed out). Each workflow run has a unique run ID logged as the verification artifact. Shallow clone failures surface in the workflow log as apt-get/npm/uv install errors. OOM failures appear as killed processes in the build step. Sunshine cmake failures surface as "CMake Error: Could not find..." in the configure step.

## Tasks

- [x] **T01: All 5 structurally fixed Docker workflows dispatched and verified passing on GitHub Actions** `est:45m`
  Re-run the 5 workflows that had structural fixes applied (MemVid, Streamer-Sales, TrendRadar, UNIT3D, MLflow) via gh workflow run dispatch and wait for each to complete with a green status.
  - Files: `.github/workflows/build-memvid.yml`, `.github/workflows/build-streamer-sales.yml`, `.github/workflows/build-trendradar.yml`, `.github/workflows/build-unit3d.yml`, `.github/workflows/build-mlflow.yml`
  - Verify: gh run list --workflow=build-<name>.yml --limit 1 --json conclusion returns 'success' for each of the 5 workflows, and run-log.md contains entries for all 5 with run IDs and passing status

- [x] **T02: Fixed gcc-13 toolchain and pinned Sunshine to v2024.1.1; cmake configure step still fails — error not visible in Actions log** `est:30m`
  Fix the Sunshine Docker build which is blocked on an upstream cmake interface change in v2025.924.154138.
  - Files: `scripts/dockerfiles/sunshine/Dockerfile`, `.github/workflows/build-sunshine.yml`
  - Verify: gh run list --workflow=build-sunshine.yml --limit 1 --json conclusion returns 'success', and run-log.md has a Sunshine entry with the pinned tag and run ID

- [x] **T03: Re-dispatch and verify 6 runner-starved workflows (AionUI, Harbor-LLM, KAG, WGCloud, Yuxi, CC Gateway)** `est:45m`
  Re-dispatch the 6 runner-starved workflows (AionUI, Harbor-LLM, KAG, WGCloud, Yuxi, CC Gateway) that failed due to GitHub Actions runner memory limits in a large concurrent batch.
  - Files: `.github/workflows/build-aionui.yml`, `.github/workflows/build-harbor-llm.yml`, `.github/workflows/build-kag.yml`, `.github/workflows/build-wgcloud.yml`, `.github/workflows/build-yuxi.yml`, `.github/workflows/build-cc-gateway.yml`
  - Verify: gh run list --workflow=build-<name>.yml --limit 1 --json conclusion returns 'success' for each of the 6 workflows, and run-log.md contains entries for all 6 with run IDs and passing status

- [x] **T04: Fix Sunshine cmake configure — diagnose locally or add build logging** `est:30m`
  The cmake configure error inside linux_build.sh is not visible in the Actions log artifact. Three dispatch cycles failed with exit 100 but the actual CMake Error lines are wrapped inside the upstream script. The blocker cannot be resolved via workflow dispatch alone.
  - Files: `scripts/dockerfiles/sunshine/Dockerfile`, `.github/workflows/build-sunshine.yml`, `.gsd/milestones/M001/slices/S01/run-log.md`
  - Verify: gh run list --workflow=build-sunshine.yml --limit 1 --json conclusion returns 'success', and run-log.md has Sunshine entry with passing run ID

## Files Likely Touched

- .github/workflows/build-memvid.yml
- .github/workflows/build-streamer-sales.yml
- .github/workflows/build-trendradar.yml
- .github/workflows/build-unit3d.yml
- .github/workflows/build-mlflow.yml
- scripts/dockerfiles/sunshine/Dockerfile
- .github/workflows/build-sunshine.yml
- .github/workflows/build-aionui.yml
- .github/workflows/build-harbor-llm.yml
- .github/workflows/build-kag.yml
- .github/workflows/build-wgcloud.yml
- .github/workflows/build-yuxi.yml
- .github/workflows/build-cc-gateway.yml
- .gsd/milestones/M001/slices/S01/run-log.md
