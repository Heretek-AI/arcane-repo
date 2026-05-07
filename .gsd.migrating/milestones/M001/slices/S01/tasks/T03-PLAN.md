---
estimated_steps: 8
estimated_files: 6
skills_used: []
---

# T03: Re-dispatch and verify 6 runner-starved workflows (AionUI, Harbor-LLM, KAG, WGCloud, Yuxi, CC Gateway)

Re-dispatch the 6 runner-starved workflows (AionUI, Harbor-LLM, KAG, WGCloud, Yuxi, CC Gateway) that failed due to GitHub Actions runner memory limits in a large concurrent batch.

Steps:
1. Dispatch each workflow sequentially (not in parallel) to avoid runner memory contention: gh workflow run build-<name>.yml --ref main
2. After each dispatch, wait up to 10 minutes for the run to start and make measurable progress (runner status = 'queued' or 'in_progress')
3. Once a run is in_progress, move to the next workflow
4. After all 6 are dispatched and in-progress, wait for completion using polling
5. For each workflow, record run ID and final status in run-log.md
6. If any workflow fails with an OOM error again, note it as needing potential runner-size upgrade and document the failure pattern

## Inputs

- None specified.

## Expected Output

- `run-log.md`

## Verification

gh run list --workflow=build-<name>.yml --limit 1 --json conclusion returns 'success' for each of the 6 workflows, and run-log.md contains entries for all 6 with run IDs and passing status

## Observability Impact

OOM failures appear as 'Process killed' or 'No space left on device' in gh run view <id> --log. Sequential dispatch avoids runner memory contention.
