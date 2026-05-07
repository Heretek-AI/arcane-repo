# GSD context snapshot (2026-05-07T14:42:12.364Z)

## Top project memories
- [MEM001] (gotcha) Sunshine repo tags are all v2025.x.x — v2024.1.1 tag does not exist. When pinning to a specific release tag, verify the tag exists on the remote before committing the pin. Use `git ls-remote --tags <repo>` to check available tags.
- [MEM002] (gotcha) git clone --depth 1 does NOT fetch submodules. If the build uses add_subdirectory for third-party deps, you MUST add --recurse-submodules to the clone command. Missing submodules manifest as "add_subdirectory given source ... which is not an existing directory" cmake errors.
- [MEM003] (gotcha) When a Dockerfile uses SHELL ["/bin/bash", "-o", "pipefail"], RUN commands with pipes silently swallow non-zero exit codes from earlier commands. The pipeline's exit code becomes the last command's exit code, which may be 0 even if an earlier command failed. Use `test "${PIPESTATUS[0]}" -eq 0 || ...` to check the first command's actual exit code, or redirect stderr to a log file via `2>&1 | tee /tmp/build.log` for diagnosis.
- [MEM005] (pattern) When dispatching GitHub Actions workflows programmatically, use `gh api repos/OWNER/REPO/actions/workflows/ID/dispatches -f ref=main` with the numeric workflow ID (from `gh workflow list`) rather than `gh workflow run build-<name>.yml`, which fails with HTTP 404 for workflow names that don't match the on-disk file path exactly.
- [MEM004] (convention) When diagnosing Docker build failures in GitHub Actions without local Docker (Windows host), add `2>&1 | tee /tmp/build.log` to the Dockerfile RUN command followed by a PIPESTATUS check. This surfaces hidden cmake/configure errors in the Actions log that are otherwise wrapped inside upstream build scripts.
- [MEM006] (architecture) Sunshine Docker build required: (1) ubuntu-toolchain-r/test PPA for gcc-13 on Ubuntu 22.04, (2) pin to v2025.924.154138 (v2024.1.1 tag doesn't exist), (3) --recurse-submodules for third-party deps, (4) MAKEFLAGS=-j2 to prevent OOM on 2-core runners.


…[truncated]
