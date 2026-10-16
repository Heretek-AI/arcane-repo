#!/usr/bin/env python3
"""Build and validate the Arcane templates registry.

Mirrors the behavior of the official getarcaneapp/templates generator
(scripts/lib/registry.ts) without the Vite+ toolchain:

  python3 scripts/build_registry.py validate   # lint templates + schema-check
  python3 scripts/build_registry.py generate   # write registry.json

Layout per template (templates/<id>/):
  compose.yaml    the Compose project (this exact name)
  .env.example    every variable compose.yaml uses without a default
  template.json   name, description, author, icon_url, tags
  README.md       deployment notes (must have a "## Deployment" section)

Environment overrides (same names as the official generator):
  REGISTRY_NAME / REGISTRY_DESCRIPTION / REGISTRY_AUTHOR / REGISTRY_URL
  REGISTRY_VERSION (seed version when no registry.json exists yet)
  PUBLIC_BASE   base URL for compose_url / env_url
  DOCS_BASE     base URL for documentation_url
  SCHEMA_URL    value of the registry "$schema" field
  BUMP_PART / CHANGED_TEMPLATE_BUMP_PART (major|minor|patch)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(ROOT, "templates")
SCHEMA_PATH = os.path.join(ROOT, "schema.json")
TAGS_PATH = os.path.join(ROOT, "tags.json")
REGISTRY_PATH = os.path.join(ROOT, "registry.json")

COMPOSE_FILE = "compose.yaml"
LEGACY_COMPOSE_FILES = ("compose.yml", "docker-compose.yml", "docker-compose.yaml")
HASH_SOURCES = (
    "template.json",
    None,
    ".env.example",
    "README.md",
)  # None = compose file

DEFAULT_PUBLIC_BASE = (
    "https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates"
)
DEFAULT_DOCS_BASE = "https://github.com/Heretek-AI/arcane-repo/tree/main/templates"
DEFAULT_REGISTRY_URL = "https://github.com/Heretek-AI/arcane-repo"

# Images allowed to keep a pinned tag (stateful services: a major upgrade can
# change the on-disk format). Everything else must track :latest (or no tag).
STATEFUL_IMAGE_RES = (
    "postgres",
    "postgis",
    "pgvector",
    "redis",
    "valkey",
    "rabbitmq",
    "mysql",
    "mariadb",
    "mongo",
    "elasticsearch",
    "opensearch",
    "clickhouse",
    "cassandra",
    "couchdb",
    "neo4j",
    "minio",
    "nats",
    "kafka",
)
FLOATING_TAGS = ("latest", "stable", "lts")

SECRET_HINT_RES = ("password", "secret", "token", "private_key", "api_key", "apikey")
PLACEHOLDER_RES = ("change-me", "changeme", "placeholder", "example", "test", "xxx")


# --------------------------------------------------------------------------- #
# registry building (ported from the official TypeScript generator)
# --------------------------------------------------------------------------- #
def to_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9-]", "-", value.lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug


def parse_bump_part(value: str | None, fallback: str) -> str:
    normalized = (value or "").lower()
    return normalized if normalized in ("major", "minor", "patch") else fallback


def bump_semver(version: str, part: str = "minor") -> str:
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:[.-].*)?$", str(version))
    if not match:
        return "1.0.0"
    major, minor, patch = (int(match.group(i)) for i in (1, 2, 3))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    return f"{major}.{minor + 1}.0"


def template_content_hash(template_dir: str, compose_file: str) -> str:
    digest = hashlib.sha256()
    for source in ("template.json", compose_file, ".env.example", "README.md"):
        path = os.path.join(template_dir, source)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        digest.update(f"{source}\n{len(content)}\n".encode("utf-8"))
        digest.update(content.encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def load_local_registry() -> dict | None:
    if not os.path.isfile(REGISTRY_PATH):
        print("No local registry.json found, starting fresh")
        return None
    try:
        with open(REGISTRY_PATH, encoding="utf-8") as fh:
            data = json.load(fh)
        print(
            f"Found local registry.json version: {data.get('version')} "
            f"with {len(data.get('templates', []))} templates"
        )
        return data
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Could not parse local registry.json: {exc}")
        return None


def list_template_dirs() -> list[str]:
    return sorted(
        entry
        for entry in os.listdir(TEMPLATES_DIR)
        if os.path.isdir(os.path.join(TEMPLATES_DIR, entry))
        and not entry.startswith(".")
    )


def find_compose_file(template_dir: str) -> str:
    if os.path.isfile(os.path.join(template_dir, COMPOSE_FILE)):
        return COMPOSE_FILE
    for legacy in LEGACY_COMPOSE_FILES:
        if os.path.isfile(os.path.join(template_dir, legacy)):
            raise RuntimeError(
                f"{os.path.relpath(os.path.join(template_dir, legacy), ROOT)} "
                f"must be named {COMPOSE_FILE}"
            )
    raise RuntimeError(
        f"No {COMPOSE_FILE} found in {os.path.relpath(template_dir, ROOT)}"
    )


def build_template_entry(dir_name: str, public_base: str, docs_base: str) -> dict:
    template_id = to_slug(dir_name)
    template_dir = os.path.join(TEMPLATES_DIR, dir_name)
    meta_path = os.path.join(template_dir, "template.json")
    if not os.path.isfile(meta_path):
        raise RuntimeError(f"Missing templates/{dir_name}/template.json (required)")
    with open(meta_path, encoding="utf-8") as fh:
        meta = json.load(fh)
    compose_file = find_compose_file(template_dir)
    if not os.path.isfile(os.path.join(template_dir, ".env.example")):
        raise RuntimeError(f"Missing templates/{dir_name}/.env.example")

    entry: dict = {
        "id": template_id,
        "name": str(meta.get("name") or ""),
        "description": str(meta.get("description") or ""),
        "version": str(meta.get("version") or ""),
        "author": str(meta.get("author") or ""),
        "compose_url": f"{public_base}/{template_id}/{compose_file}",
        "env_url": f"{public_base}/{template_id}/.env.example",
        "documentation_url": f"{docs_base}/{template_id}",
        "content_hash": template_content_hash(template_dir, compose_file),
        "tags": [str(t) for t in meta.get("tags", [])],
    }
    if meta.get("icon_url"):
        entry["icon_url"] = str(meta["icon_url"])
    for key in ("name", "description", "author"):
        if not entry[key]:
            raise RuntimeError(f'templates/{dir_name}/template.json missing "{key}"')
    if not entry["tags"]:
        raise RuntimeError(
            f'templates/{dir_name}/template.json must include non-empty "tags"'
        )
    return entry


def apply_auto_versions(templates: list[dict], previous: list[dict]) -> list[dict]:
    previous_by_id = {t["id"]: t for t in previous}
    result = []
    for template in templates:
        if template["version"]:
            result.append(template)
            continue
        prev = previous_by_id.get(template["id"])
        version = "1.0.0"
        if prev:
            version = (
                prev["version"]
                if prev.get("content_hash") == template["content_hash"]
                else bump_semver(prev.get("version", "1.0.0"), "patch")
            )
        result.append({**template, "version": version})
    return result


def detect_changes(previous: list[dict], current: list[dict]) -> dict:
    previous_by_id = {t["id"]: t for t in previous}
    current_ids = {t["id"] for t in current}
    added = [t["id"] for t in current if t["id"] not in previous_by_id]
    updated = [
        t["id"]
        for t in current
        if t["id"] in previous_by_id
        and previous_by_id[t["id"]].get("content_hash") != t["content_hash"]
    ]
    removed = [t["id"] for t in previous if t["id"] not in current_ids]
    bump_part = parse_bump_part(os.environ.get("BUMP_PART"), "minor")
    changed_bump = parse_bump_part(
        os.environ.get("CHANGED_TEMPLATE_BUMP_PART"), "patch"
    )
    part = bump_part if added else (changed_bump if (updated or removed) else None)
    return {"added": added, "updated": updated, "removed": removed, "bump_part": part}


def build_registry() -> dict:
    previous = load_local_registry()
    previous_templates = (previous or {}).get("templates", [])
    public_base = os.environ.get("PUBLIC_BASE", DEFAULT_PUBLIC_BASE).rstrip("/")
    docs_base = os.environ.get("DOCS_BASE", DEFAULT_DOCS_BASE).rstrip("/")
    templates = sorted(
        (build_template_entry(d, public_base, docs_base) for d in list_template_dirs()),
        key=lambda t: t["id"],
    )
    templates = apply_auto_versions(templates, previous_templates)
    base_version = (previous or {}).get(
        "version", os.environ.get("REGISTRY_VERSION", "1.0.0")
    )
    changes = detect_changes(previous_templates, templates)
    version = (
        bump_semver(str(base_version), changes["bump_part"])
        if changes["bump_part"]
        else str(base_version)
    )
    if changes["added"] or changes["updated"] or changes["removed"]:
        print(
            "Detected template changes -> "
            f"added={changes['added']} updated={changes['updated']} "
            f"removed={changes['removed']} -> bumping {changes['bump_part']} to {version}"
        )
    else:
        print(f"No template changes detected -> keeping version {base_version}")
    return {
        "$schema": os.environ.get(
            "SCHEMA_URL", "https://registry.getarcane.app/schema.json"
        ),
        "name": (previous or {}).get(
            "name", os.environ.get("REGISTRY_NAME", "Heretek AI Arcane Templates")
        ),
        "description": (previous or {}).get(
            "description",
            os.environ.get("REGISTRY_DESCRIPTION", "Arcane Docker Compose templates"),
        ),
        "author": (previous or {}).get(
            "author", os.environ.get("REGISTRY_AUTHOR", "Heretek-AI")
        ),
        "url": (previous or {}).get(
            "url", os.environ.get("REGISTRY_URL", DEFAULT_REGISTRY_URL)
        ),
        "version": version,
        "templates": templates,
    }


# --------------------------------------------------------------------------- #
# validation (mirrors the official template linter rules)
# --------------------------------------------------------------------------- #
class ValidationError(Exception):
    pass


def load_tags() -> tuple[set[str], dict[str, str | None]]:
    with open(TAGS_PATH, encoding="utf-8") as fh:
        data = json.load(fh)
    return set(data.get("tags", {})), data.get("aliases", {})


def extract_env_refs(compose_raw: str) -> tuple[set[str], set[str]]:
    """Return (required_vars, all_vars) referenced in compose text.

    A var counts as required when referenced as $VAR or ${VAR} (no default
    operator). $$ escapes are ignored.
    """
    required: set[str] = set()
    seen: set[str] = set()
    token = re.compile(
        r"\$(?P<esc>\$)?(?:\{(?P<braced>[A-Za-z_][A-Za-z0-9_]*)(?P<op>[^}]*)\}|(?P<plain>[A-Za-z_][A-Za-z0-9_]*))"
    )
    for match in token.finditer(compose_raw):
        if match.group("esc"):
            continue
        if match.group("braced") is not None:
            name = match.group("braced")
            op = match.group("op") or ""
            seen.add(name)
            if op == "" or not re.match(r"^(?::?[-=?]|:?\+)", op):
                # ${VAR}, ${VAR:?err}, ${VAR:+alt} -> required unless covered.
                # ${VAR:-d}, ${VAR-d}, ${VAR:=d} provide a default.
                if re.match(r"^(?::\?|\?|:\+|\+)", op) or op == "":
                    required.add(name)
        elif match.group("plain") is not None:
            name = match.group("plain")
            seen.add(name)
            required.add(name)
    return required, seen


def parse_dotenv(raw: str) -> dict[str, str]:
    env: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=(.*)$", line)
        if not match:
            continue
        value = match.group(2).strip()
        if value[:1] in ("'", '"') and len(value) > 1:
            quote = value[0]
            end = value.find(quote, 1)
            value = value[1:end] if end > 0 else value[1:]
        else:
            value = re.sub(r"(^|\s)#.*$", "", value).strip()
        env[match.group(1)] = value
    return env


def looks_secret_value(value: str) -> bool:
    lowered = value.lower()
    return not value or any(p in lowered for p in PLACEHOLDER_RES)


def validate_template(
    dir_name: str, tags: set[str], aliases: dict, warnings: list[str]
) -> None:
    template_dir = os.path.join(TEMPLATES_DIR, dir_name)
    if not re.fullmatch(r"[a-z0-9-]+", dir_name):
        raise ValidationError(f"templates/{dir_name}: id must match [a-z0-9-]+")

    compose_file = find_compose_file(template_dir)  # raises on legacy names
    compose_path = os.path.join(template_dir, compose_file)
    with open(compose_path, encoding="utf-8") as fh:
        compose_raw = fh.read()
    if yaml is None:
        raise ValidationError("PyYAML is required: pip install pyyaml")
    compose = yaml.safe_load(compose_raw)
    if not isinstance(compose, dict) or not isinstance(compose.get("services"), dict):
        raise ValidationError(
            f"templates/{dir_name}/{compose_file}: no services mapping"
        )

    meta_path = os.path.join(template_dir, "template.json")
    if not os.path.isfile(meta_path):
        raise ValidationError(f"templates/{dir_name}/template.json is missing")
    with open(meta_path, encoding="utf-8") as fh:
        meta = json.load(fh)
    for key in ("name", "description", "author", "tags"):
        if not meta.get(key):
            raise ValidationError(f'templates/{dir_name}/template.json missing "{key}"')
    for tag in meta["tags"]:
        if tag in tags:
            continue
        fixed = aliases.get(tag)
        hint = f' (use "{fixed}")' if fixed else ""
        raise ValidationError(f'templates/{dir_name}: unknown tag "{tag}"{hint}')

    icon_url = meta.get("icon_url")
    if not icon_url:
        raise ValidationError(f"templates/{dir_name}/template.json missing icon_url")
    arcane = compose.get("x-arcane") or {}
    if arcane.get("icon") != icon_url:
        raise ValidationError(
            f"templates/{dir_name}: x-arcane.icon must match template.json icon_url"
        )
    for service_name, service in compose["services"].items():
        labels = service.get("labels") or {}
        if isinstance(labels, list):
            labels = dict(item.split("=", 1) for item in labels if "=" in item)
        if "com.getarcaneapp.arcane.icon" not in labels:
            raise ValidationError(
                f"templates/{dir_name}: service {service_name} is missing the "
                "com.getarcaneapp.arcane.icon label"
            )
        if "restart" not in service:
            warnings.append(
                f"templates/{dir_name}: service {service_name} has no restart policy"
            )
        image = str(service.get("image") or "")
        if not image:
            warnings.append(
                f"templates/{dir_name}: service {service_name} has no image "
                "(build contexts cannot deploy on Arcane)"
            )
        else:
            repo, _, tag = image.rpartition(":")
            repo_lower = repo.lower()
            if "/" not in repo_lower:  # docker.io library short name
                repo_lower = f"library/{repo_lower}"
            if not tag or "/" in tag or tag.lower() in FLOATING_TAGS:
                pass
            elif any(s in repo_lower for s in STATEFUL_IMAGE_RES):
                pass
            else:
                raise ValidationError(
                    f"templates/{dir_name}: service {service_name} pins {image}; "
                    "track :latest (stateful services may keep a major-version tag)"
                )

    env_path = os.path.join(template_dir, ".env.example")
    if not os.path.isfile(env_path):
        raise ValidationError(f"templates/{dir_name}/.env.example is missing")
    with open(env_path, encoding="utf-8") as fh:
        env = parse_dotenv(fh.read())
    required, _ = extract_env_refs(compose_raw)
    missing = sorted(required - set(env))
    if missing:
        raise ValidationError(
            f"templates/{dir_name}: {', '.join(missing)} used without a default "
            "but missing from .env.example"
        )
    for key, value in env.items():
        lowered = key.lower()
        if any(h in lowered for h in SECRET_HINT_RES) and not looks_secret_value(value):
            raise ValidationError(
                f"templates/{dir_name}/.env.example: {key} looks like a real secret; "
                "leave it empty or use an obvious placeholder"
            )

    readme_path = os.path.join(template_dir, "README.md")
    if not os.path.isfile(readme_path):
        warnings.append(f"templates/{dir_name}: README.md is missing")
    else:
        with open(readme_path, encoding="utf-8") as fh:
            if "## Deployment" not in fh.read():
                warnings.append(
                    f"templates/{dir_name}: README.md has no ## Deployment section"
                )


def docker_compose_config_ok(dir_name: str) -> bool | None:
    """Run `docker compose config` with .env.example as the env file.

    Returns True/False, or None when docker is unavailable.
    """
    if shutil.which("docker") is None:
        return None
    template_dir = os.path.join(TEMPLATES_DIR, dir_name)
    result = subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            os.path.join(template_dir, COMPOSE_FILE),
            "--env-file",
            os.path.join(template_dir, ".env.example"),
            "config",
            "-q",
        ],
        capture_output=True,
        text=True,
        cwd=template_dir,
    )
    if result.returncode != 0:
        raise ValidationError(
            f"templates/{dir_name}: docker compose config failed:\n"
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    return True


def validate_registry_schema(registry: dict) -> None:
    with open(SCHEMA_PATH, encoding="utf-8") as fh:
        schema = json.load(fh)
    try:
        import jsonschema

        jsonschema.validate(registry, schema)
    except ImportError:
        for key in ("name", "description", "version", "author", "url", "templates"):
            if not registry.get(key):
                raise ValidationError(f"registry.json missing {key}")
        if not re.match(r"^\d+\.\d+\.\d+", str(registry.get("version", ""))):
            raise ValidationError("registry.json version is not semver")


def cmd_validate(_: argparse.Namespace) -> int:
    tags, aliases = load_tags()
    warnings: list[str] = []
    for dir_name in list_template_dirs():
        validate_template(dir_name, tags, aliases, warnings)
        try:
            outcome = docker_compose_config_ok(dir_name)
        except ValidationError:
            raise
        if outcome is None:
            warnings.append("docker not available; skipped compose config check")
        print(f"OK templates/{dir_name}")
    validate_registry_schema(build_registry_quiet())
    for warning in warnings:
        print(f"warning: {warning}")
    print(f"Validated {len(list_template_dirs())} template(s)")
    return 0


def build_registry_quiet() -> dict:
    real_stdout = sys.stdout
    try:
        import io

        sys.stdout = io.StringIO()
        return build_registry()
    finally:
        sys.stdout = real_stdout


def cmd_generate(args: argparse.Namespace) -> int:
    for key, value in (
        ("PUBLIC_BASE", args.public_base),
        ("DOCS_BASE", args.docs_base),
        ("REGISTRY_URL", args.registry_url),
        ("SCHEMA_URL", args.schema_url),
    ):
        if value:
            os.environ[key] = value
    registry = build_registry()
    validate_registry_schema(registry)
    if args.check:
        if not os.path.isfile(REGISTRY_PATH):
            print("registry.json does not exist; run generate without --check first")
            return 1
        with open(REGISTRY_PATH, encoding="utf-8") as fh:
            current = json.load(fh)
        if current != registry:
            print("registry.json is out of date; run generate and commit the result")
            return 1
        print("registry.json is up to date")
        return 0
    with open(REGISTRY_PATH, "w", encoding="utf-8") as fh:
        json.dump(registry, fh, indent=2)
        fh.write("\n")
    print(f"Wrote {os.path.relpath(REGISTRY_PATH, ROOT)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and validate the registry")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="lint templates and schema-check the registry")
    gen = sub.add_parser("generate", help="write registry.json")
    gen.add_argument("--public-base", default=None)
    gen.add_argument("--docs-base", default=None)
    gen.add_argument("--registry-url", default=None)
    gen.add_argument("--schema-url", default=None)
    gen.add_argument(
        "--check",
        action="store_true",
        help="fail when registry.json differs from the generated output",
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            return cmd_validate(args)
        return cmd_generate(args)
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
