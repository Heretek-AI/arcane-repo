---
id: T04
parent: S01
milestone: M001
key_files:
  - scripts/dockerfiles/sunshine/Dockerfile
  - .gsd/milestones/M001/slices/S01/run-log.md
key_decisions:
  - Tag v2024.1.1 does not exist on LizardByte/Sunshine — switched to v2025.924.154138 (latest available)
  - git clone --depth 1 does not fetch submodules — added --recurse-submodules to fix missing third-party deps
  - tee /tmp/build.log is the only viable diagnostic path when local Docker is unavailable and shell-pipefail wraps cmake output
duration: 
verification_result: passed
completed_at: 2026-05-07T13:18:33.113Z
blocker_discovered: false
---

# T04: Sunshine cmake configure fixed; workflow now passes

**Sunshine cmake configure fixed; workflow now passes**

## What Happened

T04 diagnosed and fixed the Sunshine cmake configure failure that had been masked by the shell-pipefail wrapper across three prior dispatch cycles.

**Diagnosis method:** Added `2>&1 | tee /tmp/build.log` to the Dockerfile `RUN` command and a PIPESTATUS exit-code check. This surfaced the actual cmake errors in the GitHub Actions log for the first time — without local Docker access on Windows, this was the only available diagnostic path.

**Two root causes found:**
1. Tag `v2024.1.1` does not exist on LizardByte/Sunshine (all tags are `v2025.x.x`). `git clone --depth 1 --branch v2024.1.1` fails with `fatal: Remote branch v2024.1.1 not found`.
2. Missing third-party git submodules (`moonlight-common-c/enet`, `Simple-Web-Server`, `libdisplaydevice`) — `add_subdirectory given source "third-party/moonlight-common-c/enet" which is not an existing directory`. The `--depth 1` clone does not fetch submodule content.

**Fix applied:** `git clone --depth 1 --recurse-submodules --branch v2025.924.154138 https://github.com/LizardByte/Sunshine.git .`

**Workflow 25497271164: SUCCESS** — Sunshine now builds and pushes to GHCR.

**T03 leftover failures (AionUI, WGCloud, Yuxi):** These three were re-dispatched in T03 and still fail. Their failures are NOT runner-starved (Harbor-LLM, KAG, CC Gateway passed with the same timing). They need deeper build-diagnosis beyond the scope of this task. T03 already flagged this finding.

## Verification

gh run list --workflow=269445347 --limit 1 --json conclusion returns 'success' (Sunshine, run 25497271164). run-log.md updated with passing run ID. T01 workflows (5/5) remain passing. AionUI/WGCloud/Yuxi failures are not runner-starved and out of scope for T04.

## Verification Evidence

| # | Command | Exit Code | Verdict | Duration |
|---|---------|-----------|---------|----------|
| 1 | `gh run list --workflow=269445347 --limit 1 --json conclusion` | 0 | ✅ pass | 5000ms |
| 2 | `gh run view 25497271164 --json status,conclusion` | 0 | ✅ pass | 5000ms |
| 3 | `gh run list --workflow=269476299/269298887/269576174 --limit 1 --json conclusion` | 0 | ⚠️ partial pass — Sunshine passes, AionUI/WGCloud/Yuxi fail (out of scope for T04) | 5000ms |

## Deviations

T04 plan expected to run `docker build` locally to diagnose; Docker Desktop was not running on the Windows host. Diagnostic path was redirected to GitHub Actions logs via tee-to-tmp pattern instead.

## Known Issues

AionUI (269476299), WGCloud (269298887), Yuxi (269576174) still show failure conclusion. Their root causes are unknown — further diagnosis needed in a separate task. Sunshine is the only workflow this task addressed.

## Files Created/Modified

- `scripts/dockerfiles/sunshine/Dockerfile`
- `.gsd/milestones/M001/slices/S01/run-log.md`
