#!/usr/bin/env node
/**
 * audit-templates.js — Template Quality Auditor
 *
 * Scans all templates/ subdirectories and checks for:
 *   1. Description quality (generic, short)
 *   2. Upstream links (GitHub project links in README)
 *   3. Port/value mismatches (compose default vs .env value)
 *   4. Tag consistency (single-tag, missing)
 *   5. Image references (:latest vs pinned)
 *
 * Non-serviceable templates (tagged "non-serviceable" in arcane.json) are skipped.
 *
 * Usage:
 *   node scripts/audit-templates.js                      # full audit
 *   node scripts/audit-templates.js --limit 10            # first 10 templates
 *   node scripts/audit-templates.js --limit 10 --verbose  # verbose output
 *   node scripts/audit-templates.js --output-dir ./out    # custom output dir
 *
 * Output (per-category ranked JSON files):
 *   deploy-config-issues.json
 *   description-issues.json
 *   tag-issues.json
 *   upstream-link-issues.json
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ── Configuration ──────────────────────────────────────────────────────

const ROOT_DIR = path.resolve(__dirname, '..');
const TEMPLATES_DIR = path.join(ROOT_DIR, 'templates');
const DEFAULT_OUTPUT_DIR = path.join(__dirname, 'audit-output');

// Generic description patterns to flag
const GENERIC_DESC_PATTERNS = [
  // "Self-hosted X deployment via Docker" (most common pattern)
  /self-hosted\s+\S+?\s+deployment\s+via\s+docker/i,
  // "Self-hosted X via Docker"
  /self-hosted\s+\S+?\s+via\s+docker/i,
  // "X — self-hosted via Docker Compose"
  /self-hosted\s+\S+?\s+via\s+docker\s+compose/i,
  /self-hosted\s+deployment\s+via\s+docker/i,
  /self-hosted\s+(via|through|using)\s+docker/i,
  /deploy\s+.*?\s+with\s+docker/i,
  /docker\s+.*?\s+template/i,
  /^—\s+self-hosted\s+via/i,
];

// Minimum description length to consider meaningful
const MIN_DESC_LENGTH = 30;

// Generic image names that shouldn't be counted as upstream references
const GENERIC_IMAGES = new Set([
  'python', 'node', 'nginx', 'postgres', 'redis', 'mysql',
  'mongo', 'alpine', 'ubuntu', 'debian', 'busybox', 'httpd',
  'php', 'ruby', 'golang', 'openjdk', 'eclipse-mosquitto',
  'traefik', 'portainer', 'adminer', 'memcached', 'rabbitmq',
  'elasticsearch', 'kibana', 'logstash', 'grafana', 'prometheus',
  'influxdb', 'minio', 'docker', 'caddy', 'haproxy',
  'mariadb', 'couchdb', 'nextcloud', 'wordpress',
  'drupal', 'ghost', 'joomla', 'magento', 'mediawiki',
  'nginx-proxy-manager', 'nginx-proxy-manager-zh',
]);

// ── CLI parsing ────────────────────────────────────────────────────────

const args = process.argv.slice(2);
let outputDir = DEFAULT_OUTPUT_DIR;
let limit = Infinity;
let verbose = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--output-dir' && i + 1 < args.length) {
    outputDir = path.resolve(args[++i]);
  } else if (args[i] === '--limit' && i + 1 < args.length) {
    limit = parseInt(args[++i], 10);
    if (isNaN(limit) || limit < 1) limit = Infinity;
  } else if (args[i] === '--verbose') {
    verbose = true;
  } else if (args[i] === '--help') {
    console.log(`
Usage: node scripts/audit-templates.js [options]

Options:
  --output-dir DIR   Output directory for audit JSON files
                     (default: scripts/audit-output/)
  --limit N          Only audit the first N templates
  --verbose          Show per-template progress
  --help             Show this help
`);
    process.exit(0);
  }
}

// ── Utilities ──────────────────────────────────────────────────────────

function log(...args) {
  if (verbose) console.log(...args);
}

function readFileSafe(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf-8');
  } catch {
    return null;
  }
}

function readJsonSafe(filePath) {
  const raw = readFileSafe(filePath);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function getTemplateDirs() {
  const entries = fs.readdirSync(TEMPLATES_DIR, { withFileTypes: true });
  return entries
    .filter(e => e.isDirectory())
    .map(e => e.name)
    .sort();
}

function isNonServiceable(arcane) {
  return arcane && Array.isArray(arcane.tags) && arcane.tags.includes('non-serviceable');
}

// ── Check 1: Description Quality ───────────────────────────────────────

function checkDescriptionQuality(arcane) {
  const issues = [];
  const desc = (arcane.description || '').trim();

  // Missing description
  if (!desc) {
    issues.push({ category: 'missing-description', severity: 'high', message: 'Description field is empty or missing' });
    return issues;
  }

  // Too short
  if (desc.length < MIN_DESC_LENGTH) {
    issues.push({ category: 'short-description', severity: 'medium', message: `Description is only ${desc.length} characters (minimum ${MIN_DESC_LENGTH})` });
  }

  // Generic patterns
  for (const pattern of GENERIC_DESC_PATTERNS) {
    if (pattern.test(desc)) {
      issues.push({ category: 'generic-description', severity: 'medium', message: `Description matches generic pattern: "${desc}"` });
      break;
    }
  }

  return issues;
}

// ── Check 2: Upstream Links ────────────────────────────────────────────

function checkUpstreamLinks(templateId, readmeContent) {
  const issues = [];

  if (!readmeContent) {
    issues.push({ category: 'missing-readme', severity: 'high', message: 'README.md is missing or unreadable' });
    return issues;
  }

  // Look for GitHub project links (github.com/owner/repo)
  const githubLinks = readmeContent.match(/https?:\/\/github\.com\/[\w.-]+\/[\w.-]+/gi) || [];

  // Look for links in Project Homepage section (must be a heading or link, not just word occurrence)
  const hasProjectHomepage = /##\s*(project\s+(homepage|home|website|url)|upstream|source\s+code)/i.test(readmeContent) ||
    /\[(project\s+(homepage|home|website|url)|upstream)\]/i.test(readmeContent) ||
    /homepage\s*:\s*https?:\/\//i.test(readmeContent);

  // Look for external URLs (http/https)
  const allUrls = readmeContent.match(/https?:\/\/[^\s"')\]}>]+/gi) || [];
  const nonGithubUrls = allUrls.filter(u => !u.startsWith('http://localhost') && !u.startsWith('http://0.0.0.0'));

  // Parse image refs from docker-compose to see if we can derive an upstream
  const composeContent = readFileSafe(path.join(TEMPLATES_DIR, templateId, 'docker-compose.yml'));
  const imageRefs = [];
  if (composeContent) {
    const imageLines = composeContent.match(/^\s*image:\s+(.+)$/gm) || [];
    for (const line of imageLines) {
      const ref = line.replace(/^\s*image:\s*/, '').trim();
      if (ref && !ref.includes('${')) {  // skip variable-ref images
        imageRefs.push(ref);
      }
    }
  }

  // Determine if there's a meaningful upstream link
  const hasGithubLink = githubLinks.length > 0;
  const hasHomepageSection = hasProjectHomepage;
  const hasExternalUrl = nonGithubUrls.length >= 2;  // at least 2 non-localhost URLs

  if (!hasGithubLink && !hasHomepageSection) {
    // Check if we can derive from image (must be org/repo style, not docker.io/library/official)
    const deriveableFromImage = imageRefs.some(ref => {
      const parts = ref.split('/');
      // ghcr.io/org/repo or docker.io/org/repo or quay.io/org/repo patterns
      if (parts.length < 3) return false;
      // Skip official Docker images (docker.io/library/*)
      if (parts[0] === 'docker.io' && parts[1] === 'library') return false;
      if (parts[0] === 'docker.io' && parts[1] === '') return false;
      const imageName = parts[parts.length - 1].split(':')[0];
      return !GENERIC_IMAGES.has(imageName);
    });

    if (!deriveableFromImage) {
      issues.push({ category: 'no-upstream-link', severity: 'high', message: 'No GitHub project link or Project Homepage section found in README' });
    }
  }

  // Check if there are markdown links at all
  const mdLinks = readmeContent.match(/\[([^\]]+)\]\(([^)]+)\)/g) || [];
  if (mdLinks.length < 3) {
    issues.push({ category: 'few-links', severity: 'low', message: `Only ${mdLinks.length} markdown links found in README` });
  }

  return issues;
}

// ── Check 3: Port/Value/Env Mismatches ─────────────────────────────────

function checkDeployConfig(templateId) {
  const issues = [];
  const composeContent = readFileSafe(path.join(TEMPLATES_DIR, templateId, 'docker-compose.yml'));
  const envContent = readFileSafe(path.join(TEMPLATES_DIR, templateId, '.env.example'));

  if (!composeContent) {
    issues.push({ category: 'missing-compose', severity: 'high', message: 'docker-compose.yml is missing or unreadable' });
    return issues;
  }

  if (!envContent) {
    issues.push({ category: 'missing-env', severity: 'high', message: '.env.example is missing or unreadable' });
    return issues;
  }

  // Parse env vars from .env.example: VAR=value (non-comment, non-blank lines)
  const envVars = new Map();
  for (const line of envContent.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx === -1) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    const val = trimmed.slice(eqIdx + 1).trim();
    if (key) envVars.set(key, val);
  }

  // Parse port mappings from docker-compose.yml
  // Matches: "${VAR:-8080}:3000" or "${VAR}:8080"
  // Pattern: "${VARNAME:default}:port" or "${VARNAME}:port"
  const composePortPattern = /"\$\{([A-Z_0-9][A-Z_0-9_]*)(?::([^}]*))?\}\s*:\s*(\d+)"/g;
  let portMatch;
  while ((portMatch = composePortPattern.exec(composeContent)) !== null) {
    const composeVar = portMatch[1];   // e.g. 2FAUTH_PORT
    const defaultWithDash = portMatch[2] || '';  // e.g. -8080 or 8080
    const composeDefault = defaultWithDash.replace(/^-/, '').trim();  // Strip leading dash
    const portNum = portMatch[3];  // e.g. 3000 (container-side port)

    // Find the matching env var (case-insensitive match on name)
    let matchedKey = null;
    let envValue = null;
    for (const [key, val] of envVars) {
      // Normalize comparison: strip _PORT suffix for matching
      const keyNorm = key.replace(/_PORT$/, '').toLowerCase();
      const composeNorm = composeVar.replace(/_PORT$/, '').toLowerCase();
      if (keyNorm === composeNorm || key.toLowerCase() === composeVar.toLowerCase()) {
        matchedKey = key;
        envValue = val;
        break;
      }
    }

    if (matchedKey) {
      // Check port value mismatch
      if (envValue && envValue !== composeDefault) {
        issues.push({
          category: 'port-value-mismatch',
          severity: 'high',
          message: `Port value mismatch: compose default for ${composeVar} is "${composeDefault}" but .env.example ${matchedKey}="${envValue}"`,
          composeVar,
          composeDefault,
          envKey: matchedKey,
          envValue
        });
      }
    } else {
      // Check if a similar name exists (e.g., 2FAUTH_PORT in compose vs TWOFAUTH_PORT in .env)
      const composeVarLower = composeVar.toLowerCase();
      let similarVar = null;
      for (const key of envVars.keys()) {
        // Levenshtein-like: check if one contains the other or is off by a few chars
        const keyLower = key.toLowerCase();
        if (keyLower.includes(composeVarLower) || composeVarLower.includes(keyLower)) {
          similarVar = key;
          break;
        }
        // Check for port-specific match
        const keyPort = key.replace(/_PORT$/, '').toLowerCase();
        const composePort = composeVar.replace(/_PORT$/, '').toLowerCase();
        if (keyPort === composePort) {
          similarVar = key;
          break;
        }
        // Fuzzy match: shared character sequence of at least 4 chars
        // Catches cases like 2FAUTH vs TWOFAUTH
        const minShared = 4;
        for (let i = 0; i <= composePort.length - minShared; i++) {
          const sub = composePort.slice(i, i + minShared);
          if (keyPort.includes(sub)) {
            similarVar = key;
            break;
          }
        }
        if (similarVar) break;
      }

      if (similarVar) {
        issues.push({
          category: 'env-var-name-mismatch',
          severity: 'high',
          message: `Env var name mismatch: compose uses "${composeVar}" but .env.example has "${similarVar}" (similar name)`,
          composeVar,
          similarEnvKey: similarVar
        });
      } else {
        // Variable used in compose but not defined in .env.example
        issues.push({
          category: 'missing-env-var',
          severity: 'medium',
          message: `Env var "${composeVar}" referenced in docker-compose.yml but not found in .env.example`,
          composeVar
        });
      }
    }
  }

  // Parse env var refs in environment blocks — allow leading digits (e.g. 2FAUTH_PORT)
  const composeEnvPattern = /\$\{([A-Z_0-9][A-Z0-9_]*(?:_[A-Z0-9_]+)*)(?::[^}]*)?\}/gi;
  const composeEnvVars = new Set();
  let envMatch;
  while ((envMatch = composeEnvPattern.exec(composeContent)) !== null) {
    composeEnvVars.add(envMatch[1]);
  }

  // Check each compose env var exists in .env.example
  for (const composeVar of composeEnvVars) {
    // Skip common internal vars and healthcheck vars
    if (composeVar.startsWith('_') || composeVar === 'VAR') continue;

    const existsInEnv = [...envVars.keys()].some(k =>
      k === composeVar ||
      k.replace(/_PORT$/, '').toLowerCase() === composeVar.replace(/_PORT$/, '').toLowerCase()
    );

    if (!existsInEnv) {
      // Only flag as warning, not high severity since env vars can have defaults
      issues.push({
        category: 'missing-env-var',
        severity: 'low',
        message: `Env var "${composeVar}" referenced in docker-compose.yml but not defined in .env.example`
      });
    }
  }

  return issues;
}

// ── Check 4: Tag Consistency ──────────────────────────────────────────

function checkTagConsistency(arcane) {
  const issues = [];
  const tags = arcane.tags || [];

  if (tags.length === 0) {
    issues.push({ category: 'no-tags', severity: 'high', message: 'No tags defined' });
  } else if (tags.length === 1) {
    issues.push({ category: 'single-tag', severity: 'medium', message: `Only 1 tag: "${tags[0]}". Consider adding more descriptive tags.` });
  }

  // Check for very short tags
  for (const tag of tags) {
    if (tag.length < 3) {
      issues.push({ category: 'short-tag', severity: 'low', message: `Tag "${tag}" is very short` });
    }
  }

  return issues;
}

// ── Check 5: Image References ──────────────────────────────────────────

function checkImageReferences(composeContent) {
  const issues = [];
  if (!composeContent) return issues;

  const imageLines = composeContent.match(/^\s*image:\s+(.+)$/gm) || [];

  for (const line of imageLines) {
    const ref = line.replace(/^\s*image:\s*/, '').trim();
    if (ref.includes('${')) continue;  // Skip variable-ref images

    const tagMatch = ref.match(/:([^@]+)$/);
    if (tagMatch) {
      const tag = tagMatch[1];
      if (tag === 'latest') {
        issues.push({ category: 'latest-tag', severity: 'low', message: `Image "${ref}" uses :latest tag` });
      } else if (/^\d+\.\d+\.\d+$/.test(tag)) {
        // Pinned semver — good!
      }
    } else {
      // No tag specified — defaults to :latest
      issues.push({ category: 'no-tag', severity: 'medium', message: `Image "${ref}" has no tag specified (defaults to :latest)` });
    }
  }

  return issues;
}

// ── Main audit logic ───────────────────────────────────────────────────

function auditAll() {
  const templateDirs = getTemplateDirs();
  log(`Found ${templateDirs.length} template directories`);

  // Ensure output dir exists
  fs.mkdirSync(outputDir, { recursive: true });

  // Category collectors
  const descriptionIssues = [];
  const upstreamLinkIssues = [];
  const deployConfigIssues = [];
  const tagIssues = [];
  const latestImages = [];  // informational

  let processed = 0;
  let skipped = 0;

  for (const dirName of templateDirs) {
    if (processed >= limit && limit !== Infinity) break;

    const templateDir = path.join(TEMPLATES_DIR, dirName);
    const arcanePath = path.join(templateDir, 'arcane.json');
    const composePath = path.join(templateDir, 'docker-compose.yml');
    const envPath = path.join(templateDir, '.env.example');
    const readmePath = path.join(templateDir, 'README.md');

    const arcane = readJsonSafe(arcanePath);
    if (!arcane || !arcane.id) {
      log(`  SKIP ${dirName}: invalid or missing arcane.json`);
      skipped++;
      continue;
    }

    // Skip non-serviceable templates
    if (isNonServiceable(arcane)) {
      log(`  SKIP ${dirName}: non-serviceable`);
      skipped++;
      continue;
    }

    processed++;
    log(`  [${processed}/${templateDirs.length}] ${dirName}...`);

    const templateId = arcane.id;
    const templateName = arcane.name || dirName;

    // Check 1: Description quality
    const descIssues = checkDescriptionQuality(arcane);
    if (descIssues.length > 0) {
      for (const issue of descIssues) {
        descriptionIssues.push({ templateId, name: templateName, issues: [issue] });
      }
    }

    // Check 2: Upstream links
    const readmeContent = readFileSafe(readmePath);
    const linkIssues = checkUpstreamLinks(dirName, readmeContent);
    if (linkIssues.length > 0) {
      // Group link issues per template
      upstreamLinkIssues.push({ templateId, name: templateName, issues: linkIssues });
    }

    // Check 3: Deploy config
    const configIssues = checkDeployConfig(dirName);
    if (configIssues.length > 0) {
      deployConfigIssues.push({ templateId, name: templateName, issues: configIssues });
    }

    // Check 4: Tag consistency
    const tagIssuesForTemplate = checkTagConsistency(arcane);
    if (tagIssuesForTemplate.length > 0) {
      tagIssues.push({ templateId, name: templateName, issues: tagIssuesForTemplate });
    }

    // Check 5: Image references (informational)
    const composeContent = readFileSafe(composePath);
    const imgIssues = checkImageReferences(composeContent);
    if (imgIssues.length > 0 && imgIssues.some(i => i.category === 'latest-tag' || i.category === 'no-tag')) {
      const latestCount = imgIssues.filter(i => i.category === 'latest-tag').length;
      const noTagCount = imgIssues.filter(i => i.category === 'no-tag').length;
      if (latestCount > 0) {
        latestImages.push({ templateId, name: templateName, latestCount });
      }
    }
  }

  // Sort by severity within each category
  const severityOrder = { high: 0, medium: 1, low: 2 };
  function sortBySeverity(a, b) {
    const aMin = Math.min(...a.issues.map(i => severityOrder[i.severity] || 99));
    const bMin = Math.min(...b.issues.map(i => severityOrder[i.severity] || 99));
    return aMin - bMin;
  }

  descriptionIssues.sort(sortBySeverity);
  upstreamLinkIssues.sort(sortBySeverity);
  deployConfigIssues.sort(sortBySeverity);
  tagIssues.sort(sortBySeverity);

  // Write output files
  const meta = {
    auditedAt: new Date().toISOString(),
    totalTemplates: templateDirs.length,
    processed,
    skipped
  };

  function writeOutput(filename, data) {
    const filePath = path.join(outputDir, filename);
    fs.writeFileSync(filePath, JSON.stringify({ meta, data }, null, 2), 'utf-8');
    log(`  Wrote ${filePath} (${data.length} entries)`);
  }

  writeOutput('description-issues.json', descriptionIssues);
  writeOutput('upstream-link-issues.json', upstreamLinkIssues);
  writeOutput('deploy-config-issues.json', deployConfigIssues);
  writeOutput('tag-issues.json', tagIssues);

  // Write image reference summary
  const imageSummary = {
    meta,
    totalWithLatestImages: latestImages.length,
    entries: latestImages.sort((a, b) => b.latestCount - a.latestCount)
  };
  writeOutput('latest-image-references.json', imageSummary.entries);

  // Print summary
  console.log('\n=== Audit Summary ===');
  console.log(`  Templates scanned:  ${processed}`);
  console.log(`  Non-serviceable skipped: ${skipped}`);
  console.log(`  Description issues: ${descriptionIssues.length} templates`);
  console.log(`  Upstream link issues: ${upstreamLinkIssues.length} templates`);
  console.log(`  Deploy config issues: ${deployConfigIssues.length} templates`);
  console.log(`  Tag issues: ${tagIssues.length} templates`);
  console.log(`  Templates with :latest images: ${latestImages.length}`);
  console.log(`\n  Output directory: ${outputDir}`);
}

// ── Execute ────────────────────────────────────────────────────────────

try {
  auditAll();
} catch (err) {
  console.error('Fatal error during audit:', err);
  process.exit(1);
}
