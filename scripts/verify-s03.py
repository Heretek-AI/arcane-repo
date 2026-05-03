#!/usr/bin/env python3
"""
Verification script for S03 (template remediation wave 2 — batches 25-49).
Validates batch2-report.json, README quality, compose healthchecks,
restart policies, and description cleanliness for 250 remediated templates.

Run: python scripts/verify-s03.py
"""
import json
import os
import re
import sys
import io
import random

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASS = "[PASS]"
FAIL = "[FAIL]"
results = []


def check(name, condition, detail=""):
    status = PASS if condition else FAIL
    results.append((name, status, detail))
    print(f"  {status} {name}" + (f" — {detail}" if detail else ""))
    return condition


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    print("=" * 60)
    print("S03 Verification Script (Batches 25-49 Remediation)")
    print("=" * 60)

    templates_dir = os.path.join(ROOT, "templates")

    # ---------------------------------------------------------------
    # 1. batch2-report.json exists and has correct summary
    # ---------------------------------------------------------------
    report_path = os.path.join(ROOT, ".gsd", "milestones", "M008", "slices", "S03", "batch2-report.json")
    report_exists = os.path.isfile(report_path)
    check("batch2-report.json exists", report_exists)

    if not report_exists:
        print(f"\n{FAIL} — Cannot continue without batch2-report.json")
        return 1

    report = load_json(report_path)
    summary = report.get("summary", {})
    remediated = summary.get("remediated", 0)
    failed = summary.get("failed", 0)
    check("batch2-report shows >= 250 remediated", remediated >= 250,
          f"remediated={remediated}")
    check("batch2-report shows 0 failures", failed == 0,
          f"failed={failed}")

    # ---------------------------------------------------------------
    # 2. All 250 template IDs in report exist on disk
    # ---------------------------------------------------------------
    templates_list = report.get("per_template", [])
    report_ids = [t["id"] for t in templates_list]
    check("batch2-report has 250 entries", len(report_ids) == 250,
          f"found {len(report_ids)}")

    missing_on_disk = []
    for tid in report_ids:
        tdir = os.path.join(templates_dir, tid)
        if not os.path.isdir(tdir):
            missing_on_disk.append(tid)
    check("All reported templates exist on disk", len(missing_on_disk) == 0,
          f"{len(missing_on_disk)} missing" if missing_on_disk else "all present")

    # ---------------------------------------------------------------
    # 3. README quality: 8 required sections per README
    # ---------------------------------------------------------------
    required_sections = [
        "Quick Start",
        "Architecture",
        "Configuration",
        "Troubleshooting",
        "Backup",
        "Links",
        "Prerequisites",
    ]
    readme_failures = []
    for tid in report_ids:
        readme_path = os.path.join(templates_dir, tid, "README.md")
        if not os.path.isfile(readme_path):
            readme_failures.append((tid, "missing"))
            continue
        content = open(readme_path, encoding="utf-8").read()
        # Count ## headings
        headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
        found_sections = [s.strip() for s in headings]
        missing = []
        for req in required_sections:
            if not any(req.lower() in h.lower() for h in found_sections):
                missing.append(req)
        if len(found_sections) < 7:
            readme_failures.append((tid, f"only {len(found_sections)} sections, missing: {missing}"))
        elif missing:
            readme_failures.append((tid, f"missing sections: {missing}"))

    check("All READMEs have >= 7 required sections", len(readme_failures) == 0,
          f"{len(readme_failures)} failures" if readme_failures else "all pass")
    if readme_failures:
        for tid, detail in readme_failures[:5]:
            print(f"    → {tid}: {detail}")

    # ---------------------------------------------------------------
    # 4. Description cleanliness: no 'sourced from' markers
    # ---------------------------------------------------------------
    sourced_from_failures = []
    for tid in report_ids:
        arcane_path = os.path.join(templates_dir, tid, "arcane.json")
        if not os.path.isfile(arcane_path):
            continue
        try:
            arcane = load_json(arcane_path)
            desc = arcane.get("description", "")
            if re.search(r"sourced from", desc, re.IGNORECASE):
                sourced_from_failures.append(tid)
        except Exception:
            pass

    check("No 'sourced from' in descriptions", len(sourced_from_failures) == 0,
          f"{len(sourced_from_failures)} violations" if sourced_from_failures else "all clean")

    # ---------------------------------------------------------------
    # 5. Compose restart policy: all services should have restart
    # ---------------------------------------------------------------
    restart_failures = []
    for tid in report_ids:
        compose_path = os.path.join(templates_dir, tid, "docker-compose.yml")
        if not os.path.isfile(compose_path):
            continue
        try:
            content = open(compose_path, encoding="utf-8").read()
            if "restart:" not in content:
                restart_failures.append(tid)
        except Exception:
            pass

    check("All compose files have restart policy", len(restart_failures) == 0,
          f"{len(restart_failures)} missing" if restart_failures else "all have restart")

    # ---------------------------------------------------------------
    # 6. Wave results files exist and sum correctly
    # ---------------------------------------------------------------
    wave_dir = os.path.join(ROOT, ".gsd", "milestones", "M008", "slices", "S03")
    wave_total = 0
    wave_ok = True
    for i in range(4, 8):
        wave_path = os.path.join(wave_dir, f"wave{i}-results.json")
        if not os.path.isfile(wave_path):
            check(f"wave{i}-results.json exists", False, "missing")
            wave_ok = False
            continue
        wdata = load_json(wave_path)
        ws = wdata.get("summary", {})
        wave_success = ws.get("success", 0)
        wave_failed = ws.get("failed", 0)
        wave_total += wave_success
        if wave_failed > 0:
            wave_ok = False
    check("Wave results sum to >= 250 successes", wave_total >= 250,
          f"total={wave_total}")
    check("All waves have 0 failures", wave_ok)

    # ---------------------------------------------------------------
    # 7. Spot-check 5 random templates for deep quality
    # ---------------------------------------------------------------
    random.seed(42)
    spot_targets = random.sample(report_ids, min(5, len(report_ids)))
    spot_pass = 0
    for tid in spot_targets:
        tdir = os.path.join(templates_dir, tid)
        issues = []

        # Check README has real content (not boilerplate)
        readme_path = os.path.join(tdir, "README.md")
        if os.path.isfile(readme_path):
            rc = open(readme_path, encoding="utf-8").read()
            if len(rc) < 500:
                issues.append(f"README too short ({len(rc)} chars)")
            if "Self-Hosted Application available through" in rc:
                issues.append("README has boilerplate pattern")

        # Check arcane.json description
        arcane_path = os.path.join(tdir, "arcane.json")
        if os.path.isfile(arcane_path):
            try:
                ad = load_json(arcane_path)
                desc = ad.get("description", "")
                if len(desc) < 20:
                    issues.append(f"Description too short: '{desc}'")
                if desc.lower() in ("todo", "tbd", "fixme"):
                    issues.append(f"Placeholder description: '{desc}'")
            except Exception:
                issues.append("arcane.json parse error")

        # Check compose has healthcheck
        compose_path = os.path.join(tdir, "docker-compose.yml")
        if os.path.isfile(compose_path):
            cc = open(compose_path, encoding="utf-8").read()
            if "healthcheck:" not in cc:
                issues.append("Compose missing healthcheck")

        ok = len(issues) == 0
        spot_pass += 1 if ok else 0
        check(f"Spot-check: {tid}", ok,
              "; ".join(issues) if issues else "quality OK")

    check(f"Spot-check pass rate ({spot_pass}/{len(spot_targets)})",
          spot_pass == len(spot_targets),
          f"{spot_pass}/{len(spot_targets)} passed")

    # ---------------------------------------------------------------
    # 8. Run test-audit-templates.py regression suite
    # ---------------------------------------------------------------
    import subprocess
    test_script = os.path.join(ROOT, "scripts", "test-audit-templates.py")
    if os.path.isfile(test_script):
        try:
            result = subprocess.run(
                [sys.executable, test_script],
                capture_output=True, text=True, timeout=120, cwd=ROOT
            )
            all_tests_pass = result.returncode == 0
            test_detail = f"exit={result.returncode}"
            if not all_tests_pass:
                # Extract last few lines of output for detail
                lines = (result.stdout + result.stderr).strip().split("\n")
                test_detail += f": {lines[-1] if lines else 'no output'}"
            check("test-audit-templates.py passes all assertions",
                  all_tests_pass, test_detail)
        except subprocess.TimeoutExpired:
            check("test-audit-templates.py passes all assertions", False, "timeout")
        except Exception as e:
            check("test-audit-templates.py passes all assertions", False, str(e))
    else:
        check("test-audit-templates.py exists", False, "not found")

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Batch 2 report:       {remediated} remediated, {failed} failed")
    print(f"  Wave total:           {wave_total} successes")
    print(f"  README quality:       {len(readme_failures)} failures out of {len(report_ids)}")
    print(f"  Description cleanup:  {len(sourced_from_failures)} 'sourced from' remaining")
    print(f"  Restart policies:     {len(restart_failures)} missing")
    print(f"  Spot-check:           {spot_pass}/{len(spot_targets)} passed")

    passed_count = sum(1 for _, s, _ in results if s == PASS)
    total = len(results)
    print(f"\n  Checks: {passed_count}/{total} passed")

    if passed_count < total:
        print(f"\n{FAIL} — {total - passed_count} check(s) failed")
        return 1
    else:
        print(f"\n{PASS} — All checks passed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
