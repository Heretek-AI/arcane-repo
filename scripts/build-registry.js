#!/usr/bin/env node
/**
 * build-registry.js — Arcane Template Registry Builder
 *
 * Reads template folders under templates/, validates their arcane.json metadata
 * and required files, and produces a registry.json manifest.
 *
 * Usage:
 *   node scripts/build-registry.js             # build and write registry.json
 *   node scripts/build-registry.js --validate-only  # validate only, exit non-zero on error
 *
 * Environment variables:
 *   REPO_OWNER          (default: Heretek-AI)
 *   REPO_NAME           (default: arcane-repo)
 *   DEFAULT_BRANCH      (default: main)
 *   GITHUB_REPOSITORY   (CI override: "owner/repo" format)
 */

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ── Configuration ──────────────────────────────────────────────────────

const ROOT_DIR = path.resolve(__dirname, '..');
const TEMPLATES_DIR = path.join(ROOT_DIR, 'templates');
const REGISTRY_PATH = path.join(ROOT_DIR, 'registry.json');

// Resolve repo config from env
let repoOwner, repoName;
const githubRepo = process.env.GITHUB_REPOSITORY || '';

if (githubRepo && githubRepo.includes('/')) {
  const parts = githubRepo.split('/');
  repoOwner = parts[0];
  repoName = parts[1];
} else {
  repoOwner = process.env.REPO_OWNER || 'Heretek-AI';
  repoName = process.env.REPO_NAME || 'arcane-repo';
}

const defaultBranch = process.env.DEFAULT_BRANCH || 'main';
const rawBase = `https://raw.githubusercontent.com/${repoOwner}/${repoName}/${defaultBranch}`;
const repoUrl = `https://github.com/${repoOwner}/${repoName}`;

// ── CLI flags ──────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const validateOnly = args.includes('--validate-only');

// ── Helpers ────────────────────────────────────────────────────────────

const SEMVER_RE = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$/;
const SLUG_RE = /^[a-z0-9-]+$/;
const HEX64_RE = /^[a-f0-9]{64}$/;

let errors = [];
let warnings = [];

function error(msg) {
  errors.push(msg);
  console.error(`ERROR: ${msg}`);
}

function warn(msg) {
  warnings.push(msg);
  console.error(`WARN: ${msg}`);
}

function validateStringField(obj, key, templateId, fileLabel) {
  const val = obj[key];
  if (val === undefined || val === null) {
    error(`templates/${templateId}/${fileLabel}: missing field "${key}"`);
    return false;
  }
  if (typeof val !== 'string') {
    error(`templates/${templateId}/${fileLabel}: field "${key}" must be a string`);
    return false;
  }
  if (val.length < 1) {
    error(`templates/${templateId}/${fileLabel}: field "${key}" must have minLength >= 1`);
    return false;
  }
  return true;
}

function validateTags(obj, templateId, fileLabel) {
  const tags = obj.tags;
  if (tags === undefined || tags === null) {
    error(`templates/${templateId}/${fileLabel}: missing field "tags"`);
    return false;
  }
  if (!Array.isArray(tags)) {
    error(`templates/${templateId}/${fileLabel}: field "tags" must be an array`);
    return false;
  }
  if (tags.length < 1) {
    error(`templates/${templateId}/${fileLabel}: field "tags" must be a non-empty array`);
    return false;
  }
  for (let i = 0; i < tags.length; i++) {
    if (typeof tags[i] !== 'string' || tags[i].length < 1) {
      error(`templates/${templateId}/${fileLabel}: tags[${i}] must be a non-empty string`);
    }
  }
  // Check unique tags
  if (new Set(tags).size !== tags.length) {
    warn(`templates/${templateId}/${fileLabel}: tags array contains duplicates`);
  }
  return true;
}

// ── Main build logic ───────────────────────────────────────────────────

function build() {
  errors = [];
  warnings = [];

  // 1. Ensure templates/ directory exists
  if (!fs.existsSync(TEMPLATES_DIR)) {
    error(`templates/ directory does not exist at ${TEMPLATES_DIR}`);
    return null;
  }

  // 2. Read template subdirectories
  const entries = fs.readdirSync(TEMPLATES_DIR, { withFileTypes: true });
  const templateDirs = entries
    .filter(entry => entry.isDirectory() && !entry.name.startsWith('.'))
    .map(entry => entry.name)
    .sort();

  if (templateDirs.length === 0) {
    error('templates/ directory contains no template folders');
    return null;
  }

  const templates = [];
  const seenIds = new Set();

  for (const dirName of templateDirs) {
    const dirPath = path.join(TEMPLATES_DIR, dirName);

    // 2a. Read and validate arcane.json
    const arcanePath = path.join(dirPath, 'arcane.json');
    if (!fs.existsSync(arcanePath)) {
      error(`templates/${dirName}/: missing arcane.json`);
      continue;
    }

    let arcane;
    try {
      const raw = fs.readFileSync(arcanePath, 'utf8');
      arcane = JSON.parse(raw);
    } catch (e) {
      error(`templates/${dirName}/arcane.json: invalid JSON — ${e.message}`);
      continue;
    }

    const fileLabel = 'arcane.json';

    // Validate required string fields
    const stringFields = ['id', 'name', 'description', 'version', 'author'];
    let arcaneValid = true;
    for (const field of stringFields) {
      if (!validateStringField(arcane, field, dirName, fileLabel)) {
        arcaneValid = false;
      }
    }
    // Validate tags separately (array, not string)
    if (!validateTags(arcane, dirName, fileLabel)) {
      arcaneValid = false;
    }

    // id must match slug pattern
    if (arcane.id !== undefined && typeof arcane.id === 'string') {
      if (!SLUG_RE.test(arcane.id)) {
        error(`templates/${dirName}/arcane.json: id "${arcane.id}" must match slug pattern /^[a-z0-9-]+$/`);
        arcaneValid = false;
      }
      // id must match folder name
      if (arcane.id !== dirName) {
        error(`templates/${dirName}/arcane.json: id "${arcane.id}" must match folder name "${dirName}"`);
        arcaneValid = false;
      }
    }

    // version must match semver
    if (arcane.version !== undefined && typeof arcane.version === 'string') {
      if (!SEMVER_RE.test(arcane.version)) {
        error(`templates/${dirName}/arcane.json: version "${arcane.version}" is not valid semver`);
        arcaneValid = false;
      }
    }

    // Check for duplicate IDs
    if (arcane.id && seenIds.has(arcane.id)) {
      error(`templates/: duplicate template id "${arcane.id}" found in folder "${dirName}"`);
      arcaneValid = false;
    }
    if (arcane.id) {
      seenIds.add(arcane.id);
    }

    if (!arcaneValid) {
      continue;
    }

    // 2b. Ensure required files exist
    const requiredFiles = ['docker-compose.yml', '.env.example', 'README.md'];
    let filesMissing = false;
    for (const fileName of requiredFiles) {
      if (!fs.existsSync(path.join(dirPath, fileName))) {
        error(`templates/${dirName}/: missing required file "${fileName}"`);
        filesMissing = true;
      }
    }
    if (filesMissing) {
      continue;
    }

    // 2c. Compute content_hash from all four source files
    // Four source files: arcane.json, docker-compose.yml, .env.example, README.md
    // Sorted alphabetically for determinism
    const sourceFiles = ['arcane.json', 'docker-compose.yml', '.env.example', 'README.md'].sort();
    const hash = crypto.createHash('sha256');
    for (const fileName of sourceFiles) {
      const filePath = path.join(dirPath, fileName);
      const content = fs.readFileSync(filePath);
      hash.update(content);
    }
    const contentHash = hash.digest('hex');

    // 2d. Auto-generate URL fields
    const composeUrl = `${rawBase}/templates/${dirName}/docker-compose.yml`;
    const envUrl = `${rawBase}/templates/${dirName}/.env.example`;
    const documentationUrl = `${rawBase}/templates/${dirName}/README.md`;

    // 2e. Collect enriched template entry
    templates.push({
      id: arcane.id,
      name: arcane.name,
      description: arcane.description,
      version: arcane.version,
      author: arcane.author,
      compose_url: composeUrl,
      env_url: envUrl,
      documentation_url: documentationUrl,
      content_hash: contentHash,
      tags: arcane.tags
    });
  }

  if (errors.length > 0) {
    return null;
  }

  // 3. Duplicate ID check is done per-folder above

  // 4. Assemble the full registry object
  const registry = {
    $schema: 'https://raw.githubusercontent.com/getarcaneapp/templates/main/schema.json',
    name: repoName,
    description: `Arcane template registry for ${repoName}`,
    version: '1.0.0',
    author: repoOwner,
    url: repoUrl,
    templates: templates
  };

  // 5. Validate the assembled registry
  validateRegistry(registry);

  if (errors.length > 0) {
    return null;
  }

  return registry;
}

function validateRegistry(registry) {
  // Top-level field validation
  const topFields = ['name', 'description', 'version', 'author', 'url'];
  for (const field of topFields) {
    if (typeof registry[field] !== 'string' || registry[field].length < 1) {
      error(`registry: missing or empty top-level field "${field}"`);
    }
  }

  if (!Array.isArray(registry.templates) || registry.templates.length === 0) {
    error('registry: "templates" must be a non-empty array');
    return;
  }

  // Validate each template entry has auto-generated URLs matching expected patterns
  for (const tpl of registry.templates) {
    if (!tpl.compose_url || !tpl.compose_url.startsWith(rawBase)) {
      error(`template "${tpl.id}": compose_url does not match expected raw content pattern`);
    }
    if (!tpl.env_url || !tpl.env_url.startsWith(rawBase)) {
      error(`template "${tpl.id}": env_url does not match expected raw content pattern`);
    }
    if (!tpl.documentation_url || !tpl.documentation_url.startsWith(rawBase)) {
      error(`template "${tpl.id}": documentation_url does not match expected raw content pattern`);
    }
    if (!tpl.content_hash || !HEX64_RE.test(tpl.content_hash)) {
      error(`template "${tpl.id}": content_hash must be a 64-char hex string (SHA-256)`);
    }
    if (!Array.isArray(tpl.tags) || tpl.tags.length === 0) {
      error(`template "${tpl.id}": tags must be a non-empty array`);
    }
  }
}

// ── Main ───────────────────────────────────────────────────────────────

function main() {
  const registry = build();

  const hasErrors = errors.length > 0;

  if (hasErrors) {
    if (warnings.length > 0) {
      warnings.forEach(w => console.error(`WARN: ${w}`));
    }
    process.exitCode = 1;
    return;
  }

  if (warnings.length > 0) {
    warnings.forEach(w => console.error(`WARN: ${w}`));
  }

  if (!validateOnly) {
    const json = JSON.stringify(registry, null, 2) + '\n';
    fs.writeFileSync(REGISTRY_PATH, json, 'utf8');
    console.log(`✓ Wrote registry.json (${registry.templates.length} templates)`);
  } else {
    console.log(`✓ Validation passed (${registry.templates.length} templates would be included)`);
  }

  process.exitCode = 0;
}

main();
