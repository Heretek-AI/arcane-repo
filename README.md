# Arcane Template Registry

A curated registry of Docker Compose templates for Arcane. Template folders serve as the single source of truth — CI validates their structure, assembles `registry.json` from on-disk state, and publishes it to GitHub Pages. No manual registry edits, no stale entries, no sync drift between folders and the index.

> **Status:** Early development. Structure and CI are being established.

## Badges

<!-- TODO: Add CI status badge once GitHub Actions are configured -->

## Quick Start

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add, modify, or remove templates.

## How It Works

1. Each template lives in its own directory under `templates/` with an `arcane.json` metadata file and a `docker-compose.yml`.
2. A CI workflow (`build-registry.yml`) runs the `scripts/build-registry.js` script, which reads each template folder, validates it against `schema.json`, and produces `registry.json`.
3. The generated `registry.json` is deployed to GitHub Pages for consumption by Arcane clients.

## License

MIT
