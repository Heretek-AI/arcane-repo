#!/usr/bin/env python3
"""
Verification script for S05 (VitePress static site generation and deployment).
Validates site structure, page generation, CI wiring, and build output.

Run: python scripts/verify-s05.py
"""
import json
import os
import subprocess
import sys
import io

# Fix Windows console encoding for emoji output (MEM151)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
PASS = "[PASS]"
FAIL = "[FAIL]"
results = []


def check(name, condition, detail=""):
    status = PASS if condition else FAIL
    results.append((name, status, detail))
    print(f"  {status} {name}" + (f" — {detail}" if detail else ""))
    return condition


def resolve_cmd(cmd):
    """On Windows, resolve bare 'npm'/'npx'/'node' to .cmd variants."""
    if sys.platform == "win32" and cmd and cmd[0] in ("npm", "npx"):
        return [cmd[0] + ".cmd"] + cmd[1:]
    return cmd


def run_cmd(cmd, cwd=None, timeout=120):
    """Run a command and return (exit_code, stdout, stderr)."""
    cmd = resolve_cmd(cmd)
    try:
        result = subprocess.run(
            cmd, cwd=cwd or ROOT, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)


def main():
    print("=" * 60)
    print("S05 Verification Script")
    print("=" * 60)

    # ─────────────────────────────────────────────────────────────
    # Check 1: docs/ directory exists with package.json
    # ─────────────────────────────────────────────────────────────
    docs_dir_exists = os.path.isdir(DOCS)
    pkg_json_path = os.path.join(DOCS, "package.json")
    pkg_json_exists = os.path.isfile(pkg_json_path)
    check("docs/ directory exists", docs_dir_exists)
    check("docs/package.json exists", pkg_json_exists)

    # ─────────────────────────────────────────────────────────────
    # Check 2: docs/.vitepress/config.mts exists
    # ─────────────────────────────────────────────────────────────
    config_path = os.path.join(DOCS, ".vitepress", "config.mts")
    check("docs/.vitepress/config.mts exists", os.path.isfile(config_path))

    # ─────────────────────────────────────────────────────────────
    # Check 3: scripts/generate-docs.js exists
    # ─────────────────────────────────────────────────────────────
    gen_script = os.path.join(ROOT, "scripts", "generate-docs.js")
    check("scripts/generate-docs.js exists", os.path.isfile(gen_script))

    # ─────────────────────────────────────────────────────────────
    # Check 4: Run npm run docs:generate — exit code 0
    # ─────────────────────────────────────────────────────────────
    code, out, err = run_cmd(["npm", "run", "docs:generate"], cwd=DOCS)
    gen_success = code == 0
    gen_detail = out.split("\n")[-1] if out else (err.split("\n")[-1] if err else "")
    check("npm run docs:generate exits 0", gen_success, gen_detail)

    # ─────────────────────────────────────────────────────────────
    # Check 5: Count generated template pages >= 785
    # ─────────────────────────────────────────────────────────────
    templates_dir = os.path.join(DOCS, "templates")
    if os.path.isdir(templates_dir):
        template_pages = [
            f for f in os.listdir(templates_dir)
            if f.endswith(".md") and f != "index.md"
        ]
        template_count = len(template_pages)
    else:
        template_count = 0
    check("Template pages >= 785", template_count >= 785,
          f"{template_count} pages")

    # ─────────────────────────────────────────────────────────────
    # Check 6: Count generated category pages >= 10
    # ─────────────────────────────────────────────────────────────
    categories_dir = os.path.join(DOCS, "categories")
    if os.path.isdir(categories_dir):
        category_pages = [
            f for f in os.listdir(categories_dir)
            if f.endswith(".md") and f != "index.md"
        ]
        category_count = len(category_pages)
    else:
        category_count = 0
    check("Category pages >= 10", category_count >= 10,
          f"{category_count} pages")

    # ─────────────────────────────────────────────────────────────
    # Check 7: docs/categories/index.md exists and non-empty
    # ─────────────────────────────────────────────────────────────
    cat_index = os.path.join(DOCS, "categories", "index.md")
    cat_index_exists = os.path.isfile(cat_index)
    cat_index_size = os.path.getsize(cat_index) if cat_index_exists else 0
    check("docs/categories/index.md exists and non-empty",
          cat_index_exists and cat_index_size > 0,
          f"{cat_index_size} bytes")

    # ─────────────────────────────────────────────────────────────
    # Check 8: docs/templates/index.md exists and non-empty
    # ─────────────────────────────────────────────────────────────
    tmpl_index = os.path.join(DOCS, "templates", "index.md")
    tmpl_index_exists = os.path.isfile(tmpl_index)
    tmpl_index_size = os.path.getsize(tmpl_index) if tmpl_index_exists else 0
    check("docs/templates/index.md exists and non-empty",
          tmpl_index_exists and tmpl_index_size > 0,
          f"{tmpl_index_size} bytes")

    # ─────────────────────────────────────────────────────────────
    # Check 9: docs/index.md contains 'Arcane' or 'Registry'
    # ─────────────────────────────────────────────────────────────
    site_index = os.path.join(DOCS, "index.md")
    site_index_exists = os.path.isfile(site_index)
    if site_index_exists:
        with open(site_index, encoding="utf-8") as f:
            content = f.read()
        has_keywords = "Arcane" in content or "Registry" in content
    else:
        has_keywords = False
    check("docs/index.md contains 'Arcane' or 'Registry'",
          site_index_exists and has_keywords)

    # ─────────────────────────────────────────────────────────────
    # Check 10: deploy.yml contains 'docs:build'
    # ─────────────────────────────────────────────────────────────
    deploy_path = os.path.join(ROOT, ".github", "workflows", "deploy.yml")
    if os.path.isfile(deploy_path):
        with open(deploy_path, encoding="utf-8") as f:
            deploy_content = f.read()
        has_docs_build = "docs:build" in deploy_content
    else:
        has_docs_build = False
    check("deploy.yml contains 'docs:build'", has_docs_build)

    # ─────────────────────────────────────────────────────────────
    # Check 11: deploy.yml upload path references dist
    # ─────────────────────────────────────────────────────────────
    has_dist_ref = "docs/.vitepress/dist" in deploy_content if os.path.isfile(deploy_path) else False
    check("deploy.yml upload path references docs/.vitepress/dist",
          has_dist_ref)

    # ─────────────────────────────────────────────────────────────
    # Check 12: npm run docs:build — exit 0, dist/index.html exists
    # ─────────────────────────────────────────────────────────────
    code, out, err = run_cmd(["npm", "run", "docs:build"], cwd=DOCS, timeout=180)
    build_success = code == 0
    dist_index = os.path.join(DOCS, ".vitepress", "dist", "index.html")
    dist_index_exists = os.path.isfile(dist_index) if build_success else False
    check("npm run docs:build exits 0", build_success,
          out.split("\n")[-1] if out else (err.split("\n")[-1] if err else ""))
    check("docs/.vitepress/dist/index.html exists", dist_index_exists)

    # ─────────────────────────────────────────────────────────────
    # Check 13: node scripts/build-registry.js --validate-only exits 0
    # ─────────────────────────────────────────────────────────────
    code, out, err = run_cmd(
        ["node", "scripts/build-registry.js", "--validate-only"],
        timeout=120
    )
    registry_ok = code == 0
    registry_detail = out.split("\n")[-1] if out else (err.split("\n")[-1] if err else "")
    check("Registry validation (--validate-only) exits 0", registry_ok,
          registry_detail)

    # ─────────────────────────────────────────────────────────────
    # Summary
    # ─────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Template pages:  {template_count}")
    print(f"  Category pages:  {category_count}")
    print(f"  Site index size: {os.path.getsize(site_index) if site_index_exists else 0} bytes")

    passed = sum(1 for _, s, _ in results if s == PASS)
    total = len(results)
    print(f"\n  Checks: {passed}/{total} passed")

    if passed < total:
        print(f"\n{FAIL} — {total - passed} check(s) failed")
        return 1
    else:
        print(f"\n{PASS} — All checks passed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
