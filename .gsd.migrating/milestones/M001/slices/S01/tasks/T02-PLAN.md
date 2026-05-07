---
estimated_steps: 9
estimated_files: 2
skills_used: []
---

# T02: Fixed gcc-13 toolchain and pinned Sunshine to v2024.1.1; cmake configure step still fails — error not visible in Actions log

Fix the Sunshine Docker build which is blocked on an upstream cmake interface change in v2025.924.154138.

Steps:
1. Inspect scripts/dockerfiles/sunshine/Dockerfile and identify the cmake configure step that fails
2. Identify the last known-working upstream git tag via upstream repo history (e.g. v2024.x series)
3. Update the Dockerfile to pin the upstream clone to a working tag: add --branch <working-tag> --depth 1 to the git clone command
4. Re-run the workflow: gh workflow run build-sunshine.yml --ref main
5. Poll status and verify success
6. If pinning an older tag does not work, try disabling the cmake feature flag causing the failure (check the upstream release notes for breaking changes)
7. Record the chosen tag and outcome in run-log.md

## Inputs

- None specified.

## Expected Output

- `run-log.md`
- `scripts/dockerfiles/sunshine/Dockerfile`

## Verification

gh run list --workflow=build-sunshine.yml --limit 1 --json conclusion returns 'success', and run-log.md has a Sunshine entry with the pinned tag and run ID

## Observability Impact

cmake configure errors appear in build logs as 'CMake Error: Could not find...' — visible via gh run view <id> --log
