#!/usr/bin/env python3
"""
validate-custom-builds.py -- Comprehensive Custom-Build Template Validation

Validates all 28 custom-build templates end-to-end across five dimensions:

1. Workflow caller validation: Each .github/workflows/build-<id>.yml correctly
   references build-custom.yml via uses: with the matching template-name input
   and secrets: inherit
2. Dockerfile validation: Each scripts/dockerfiles/<id>/Dockerfile exists, is
   non-empty, starts with FROM, and contains WORKDIR + EXPOSE directives
3. Template directory validation: Each templates/<id>/ directory contains
   arcane.json (valid JSON), docker-compose.yml (valid YAML), and README.md
   (non-empty)
4. Server.py presence: If the Dockerfile references server.py, verify it exists
   at scripts/dockerfiles/<id>/server.py
5. Registry validation: node scripts/build-registry.js --validate-only exits 0

Usage:
    python scripts/validate-custom-builds.py
    python scripts/validate-custom-builds.py --verbose

Exit codes:
    0 -- all 28 templates pass all checks
    1 -- one or more checks failed

Output:
    validation-report.json -- per-template pass/fail detail
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 stdout on Windows to avoid cp1252 encoding errors
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Paths ──────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DOCKERFILES_DIR = REPO_ROOT / "scripts" / "dockerfiles"
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
TEMPLATES_DIR = REPO_ROOT / "templates"
REPORT_PATH = REPO_ROOT / "validation-report.json"
BUILD_REGISTRY = REPO_ROOT / "scripts" / "build-registry.js"

# Directories to skip during auto-discovery (not Docker-build templates)
SKIP_IDS = {"docker-elk"}

verbose = "--verbose" in sys.argv

# ── Discovery ──────────────────────────────────────────────────────────


def discover_template_ids() -> list[str]:
    """Auto-discover all template IDs from scripts/dockerfiles/*/Dockerfile.

    Returns sorted list, excluding SKIP_IDS.
    """
    ids = []
    for dockerfile in sorted(DOCKERFILES_DIR.glob("*/Dockerfile")):
        template_id = dockerfile.parent.name
        if template_id not in SKIP_IDS:
            ids.append(template_id)
    return sorted(ids)


# ── Validation checks ──────────────────────────────────────────────────


def check_workflow(template_id: str) -> tuple[bool, str]:
    """Validate caller workflow references build-custom.yml correctly.

    Checks:
    - File .github/workflows/build-<id>.yml exists
    - Contains 'uses: ./.github/workflows/build-custom.yml'
    - Contains 'template-name: <id>'
    - Contains 'secrets: inherit'
    """
    wf_path = WORKFLOWS_DIR / f"build-{template_id}.yml"
    if not wf_path.exists():
        return False, f"Workflow file missing: {wf_path.relative_to(REPO_ROOT)}"

    content = wf_path.read_text(encoding="utf-8")

    if "uses: ./.github/workflows/build-custom.yml" not in content:
        return False, f"Workflow does not reference build-custom.yml: {wf_path.name}"

    if f"template-name: {template_id}" not in content:
        return False, f"Workflow template-name mismatch (expected '{template_id}'): {wf_path.name}"

    if "secrets: inherit" not in content:
        return False, f"Workflow missing 'secrets: inherit': {wf_path.name}"

    return True, ""


def check_dockerfile(template_id: str) -> tuple[bool, str]:
    """Validate Dockerfile exists, is non-empty, starts with FROM, has WORKDIR + EXPOSE.

    Checks:
    - File scripts/dockerfiles/<id>/Dockerfile exists
    - Non-empty after stripping comments/blank lines
    - First directive is FROM
    - Contains WORKDIR directive
    - Contains EXPOSE directive
    """
    df_path = DOCKERFILES_DIR / template_id / "Dockerfile"
    if not df_path.exists():
        return False, f"Dockerfile missing: {df_path.relative_to(REPO_ROOT)}"

    content = df_path.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    non_comment = [l for l in lines if l.strip() and not l.strip().startswith("#")]

    if not non_comment:
        return False, f"Dockerfile is empty: {df_path.relative_to(REPO_ROOT)}"

    # First non-comment line must start with FROM
    first_line = non_comment[0].strip()
    first_word = first_line.split()[0].upper() if first_line.split() else ""
    if first_word != "FROM":
        return False, f"Dockerfile does not start with FROM (got '{first_word}'): {df_path.name}"

    # Collect all directives
    directives = set()
    for line in non_comment:
        parts = line.strip().split()
        if parts:
            directives.add(parts[0].upper())

    missing = []
    if "WORKDIR" not in directives:
        missing.append("WORKDIR")
    if "EXPOSE" not in directives:
        missing.append("EXPOSE")

    if missing:
        return False, f"Dockerfile missing directives ({', '.join(missing)}): {df_path.name}"

    return True, ""


def check_template_dir(template_id: str) -> tuple[bool, str]:
    """Validate template directory has required files with valid content.

    Checks:
    - templates/<id>/ directory exists
    - arcane.json exists and is valid JSON
    - docker-compose.yml exists and is valid YAML (basic syntax check)
    - README.md exists and is non-empty
    """
    tpl_dir = TEMPLATES_DIR / template_id
    if not tpl_dir.is_dir():
        return False, f"Template directory missing: {tpl_dir.relative_to(REPO_ROOT)}"

    errors = []

    # arcane.json — valid JSON
    arcane_path = tpl_dir / "arcane.json"
    if not arcane_path.exists():
        errors.append("arcane.json missing")
    else:
        try:
            data = json.loads(arcane_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                errors.append("arcane.json is not a JSON object")
        except json.JSONDecodeError as e:
            errors.append(f"arcane.json invalid JSON: {e}")

    # docker-compose.yml — exists and basic YAML validity
    dc_path = tpl_dir / "docker-compose.yml"
    if not dc_path.exists():
        errors.append("docker-compose.yml missing")
    else:
        dc_content = dc_path.read_text(encoding="utf-8").strip()
        if not dc_content:
            errors.append("docker-compose.yml is empty")
        else:
            # Basic structural check: must contain 'services:' somewhere
            if "services:" not in dc_content:
                errors.append("docker-compose.yml missing 'services:' key")

    # README.md — exists and non-empty
    readme_path = tpl_dir / "README.md"
    if not readme_path.exists():
        errors.append("README.md missing")
    else:
        if not readme_path.read_text(encoding="utf-8").strip():
            errors.append("README.md is empty")

    if errors:
        return False, "; ".join(errors)

    return True, ""


def check_server_py(template_id: str) -> tuple[bool, str]:
    """If Dockerfile references server.py, verify it exists.

    Checks:
    - Read scripts/dockerfiles/<id>/Dockerfile
    - If it contains 'server.py' (in COPY or CMD), verify
      scripts/dockerfiles/<id>/server.py exists
    - If Dockerfile does not reference server.py, this check passes vacuously
    """
    df_path = DOCKERFILES_DIR / template_id / "Dockerfile"
    if not df_path.exists():
        return True, ""  # Dockerfile check will catch this

    content = df_path.read_text(encoding="utf-8")
    if "server.py" not in content:
        return True, ""  # No server.py reference — not applicable

    server_path = DOCKERFILES_DIR / template_id / "server.py"
    if not server_path.exists():
        return False, f"Dockerfile references server.py but file missing: {server_path.relative_to(REPO_ROOT)}"

    return True, ""


def check_registry() -> tuple[bool, str]:
    """Run node scripts/build-registry.js --validate-only and confirm exit 0."""
    if not BUILD_REGISTRY.exists():
        return False, f"build-registry.js not found: {BUILD_REGISTRY.relative_to(REPO_ROOT)}"

    try:
        result = subprocess.run(
            ["node", str(BUILD_REGISTRY), "--validate-only"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()[:500] if result.stderr else ""
            stdout = result.stdout.strip()[:500] if result.stdout else ""
            detail = stderr or stdout or "(no output)"
            return False, f"build-registry.js --validate-only exited {result.returncode}: {detail}"
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "build-registry.js --validate-only timed out (60s)"
    except FileNotFoundError:
        return False, "node not found — cannot run build-registry.js"
    except Exception as e:
        return False, f"Unexpected error running build-registry.js: {e}"


# ── Summary table ──────────────────────────────────────────────────────


def print_summary(templates: dict[str, dict], registry_ok: bool) -> None:
    """Print a formatted summary table of all results."""
    # Header
    print("\n" + "=" * 90)
    print(f"{'TEMPLATE':<20} {'WORKFLOW':>10} {'DOCKERFILE':>12} {'TPL_DIR':>10} {'SERVER_PY':>12} {'STATUS':>8}")
    print("-" * 90)

    for tid in sorted(templates.keys()):
        t = templates[tid]
        wf = "✅" if t["workflow"] else "❌"
        df = "✅" if t["dockerfile"] else "❌"
        td = "✅" if t["template_dir"] else "❌"
        sp = "✅" if t["server_py"] else "❌"
        status = "PASS" if all([t["workflow"], t["dockerfile"], t["template_dir"], t["server_py"]]) else "FAIL"
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{tid:<20} {wf:>10} {df:>12} {td:>10} {sp:>12} {status_icon} {status:>5}")

    # Registry line
    print("-" * 90)
    reg_icon = "✅" if registry_ok else "❌"
    reg_status = "PASS" if registry_ok else "FAIL"
    print(f"{'REGISTRY':<20} {reg_icon:>10} {'—':>12} {'—':>10} {'—':>12} {reg_icon} {reg_status:>5}")
    print("=" * 90)


# ── Main ───────────────────────────────────────────────────────────────


def main() -> int:
    print("=" * 60)
    print("Custom-Build Template Validation")
    print("=" * 60)

    # Step 1: Discover template IDs
    print("\n[1/3] Discovering template IDs...")
    template_ids = discover_template_ids()
    print(f"  Found {len(template_ids)} templates (skipped: {', '.join(sorted(SKID)) if (SKID := SKIP_IDS) else 'none'})")

    # Step 2: Run per-template checks
    print(f"\n[2/3] Running {4 * len(template_ids)} per-template checks + registry validation...")

    results: dict[str, dict] = {}
    all_pass = True

    for tid in template_ids:
        wf_ok, wf_err = check_workflow(tid)
        df_ok, df_err = check_dockerfile(tid)
        td_ok, td_err = check_template_dir(tid)
        sp_ok, sp_err = check_server_py(tid)

        errors = []
        if wf_err:
            errors.append(f"workflow: {wf_err}")
        if df_err:
            errors.append(f"dockerfile: {df_err}")
        if td_err:
            errors.append(f"template_dir: {td_err}")
        if sp_err:
            errors.append(f"server_py: {sp_err}")

        results[tid] = {
            "workflow": wf_ok,
            "dockerfile": df_ok,
            "template_dir": td_ok,
            "server_py": sp_ok,
            "errors": errors,
        }

        template_pass = all([wf_ok, df_ok, td_ok, sp_ok])
        if not template_pass:
            all_pass = False

        if verbose or not template_pass:
            status = "✅" if template_pass else "❌"
            print(f"  {status} {tid}")
            if errors:
                for e in errors:
                    print(f"      → {e}")

    # Step 3: Registry validation
    print("\n[3/3] Running registry validation...")
    reg_ok, reg_err = check_registry()
    if not reg_ok:
        all_pass = False
        print(f"  ❌ Registry: {reg_err}")
    else:
        print("  ✅ Registry: build-registry.js --validate-only passed")

    # Compute totals
    passed = sum(1 for t in results.values() if all([t["workflow"], t["dockerfile"], t["template_dir"], t["server_py"]]))
    failed = len(results) - passed
    if not reg_ok:
        failed += 1  # registry counts as a failure

    # Summary table
    print_summary(results, reg_ok)

    # Write report
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total": len(template_ids),
        "passed": passed,
        "failed": failed,
        "registry_ok": reg_ok,
        "templates": results,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"\nReport written to: {REPORT_PATH.relative_to(REPO_ROOT)}")

    # Final result
    print("\n" + "=" * 60)
    if all_pass:
        print(f"RESULT: PASS — all {len(template_ids)} templates validated + registry OK")
        print("=" * 60)
        return 0
    else:
        print(f"RESULT: FAIL — {failed} failure(s)")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
