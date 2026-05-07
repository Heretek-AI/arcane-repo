---
phase: M001
phase_name: Fix All Failing Docker Builds
project: arcane-repo
generated: 2026-05-07T13:20:00Z
counts:
  decisions: 7
  lessons: 5
  patterns: 4
  surprises: 4
missing_artifacts: []
---

# M001: Fix All Failing Docker Builds — Structured Learnings

### Decisions

- Pin Sunshine to v2025.924.154138 tag (v2024.1.1 does not exist on LizardByte/Sunshine upstream; all tags are v2025.x.x).
  Source: S01-SUMMARY.md/key_decisions

- Add `--recurse-submodules` to git clone for cmake-based Docker builds (shallow clone does not fetch submodule content needed by cmake configure).
  Source: S01-SUMMARY.md/key_decisions

- Add `ubuntu-toolchain-r/test` PPA for gcc-13 on Ubuntu 22.04 (gcc-13 is not in default repos).
  Source: S01-SUMMARY.md/key_decisions

- Set `MAKEFLAGS="-j2"` to prevent OOM on GitHub Actions 2-core runners during C++ builds.
  Source: S01-SUMMARY.md/key_decisions

- Use `gh api repos/OWNER/REPO/actions/workflows/ID/dispatches` instead of `gh workflow run` to avoid HTTP 404 errors on workflow file paths.
  Source: S01-SUMMARY.md/key_decisions

- Use `2>&1 | tee /tmp/build.log` with PIPESTATUS check in Dockerfile RUN commands to surface hidden build errors inside shell-pipefail wrappers.
  Source: S01-SUMMARY.md/key_decisions

- AionUI, WGCloud, Yuxi are NOT runner-starved — sequential dispatch with 30s intervals did not resolve their failures; they have real build issues needing separate diagnosis outside M001 scope.
  Source: S01-SUMMARY.md/key_decisions

### Lessons

- cmake-based Docker builds need `--recurse-submodules` on `git clone --depth 1`; submodule content is not fetched by shallow clone and cmake configure fails silently.
  Source: S01-SUMMARY.md/What Happened

- `tee /tmp/build.log + PIPESTATUS` diagnostic pattern is essential for surfacing hidden build errors inside shell-pipefail wrappers in Dockerfile RUN commands — especially on Windows hosts without local Docker Desktop.
  Source: S01-SUMMARY.md/What Happened

- `gh api workflow dispatch` using numeric workflow ID is more reliable than `gh workflow run` using workflow file path — the latter returns HTTP 404 in this repo.
  Source: S01-SUMMARY.md/What Happened

- Upstream tags cannot be assumed to exist; always verify tag existence before pinning in Dockerfile (v2024.1.1 did not exist on LizardByte/Sunshine).
  Source: S01-SUMMARY.md/Deviations

- Sequential dispatch with 30-40s intervals does NOT prevent build failures from non-resource causes — use a test dispatch pattern to distinguish runner starvation from real build errors.
  Source: S01-SUMMARY.md/What Happened

### Patterns

- cmake Dockerfiles should always add `--recurse-submodules` to shallow clones to avoid silent cmake configure failures from missing third-party submodules.
  Source: S01-SUMMARY.md/patterns_established

- Tee-to-tmp diagnostic pattern: redirect build output with `2>&1 | tee /tmp/build.log` and check `PIPESTATUS` to surface hidden errors in GitHub Actions logs.
  Source: S01-SUMMARY.md/patterns_established

- `gh api` workflow dispatch using numeric workflow IDs is the reliable alternative to `gh workflow run` (which can return HTTP 404 on file paths).
  Source: S01-SUMMARY.md/patterns_established

- Set `MAKEFLAGS="-j2"` to limit C++ build parallelism and prevent OOM on GitHub Actions 2-core runners.
  Source: S01-SUMMARY.md/patterns_established

### Surprises

- Tag v2024.1.1 does not exist on LizardByte/Sunshine. All upstream tags are v2025.x.x. The assumption that a v2024 tag existed was wrong — this caused multiple failed build cycles before discovering the real issue.
  Source: S01-SUMMARY.md/What Happened

- cmake configure errors inside `scripts/linux_build.sh` were completely invisible in GitHub Actions workflow logs due to `SHELL ["/bin/bash", "-o", "pipefail"]` wrapper swallowing the exit code. Only the `tee /tmp/build.log` diagnostic pattern surfaced the real errors.
  Source: S01-SUMMARY.md/What Happened

- AionUI, WGCloud, and Yuxi still failed after sequential dispatch disproved the runner-starvation hypothesis. These have real build issues (likely missing dependencies or broken Dockerfiles) that were never diagnosed within M001 scope.
  Source: S01-SUMMARY.md/What Happened

- Docker Desktop was not available on the Windows development host, blocking the planned local `docker build` diagnosis path. The tee-to-tmp pattern in GitHub Actions logs was the only viable alternative.
  Source: S01-SUMMARY.md/Deviations
