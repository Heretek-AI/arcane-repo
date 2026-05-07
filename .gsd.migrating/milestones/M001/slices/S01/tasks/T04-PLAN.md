---
estimated_steps: 8
estimated_files: 3
skills_used: []
---

# T04: Fix Sunshine cmake configure — diagnose locally or add build logging

The cmake configure error inside linux_build.sh is not visible in the Actions log artifact. Three dispatch cycles failed with exit 100 but the actual CMake Error lines are wrapped inside the upstream script. The blocker cannot be resolved via workflow dispatch alone.

Preferred approach: run `docker build -t sunshine-test -f scripts/dockerfiles/sunshine/Dockerfile .` locally and capture the cmake output. Alternatively, modify the Dockerfile to add `set -x` tracing or `2>&1 | tee /tmp/build.log` to the linux_build.sh invocation so cmake error lines are written to a file.

After diagnosing:
1. If cmake missing dependencies (libwayland-dev, libinput-dev, etc.): add to apt-get install step
2. If cmake version mismatch: pin cmake version or adjust CMakeLists.txt flags
3. Re-dispatch via gh api repos/Heretek-AI/arcane-repo/actions/workflows/269445347/dispatches -f ref=main
4. Verify: gh run list --workflow=build-sunshine.yml --limit 1 --json conclusion returns 'success'
5. Record run ID and passing status in run-log.md

## Inputs

- `T02-SUMMARY.md (blocker details)`
- `scripts/dockerfiles/sunshine/Dockerfile (current state)`

## Expected Output

- `Sunshine Dockerfile fixed and builds successfully`
- `gh run list --workflow=build-sunshine.yml --limit 1 --json conclusion returns 'success'`
- `run-log.md updated with passing run ID`

## Verification

gh run list --workflow=build-sunshine.yml --limit 1 --json conclusion returns 'success', and run-log.md has Sunshine entry with passing run ID
