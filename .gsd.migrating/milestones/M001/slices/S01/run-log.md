# Workflow Run Log — S01 Complete

## Sunshine (T04 — cmake diagnose + fix — IN PROGRESS)

| Run ID | Tag Pinned | Fix Applied | Status | Conclusion |
|---|---|---|---|---|
| 25494743219 | v2024.1.1 | gcc-13 via ubuntu-toolchain-r PPA | ❌ failure | exit 100 — cmake hidden by script wrapper |
| 25494909551 | v2024.1.1 | gcc-13 PPA + layered apt-get | ❌ failure | exit 100 — same cmake error hidden |
| 25495145682 | v2024.1.1 | gcc-13 + MAKEFLAGS="-j2" | ❌ failure | exit 100 — same cmake error hidden |
| 25496421330 | v2024.1.1 | tee build log to /tmp | ❌ failure | exit 1 — log capture worked, real cmake errors surfaced |
| 25496618009 | v2024.1.1 | tee build log | ❌ failure | exit 1 — fatal: Remote branch v2024.1.1 not found |
| 25496817478 | v2025.924.154138 | tee build log | ❌ failure | exit 1 — missing third-party submodules (moonlight-common-c/enet, Simple-Web-Server, libdisplaydevice) |
| 25497271164 | v2025.924.154138 | --recurse-submodules + tee | ✅ success | success |

### Root Causes Found (via tee /tmp/build.log fix)
1. `fatal: Remote branch v2024.1.1 not found` — Sunshine v2024.1.1 tag does not exist on remote (all tags are v2025.x.x)
2. `CMake Error at cmake/dependencies/common.cmake:10` — missing `third-party/moonlight-common-c/enet`
3. `CMake Error at cmake/dependencies/common.cmake:13` — missing `third-party/Simple-Web-Server`
4. `CMake Error at cmake/dependencies/common.cmake:16` — missing `third-party/libdisplaydevice`
   All three are git submodules not fetched by `--depth 1` clone

### Dockerfile Fix Applied
```dockerfile
RUN git clone --depth 1 --recurse-submodules --branch v2025.924.154138 https://github.com/LizardByte/Sunshine.git . \
    && chmod +x scripts/linux_build.sh
# AND tee build log:
RUN ./scripts/linux_build.sh ... 2>&1 | tee /tmp/build.log; \
    test "${PIPESTATUS[0]}" -eq 0 || { cat /tmp/build.log; exit 1; }
```

### Key Finding
The `SHELL ["/bin/bash", "-o", "pipefail"]` wrapper was swallowing exit 100 from the inner cmake script. Adding `2>&1 | tee /tmp/build.log` to the Dockerfile `RUN` command surfaced the actual cmake errors in the GitHub Actions log for the first time. Without local Docker access, this was the only way to diagnose.

## T03 — Runner-Starved Re-dispatch (AionUI, Harbor-LLM, KAG, WGCloud, Yuxi, CC Gateway) — 2026-05-07

| Run ID | Tag Pinned | Fix Applied | Status | Conclusion | Duration |
|---|---|---|---|---|---|
| 25494743219 | v2024.11.1 | gcc-13 via ubuntu-toolchain-r PPA | ❌ failure | exit code 100 | ~1 min |
| 25494909551 | v2024.11.1 | gcc-13 PPA + separated apt-get layers | ❌ failure | exit code 100 | ~1 min |
| 25495145682 | v2024.1.1 | gcc-13 PPA + MAKEFLAGS="-j2" | ❌ failure | exit code 100 | ~58 sec |

### Failure Analysis
- Run 25494743219: `E: Unable to locate package gcc-13` — PPA not added before gcc install
- Run 25494909551: gcc-13 PPA install succeeds (stage 6/6), but `linux_build.sh` cmake configure step fails with exit 100 inside Docker
- Run 25495145682: Same cmake failure — gcc-13 install fixed, but cmake configure error inside `linux_build.sh` not surfaced in workflow log
- Root cause: `scripts/linux_build.sh` cmake configure error is wrapped inside the script; actual `CMake Error: Could not find...` lines not visible in GitHub Actions workflow log
- Runner: ubuntu-24.04, docker-buildx, 2-core constraint

### Dockerfile Changes Made
- Pinned `git clone` to `v2024.1.1` (from `v2025.923.33222`)
- Added `software-properties-common`, `add-apt-repository -y ppa:ubuntu-toolchain-r/test`, `gcc-13 g++-13`
- Added `ENV MAKEFLAGS="-j2"` to prevent parallel-build OOM
- Separated gcc toolchain into dedicated RUN with proper chaining

## T03 — Runner-Starved Re-dispatch (AionUI, Harbor-LLM, KAG, WGCloud, Yuxi, CC Gateway) — 2026-05-07

Dispatched sequentially to avoid runner memory contention. Results:

| Workflow | Workflow ID | Run ID | Dispatch Order | Status | Conclusion |
|---|---|---|---|---|---|
| Harbor-LLM | 269260818 | 25484829333 | pre-existing | ✅ dispatch | success |
| KAG | 269476300 | 25484889320 | pre-existing | ✅ dispatch | success |
| CC Gateway | 269260814 | 25485314077 | pre-existing | ✅ dispatch | success |
| AionUI | 269476299 | 25495898323 | 1st | ❌ failure | failure |
| WGCloud | 269298887 | 25495943070 | 2nd | ❌ failure | failure |
| Yuxi | 269576174 | 25495982501 | 3rd | ❌ failure | failure |

### Key Finding
Sequential dispatch did NOT prevent OOM. Three workflows (AionUI, WGCloud, Yuxi) still failed after the 30-40s dispatch interval. Harbor-LLM, KAG, CC Gateway were already passing from prior runs — no new dispatch needed for those three. AionUI, WGCloud, Yuxi need further diagnosis: either runner-size upgrade or deeper build issues (not runner-starved).

## T01 Verification (5 Docker workflows — 2026-04-28)

| Workflow | Run ID (databaseId) | Dispatch | Status | Conclusion | Duration |
|---|---|---|---|---|---|

## Dispatched at: 2026-04-28 23:30 UTC

| Workflow | Run ID (databaseId) | Dispatch | Status | Conclusion | Duration |
|---|---|---|---|---|---|
| MemVid | 25474465254 | 23:30:30 | ✅ success | success | ~3 min |
| Streamer-Sales | 25474466236 | 23:30:30 | ✅ success | success | ~30 sec |
| TrendRadar | 25474467220 | 23:30:30 | ✅ success | success | ~2 min |
| UNIT3D | 25474468047 | 23:30:30 | ✅ success | success | ~3.5 min |
| MLflow | 25474469087 | 25474469087 | ✅ success | success | ~2.5 min |

## Verification Commands Run

Each workflow confirmed via:
```
gh run view <databaseId> --json status,conclusion
```

All 5 returned `status: completed, conclusion: success`.

## Verification Commands (Slice-level checks from S01-PLAN.md)

```
gh run list --workflow=<workflow-id> --limit 1 --json conclusion
# All 5 returned: "success"
```

## Notes
- `gh workflow run build-<name>.yml --ref main` fails with 404; used `gh api repos/Heretek-AI/arcane-repo/actions/workflows/<id>/dispatches -f ref=main` instead (workflow IDs from `gh workflow list`)
- All 5 runs reached "success" conclusion without any re-dispatch needed
- Prior run was already passing for all 5, confirming structural fixes from prior sessions held
- Poll interval: 30s, max 12 rounds (~6 min total)
- Run IDs are `databaseId` field (gh does not expose `id` in run list JSON)