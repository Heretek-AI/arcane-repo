#!/usr/bin/env python3
"""
verify-templates.py -- Dockerfile Template Verification Script

Validates that Dockerfile templates (uv-python, node-alpine) load correctly,
apply variable substitution without errors, and produce structurally valid
Dockerfiles.

Templates are simplified patterns -- they capture the core structure of each
Dockerfile pattern but don't reproduce project-specific customizations
(conditional blocks, multiple ENV vars, COPY commands for server.py, etc.).

Usage:
    python scripts/verify-templates.py              # run all checks
    python scripts/verify-templates.py --verbose     # show generated Dockerfiles
    python scripts/verify-templates.py --strict      # fail on warnings too

Exit codes:
    0 -- all checks passed
    1 -- one or more checks failed
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from string import Template
from typing import Any

# ── Paths ──────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
TEMPLATE_DIR = REPO_ROOT / "scripts" / "dockerfiles" / "templates"
DOCKERFILES_DIR = REPO_ROOT / "scripts" / "dockerfiles"

# ── Template variable definitions ──────────────────────────────────────

UV_PYTHON_VARIABLES = {
    "onyx": {
        "UPSTREAM_REPO": "https://github.com/onyx-dot-app/onyx.git",
        "APP_SLUG": "onyx",
        "EXTRA_PACKAGES": "uvicorn fastapi",
        "EXPOSE_PORT": "8080",
        "ENV_PREFIX": "ONYX",
        "CMD_MODULE": "onyx.main:app",
    },
    "mlflow": {
        "UPSTREAM_REPO": "https://github.com/mlflow/mlflow.git",
        "APP_SLUG": "mlflow",
        "EXTRA_PACKAGES": ".[extras] uvicorn",
        "EXPOSE_PORT": "5000",
        "ENV_PREFIX": "MLFLOW",
        "CMD_MODULE": "mlflow.server:app",
    },
    "memvid": {
        "UPSTREAM_REPO": "https://github.com/memvid/memvid.git",
        "APP_SLUG": "memvid",
        "EXTRA_PACKAGES": '"memvid-sdk[full]" fastapi uvicorn',
        "EXPOSE_PORT": "8000",
        "ENV_PREFIX": "MEMVID",
        "CMD_MODULE": "memvid.server:app",
    },
    "nanobot": {
        "UPSTREAM_REPO": "https://github.com/HKUDS/nanobot.git",
        "APP_SLUG": "nanobot",
        "EXTRA_PACKAGES": ". uvicorn fastapi",
        "EXPOSE_PORT": "8000",
        "ENV_PREFIX": "NANOBOT",
        "CMD_MODULE": "nanobot.server:app",
    },
    "astrbot": {
        "UPSTREAM_REPO": "https://github.com/AstrBotDevs/AstrBot.git",
        "APP_SLUG": "astrbot",
        "EXTRA_PACKAGES": "fastapi uvicorn",
        "EXPOSE_PORT": "8000",
        "ENV_PREFIX": "ASTRBOT",
        "CMD_MODULE": "astrbot.server:app",
    },
    "kag": {
        "UPSTREAM_REPO": "https://github.com/OpenSPG/KAG.git",
        "APP_SLUG": "kag",
        "EXTRA_PACKAGES": ". fastapi uvicorn",
        "EXPOSE_PORT": "8000",
        "ENV_PREFIX": "KAG",
        "CMD_MODULE": "kag.server:app",
    },
    "rd-agent": {
        "UPSTREAM_REPO": "https://github.com/microsoft/RD-Agent.git",
        "APP_SLUG": "rd-agent",
        "EXTRA_PACKAGES": ". fastapi uvicorn",
        "EXPOSE_PORT": "8000",
        "ENV_PREFIX": "RDAGENT",
        "CMD_MODULE": "rd_agent.server:app",
    },
    "streamer-sales": {
        "UPSTREAM_REPO": "https://github.com/PeterH0323/Streamer-Sales.git",
        "APP_SLUG": "ss",
        "EXTRA_PACKAGES": "fastapi uvicorn",
        "EXPOSE_PORT": "8000",
        "ENV_PREFIX": "STREAMER_SALES",
        "CMD_MODULE": "streamer_sales.server:app",
    },
    "trendradar": {
        "UPSTREAM_REPO": "https://github.com/sansan0/TrendRadar.git",
        "APP_SLUG": "tr",
        "EXTRA_PACKAGES": "fastapi uvicorn",
        "EXPOSE_PORT": "8000",
        "ENV_PREFIX": "TRENDRADAR",
        "CMD_MODULE": "trendradar.server:app",
    },
    "yuxi": {
        "UPSTREAM_REPO": "https://github.com/xerrors/Yuxi.git",
        "APP_SLUG": "yuxi",
        "EXTRA_PACKAGES": "fastapi uvicorn",
        "EXPOSE_PORT": "8000",
        "ENV_PREFIX": "YUXI",
        "CMD_MODULE": "yuxi.server:app",
    },
}

NODE_ALPINE_VARIABLES = {
    "aionui": {
        "BUILDER_IMAGE": "node:20-slim",
        "RUNTIME_IMAGE": "oven/bun:latest",
        "UPSTREAM_REPO": "https://github.com/iOfficeAI/AionUi.git",
        "APP_SLUG": "aionui",
        "BUILD_TOOL": "bun",
        "BUILD_CMD": "bun run build:renderer:web && node scripts/build-server.mjs",
        "EXPOSE_PORT": "3000",
        "ENTRYPOINT_CMD": '["bun", "dist-server/server.mjs"]',
        "EXTRA_DEPS": "",
        "BUN_SETUP": "RUN npm install -g bun",
        "SYSTEM_DEPS": "RUN apt-get update && apt-get install -y --no-install-recommends \\\n    git ca-certificates \\\n    && rm -rf /var/lib/apt/lists/*",
        "INSTALL_CMD": "RUN bun install --ignore-scripts --network-timeout 600000",
        "BUILD_CMD_BLOCK": "RUN bun run build:renderer:web && node scripts/build-server.mjs",
        "RUNTIME_SYSTEM_DEPS": "RUN apt-get update && apt-get install -y --no-install-recommends \\\n    ca-certificates \\\n    && rm -rf /var/lib/apt/lists/*",
        "COPY_CMD": "COPY --from=builder /app/dist-server ./dist-server\nCOPY --from=builder /app/out/renderer ./out/renderer",
        "ENV_BLOCK": "ENV PORT=3000\nENV NODE_ENV=production\nENV ALLOW_REMOTE=true\nENV DATA_DIR=/data",
        "HEALTHCHECK_CMD": "HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \\\n    CMD curl -f http://localhost:${PORT:-3000}/health || exit 1",
    },
    "cc-gateway": {
        "BUILDER_IMAGE": "node:lts-alpine",
        "RUNTIME_IMAGE": "node:lts-alpine",
        "UPSTREAM_REPO": "https://github.com/motiful/cc-gateway.git",
        "APP_SLUG": "ccgw",
        "BUILD_TOOL": "npm",
        "BUILD_CMD": "npx tsc --skipLibCheck 2>/dev/null || echo WARN: tsc build had warnings",
        "EXPOSE_PORT": "8000",
        "ENTRYPOINT_CMD": "sh -c 'node server.js --port ${CC_GATEWAY_PORT:-8000} 2>/dev/null || echo cc-gateway server entry not found && tail -f /dev/null'",
        "EXTRA_DEPS": "",
        "BUN_SETUP": "",
        "SYSTEM_DEPS": "RUN apt-get update && apt-get install -y --no-install-recommends \\\n    git ca-certificates \\\n    && rm -rf /var/lib/apt/lists/*",
        "INSTALL_CMD": "RUN npm ci --ignore-scripts --network-timeout 600000 2>/dev/null || \\\n    npm install --legacy-peer-deps --network-timeout 600000 2>/dev/null || \\\n    echo WARN: npm install had issues",
        "BUILD_CMD_BLOCK": "RUN npx tsc --skipLibCheck 2>/dev/null || echo WARN: tsc build had warnings",
        "RUNTIME_SYSTEM_DEPS": "RUN apk add --no-cache git",
        "COPY_CMD": "COPY --from=builder /app /app",
        "ENV_BLOCK": "ENV CC_GATEWAY_PORT=8000",
        "HEALTHCHECK_CMD": "",
    },
    "sillytavern": {
        "BUILDER_IMAGE": "node:lts-alpine",
        "RUNTIME_IMAGE": "node:lts-alpine",
        "UPSTREAM_REPO": "https://github.com/SillyTavern/SillyTavern.git",
        "APP_SLUG": "st",
        "BUILD_TOOL": "npm",
        "BUILD_CMD": "echo SillyTavern: dependencies installed",
        "EXPOSE_PORT": "8000",
        "ENTRYPOINT_CMD": "sh -c 'if [ -f /app/server.js ]; then node /app/server.js --port ${SILLYTAVERN_PORT:-8000}; else echo Server entry not found && tail -f /dev/null; fi'",
        "EXTRA_DEPS": "",
        "BUN_SETUP": "",
        "SYSTEM_DEPS": "RUN apt-get update && apt-get install -y --no-install-recommends \\\n    git ca-certificates \\\n    && rm -rf /var/lib/apt/lists/*",
        "INSTALL_CMD": "RUN npm ci --ignore-scripts --network-timeout 600000 2>/dev/null; \\\n    echo SillyTavern: dependencies installed",
        "BUILD_CMD_BLOCK": "RUN echo SillyTavern: dependencies installed",
        "RUNTIME_SYSTEM_DEPS": "RUN apk add --no-cache git",
        "COPY_CMD": "COPY --from=builder /app /app",
        "ENV_BLOCK": "ENV SILLYTAVERN_PORT=8000",
        "HEALTHCHECK_CMD": "",
    },
    "rowboat": {
        "BUILDER_IMAGE": "node:18-alpine",
        "RUNTIME_IMAGE": "node:18-alpine",
        "UPSTREAM_REPO": "https://github.com/rowboatlabs/rowboat.git",
        "APP_SLUG": "rowboat",
        "BUILD_TOOL": "npm",
        "BUILD_CMD": "npm run build",
        "EXPOSE_PORT": "3000",
        "ENTRYPOINT_CMD": '["python3", "/app/server.py"]',
        "EXTRA_DEPS": "libc6-compat",
        "BUN_SETUP": "",
        "SYSTEM_DEPS": "RUN apt-get update && apt-get install -y --no-install-recommends \\\n    git ca-certificates libc6-compat \\\n    && rm -rf /var/lib/apt/lists/*",
        "INSTALL_CMD": "RUN npm ci",
        "BUILD_CMD_BLOCK": "RUN npm run build",
        "RUNTIME_SYSTEM_DEPS": "RUN apk add --no-cache curl",
        "COPY_CMD": "COPY --from=builder /app /app",
        "ENV_BLOCK": "ENV NODE_ENV=production\nENV PORT=3000\nENV HOSTNAME=0.0.0.0",
        "HEALTHCHECK_CMD": "HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=60s \\\n    CMD curl -f http://localhost:3000/api/docs 2>/dev/null || curl -f http://localhost:${PORT:-3000}/ || exit 1",
    },
    "vane": {
        "BUILDER_IMAGE": "node:20-slim",
        "RUNTIME_IMAGE": "node:20-slim",
        "UPSTREAM_REPO": "https://github.com/ItzCrazyKns/Vane.git",
        "APP_SLUG": "vane",
        "BUILD_TOOL": "npm",
        "BUILD_CMD": "npx next build 2>/dev/null || echo WARN: next build failed",
        "EXPOSE_PORT": "3000",
        "ENTRYPOINT_CMD": "sh -c 'if [ -d /app/.next ]; then npx next start -p ${VANE_PORT:-3000}; else echo No build artifacts && tail -f /dev/null; fi'",
        "EXTRA_DEPS": "python3 python3-pip sqlite3",
        "BUN_SETUP": "",
        "SYSTEM_DEPS": "RUN apt-get update && apt-get install -y --no-install-recommends \\\n    git ca-certificates python3 python3-pip sqlite3 \\\n    && rm -rf /var/lib/apt/lists/*",
        "INSTALL_CMD": "RUN npm install --legacy-peer-deps --network-timeout 600000",
        "BUILD_CMD_BLOCK": "RUN npx next build 2>/dev/null || echo WARN: next build failed",
        "RUNTIME_SYSTEM_DEPS": "RUN apt-get update && apt-get install -y --no-install-recommends sqlite3 && rm -rf /var/lib/apt/lists/*",
        "COPY_CMD": "COPY --from=builder /app /app",
        "ENV_BLOCK": "ENV NODE_ENV=production VANE_PORT=3000",
        "HEALTHCHECK_CMD": "",
    },
}

# All template variables that must be substituted (no $VAR or ${VAR} remaining)
ALL_TEMPLATE_VARS = {
    # uv-python core
    "UPSTREAM_REPO", "APP_SLUG", "EXTRA_PACKAGES", "EXPOSE_PORT",
    "ENV_PREFIX", "CMD_MODULE",
    # node-alpine core
    "BUILDER_IMAGE", "RUNTIME_IMAGE", "BUILD_TOOL", "BUILD_CMD",
    "ENTRYPOINT_CMD", "EXTRA_DEPS",
    # node-alpine block
    "SYSTEM_DEPS", "BUN_SETUP", "INSTALL_CMD", "BUILD_CMD_BLOCK",
    "RUNTIME_SYSTEM_DEPS", "COPY_CMD", "ENV_BLOCK", "HEALTHCHECK_CMD",
}

# Required directives in order for a valid Dockerfile
REQUIRED_DIRECTIVES = ["FROM", "WORKDIR", "EXPOSE"]

# ── Helpers ────────────────────────────────────────────────────────────

verbose = "--verbose" in sys.argv
strict = "--strict" in sys.argv

errors: list[str] = []
warnings: list[str] = []


def error(msg: str) -> None:
    errors.append(msg)
    print(f"  [FAIL] {msg}")


def warn(msg: str) -> None:
    warnings.append(msg)
    print(f"  [WARN] {msg}")


def ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def load_template(name: str) -> Template | None:
    """Load a Dockerfile template by name."""
    path = TEMPLATE_DIR / f"{name}.Dockerfile.template"
    if not path.exists():
        error(f"Template not found: {path}")
        return None
    try:
        content = path.read_text(encoding="utf-8")
        return Template(content)
    except Exception as e:
        error(f"Failed to parse template {name}: {e}")
        return None


def apply_template(tmpl: Template, variables: dict[str, str], name: str) -> str | None:
    """Apply variables to a template, checking for unresolved vars."""
    try:
        result = tmpl.safe_substitute(variables)
    except Exception as e:
        error(f"Template substitution failed for {name}: {e}")
        return None

    # Check for unresolved template variables
    unresolved = re.findall(r'\$[A-Z_]+|\$\{[A-Z_]+\}', result)
    if unresolved:
        unique = sorted(set(unresolved))
        warn(f"Unresolved variables in {name}: {', '.join(unique)}")

    return result


def validate_dockerfile_syntax(content: str, name: str) -> bool:
    """Check that generated content has valid Dockerfile structure."""
    lines = content.strip().split("\n")
    non_comment = [l for l in lines if l.strip() and not l.strip().startswith("#")]

    if not non_comment:
        error(f"Generated Dockerfile for {name} is empty")
        return False

    # Must start with FROM
    first_directive = None
    for line in non_comment:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            first_directive = stripped.split()[0].upper() if stripped.split() else ""
            break

    if first_directive != "FROM":
        error(f"Generated Dockerfile for {name} does not start with FROM (got: {first_directive})")
        return False

    # Check required directives exist
    directives_found = set()
    for line in non_comment:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            parts = stripped.split()
            if parts:
                directives_found.add(parts[0].upper())

    missing = [d for d in REQUIRED_DIRECTIVES if d not in directives_found]
    if missing:
        error(f"Generated Dockerfile for {name} missing directives: {', '.join(missing)}")
        return False

    return True


def check_directive_order(content: str, name: str) -> bool:
    """Verify directives appear in correct Dockerfile order."""
    lines = content.strip().split("\n")
    non_comment = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]

    # Extract directive sequence
    directives = []
    for line in non_comment:
        parts = line.split()
        if parts:
            directives.append(parts[0].upper())

    # FROM must be first
    if not directives or directives[0] != "FROM":
        error(f"Generated Dockerfile for {name}: FROM must be first directive")
        return False

    # EXPOSE must come after WORKDIR
    if "WORKDIR" in directives and "EXPOSE" in directives:
        workdir_idx = directives.index("WORKDIR")
        expose_idx = directives.index("EXPOSE")
        if expose_idx < workdir_idx:
            error(f"Generated Dockerfile for {name}: EXPOSE appears before WORKDIR")
            return False

    # CMD/ENTRYPOINT should be last (or near last)
    for cmd_directive in ("CMD", "ENTRYPOINT"):
        if cmd_directive in directives:
            cmd_idx = directives.index(cmd_directive)
            if cmd_idx < len(directives) - 3:
                warn(f"Generated Dockerfile for {name}: {cmd_directive} appears early (index {cmd_idx}/{len(directives)})")

    return True


def check_variable_values(generated: str, variables: dict[str, str], name: str) -> bool:
    """Verify that variable values appear in the generated output.

    Handles multiline values (containing \\n) by checking each line separately.
    Empty values are skipped (they represent optional block variables left blank).
    """
    all_ok = True
    for var_name, var_value in variables.items():
        if not var_value:
            continue  # empty = optional block variable not used

        # For multiline values, check each non-empty line appears
        if "\\n" in var_value:
            lines = [l.strip() for l in var_value.split("\\n") if l.strip()]
            for line in lines:
                if line not in generated:
                    warn(f"Variable {var_name}: line {line!r} not found in generated Dockerfile for {name}")
                    all_ok = False
        else:
            if var_value not in generated:
                warn(f"Variable {var_name}={var_value!r} not found in generated Dockerfile for {name}")
                all_ok = False
    return all_ok


def strip_comments(content: str) -> str:
    """Remove comment lines and normalize whitespace."""
    lines = content.split("\n")
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            result.append(stripped)
    return "\n".join(result)


def check_original_exists(name: str) -> bool:
    """Check that an original Dockerfile exists for comparison."""
    path = DOCKERFILES_DIR / name / "Dockerfile"
    if not path.exists():
        warn(f"Original Dockerfile not found: {path}")
        return False
    return True


# ── Verification checks ────────────────────────────────────────────────

def verify_template_loads(name: str) -> Template | None:
    """Check that template file loads without errors."""
    print(f"\n  Loading template: {name}")
    tmpl = load_template(name)
    if tmpl:
        ok(f"Template {name} loaded successfully")
    return tmpl


def verify_uv_python_templates(tmpl: Template) -> int:
    """Verify uv-python template with all 10 Dockerfile variable sets."""
    passed = 0
    total = len(UV_PYTHON_VARIABLES)

    for dockerfile_name, variables in sorted(UV_PYTHON_VARIABLES.items()):
        print(f"\n  Testing uv-python -> {dockerfile_name}")

        # Apply template
        generated = apply_template(tmpl, variables, dockerfile_name)
        if not generated:
            continue

        # Validate syntax
        if not validate_dockerfile_syntax(generated, dockerfile_name):
            continue

        # Check directive order
        if not check_directive_order(generated, dockerfile_name):
            continue

        # Check variable values appear
        check_variable_values(generated, variables, dockerfile_name)

        # Verify original exists (for reference)
        check_original_exists(dockerfile_name)

        if verbose:
            print(f"\n    --- Generated Dockerfile for {dockerfile_name} ---")
            for line in generated.split("\n"):
                print(f"    {line}")
            print(f"    --- End ---\n")

        ok(f"uv-python -> {dockerfile_name}: syntax valid, variables substituted")
        passed += 1

    return passed


def verify_node_alpine_templates(tmpl: Template) -> int:
    """Verify node-alpine template with all 5 Dockerfile variable sets."""
    passed = 0
    total = len(NODE_ALPINE_VARIABLES)

    for dockerfile_name, variables in sorted(NODE_ALPINE_VARIABLES.items()):
        print(f"\n  Testing node-alpine -> {dockerfile_name}")

        # Apply template
        generated = apply_template(tmpl, variables, dockerfile_name)
        if not generated:
            continue

        # Validate syntax
        if not validate_dockerfile_syntax(generated, dockerfile_name):
            continue

        # Check directive order
        if not check_directive_order(generated, dockerfile_name):
            continue

        # Check variable values appear
        check_variable_values(generated, variables, dockerfile_name)

        # Verify original exists (for reference)
        check_original_exists(dockerfile_name)

        if verbose:
            print(f"\n    --- Generated Dockerfile for {dockerfile_name} ---")
            for line in generated.split("\n"):
                print(f"    {line}")
            print(f"    --- End ---\n")

        ok(f"node-alpine -> {dockerfile_name}: syntax valid, variables substituted")
        passed += 1

    return passed


def verify_no_unresolved_vars(content: str, name: str) -> bool:
    """Check that no template variables remain unresolved."""
    pattern = re.compile(r'\$[A-Z_]{2,}|\$\{[A-Z_]{2,}\}')
    matches = pattern.findall(content)
    if matches:
        unique = sorted(set(matches))
        error(f"Unresolved template variables in {name}: {', '.join(unique)}")
        return False
    return True


def verify_template_files_exist() -> bool:
    """Check that both template files exist."""
    all_ok = True
    for name in ("uv-python", "node-alpine"):
        path = TEMPLATE_DIR / f"{name}.Dockerfile.template"
        if path.exists():
            ok(f"Template file exists: {path.relative_to(REPO_ROOT)}")
        else:
            error(f"Template file missing: {path.relative_to(REPO_ROOT)}")
            all_ok = False
    return all_ok


# ── Main ───────────────────────────────────────────────────────────────

def main() -> int:
    print("=" * 60)
    print("Dockerfile Template Verification")
    print("=" * 60)

    # Step 1: Check template files exist
    print("\n[1/4] Checking template files...")
    if not verify_template_files_exist():
        print("\n" + "=" * 60)
        print(f"RESULT: FAIL -- {len(errors)} error(s), {len(warnings)} warning(s)")
        print("=" * 60)
        return 1

    # Step 2: Load templates
    print("\n[2/4] Loading templates...")
    uv_python_tmpl = verify_template_loads("uv-python")
    node_alpine_tmpl = verify_template_loads("node-alpine")

    if not uv_python_tmpl or not node_alpine_tmpl:
        print("\n" + "=" * 60)
        print(f"RESULT: FAIL -- {len(errors)} error(s), {len(warnings)} warning(s)")
        print("=" * 60)
        return 1

    # Step 3: Verify uv-python template with 10 Dockerfiles
    print("\n[3/4] Verifying uv-python template (10 Dockerfiles)...")
    uv_passed = verify_uv_python_templates(uv_python_tmpl)
    print(f"\n  uv-python: {uv_passed}/{len(UV_PYTHON_VARIABLES)} passed")

    # Step 4: Verify node-alpine template with 5 Dockerfiles
    print("\n[4/4] Verifying node-alpine template (5 Dockerfiles)...")
    na_passed = verify_node_alpine_templates(node_alpine_tmpl)
    print(f"\n  node-alpine: {na_passed}/{len(NODE_ALPINE_VARIABLES)} passed")

    # Summary
    total_passed = uv_passed + na_passed
    total_tests = len(UV_PYTHON_VARIABLES) + len(NODE_ALPINE_VARIABLES)

    print("\n" + "=" * 60)
    if errors:
        print(f"RESULT: FAIL -- {len(errors)} error(s), {len(warnings)} warning(s)")
        print(f"  Passed: {total_passed}/{total_tests}")
        for e in errors:
            print(f"  ERROR: {e}")
        return 1
    elif strict and warnings:
        print(f"RESULT: FAIL (strict mode) -- {len(warnings)} warning(s)")
        for w in warnings:
            print(f"  WARNING: {w}")
        return 1
    else:
        print(f"RESULT: PASS -- {total_passed}/{total_tests} template applications verified")
        if warnings:
            print(f"  ({len(warnings)} warning(s) -- non-fatal)")
        print("=" * 60)
        return 0


if __name__ == "__main__":
    sys.exit(main())
