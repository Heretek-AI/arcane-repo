---
estimated_steps: 6
estimated_files: 5
skills_used: []
---

# T01: All 5 structurally fixed Docker workflows dispatched and verified passing on GitHub Actions

Re-run the 5 workflows that had structural fixes applied (MemVid, Streamer-Sales, TrendRadar, UNIT3D, MLflow) via gh workflow run dispatch and wait for each to complete with a green status.

Steps:
1. For each of the 5 workflows, dispatch via: gh workflow run build-<name>.yml --ref main
2. Poll run status every 30s using gh run list --workflow=build-<name>.yml --limit 1 --json status,conclusion,name until conclusion is 'success' or 'failure'
3. Record the run ID (from gh run list --json id) and status for each workflow in a tracking file at run-log.md
4. If any workflow fails, re-examine the failure from gh run view <id> --log and attempt one additional fix+re-dispatch cycle before flagging

## Inputs

- None specified.

## Expected Output

- `run-log.md`

## Verification

gh run list --workflow=build-<name>.yml --limit 1 --json conclusion returns 'success' for each of the 5 workflows, and run-log.md contains entries for all 5 with run IDs and passing status

## Observability Impact

gh run list shows status/conclusion; gh run view <id> --log shows full build output including OOM kills and install errors
