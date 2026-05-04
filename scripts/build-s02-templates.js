#!/usr/bin/env node
/**
 * build-s02-templates.js — Create Arcane templates from S02 fact cards
 *
 * Reads fact-cards-s02.json, creates template directories with all 4
 * required files for each reachable candidate. Generalized version of
 * build-m012-templates.js with source-aware tag inference, well-known
 * port lookup, build-log output, and dedup suffix handling.
 *
 * Usage: node scripts/build-s02-templates.js
 */

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const FC_PATH = path.join(ROOT, 'fact-cards-s02.json');
const TEMPLATES_DIR = path.join(ROOT, 'templates');
const LOG_PATH = path.join(ROOT, 'build-log-s02.json');

// ── Helpers ────────────────────────────────────────────────────────────

function slugify(name) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function findReachableImage(card) {
  const images = card.images_checked || [];
  for (const img of images) {
    if (img.reachable) return img;
  }
  return null;
}

// ── Port Inference ─────────────────────────────────────────────────────
// Well-known default ports for S02 candidates. These are documented
// default ports from each project's official documentation, Docker
// image labels, and YunoHost/Portainer app manifests.

const WELL_KNOWN_PORTS = {
  'abantecart': 80,
  'invoice-ninja': 80,
  'satsale': 5000,
  'our-shopping-list': 80,
  'snipeit': 80,
  'nodered': 1880,
  'motioneye': 8765,
  'focalboard': 8000,
  'overleaf': 80,
  'itflow': 80,
  'easyappointments': 80,
  'koel': 80,
  'stremio': 11470,
  'node-exporter': 9100,
  'influxdb-v2': 8086,
  'mongo-express': 8081,
  'elasticsearch7': 9200,
  'rocketchat': 3000,
  'dendrite': 8008,
  'cockpit': 80,
  'funkwhale': 80,
};

function pickPort(card) {
  const slug = slugify(card.candidate);
  return WELL_KNOWN_PORTS[slug] || 8080;
}

// ── Tag Inference ──────────────────────────────────────────────────────

function pickTags(card) {
  const name = card.candidate.toLowerCase();
  const slug = slugify(name);
  const tags = [];

  // Category tags inferred from name keywords
  if (/shop|cart|commerce|invoice|sale|itflow|easyappointment|snipeit/i.test(name)) {
    tags.push('business', 'e-commerce');
  }
  if (/node.?red|automation|home.?assist|motion/i.test(name)) {
    tags.push('automation', 'iot');
  }
  if (/motion|eye|camera|stream/i.test(name)) {
    tags.push('media', 'monitoring');
  }
  if (/monitor|export|influx|elastic|mongo.?express|grafana/i.test(name)) {
    tags.push('monitoring', 'database');
  }
  if (/rocket|chat|dendrite|matrix|element|cockpit/i.test(name)) {
    tags.push('communication', 'productivity');
  }
  if (/music|audio|koel|funkwhale|stremio/i.test(name)) {
    tags.push('media', 'entertainment');
  }
  if (/note|board|overleaf|focal/i.test(name)) {
    tags.push('productivity', 'collaboration');
  }

  // Source-aware tags
  if (card.source === 'yunohost') {
    if (!tags.some(t => t === 'self-hosted')) tags.push('self-hosted');
  }
  if (card.source === 'umbrel') {
    tags.push('self-hosted', 'bitcoin');
  }
  if (card.source === 'awesome-selfhosted') {
    tags.push('self-hosted');
  }
  if (card.source === 'portainer') {
    if (!tags.some(t => t === 'self-hosted')) tags.push('self-hosted');
  }

  // Fallback — minimum 2 tags
  if (tags.length === 0) tags.push('self-hosted', 'tools');
  if (tags.length === 1) tags.push('tools');

  // Deduplicate and cap at 8
  const unique = [...new Set(tags)];
  return unique.slice(0, 8);
}

// ── File Builders ─────────────────────────────────────────────────────

function buildArcaneJson(card, slug) {
  return {
    id: slug,
    name: card.candidate,
    description: `${card.candidate} — self-hosted via Docker Compose`,
    version: '1.0.0',
    author: 'Arcane',
    tags: pickTags(card),
  };
}

function buildCompose(slug, imageRef, port) {
  const envVarName = slug.toUpperCase().replace(/-/g, '_') + '_PORT';
  const lines = [
    'version: \'3.8\'',
    '',
    'services:',
    `  ${slug}:`,
    `    image: ${imageRef}`,
    `    container_name: ${slug}`,
    `    hostname: ${slug}`,
    `    ports:`,
    `      - "\${${envVarName}:-${port}}:${port}"`,
    `    restart: unless-stopped`,
    `    volumes:`,
    `      - ${slug}_data:/data`,
    '',
    'volumes:',
    `  ${slug}_data:`,
    `    name: ${slug}_data`,
  ];
  return lines.join('\n') + '\n';
}

function buildEnvExample(card, slug, port) {
  const envVarName = slug.toUpperCase().replace(/-/g, '_') + '_PORT';
  const lines = [
    `# ── ${card.candidate} Configuration ──`,
    '# Copy this file to .env and adjust values as needed.',
    '',
    `# Host port (default: ${port})`,
    `${envVarName}=${port}`,
  ];
  return lines.join('\n') + '\n';
}

function buildReadme(card, slug, port) {
  const upstreamLink = card.github_url || '';
  return [
    `# ${card.candidate}`,
    '',
    `[${card.candidate}](${upstreamLink}) — self-hosted via Docker Compose.`,
    '',
    '## Quick Start',
    '',
    '1. Copy the environment file and adjust as needed:',
    '',
    '   ```bash',
    '   cp .env.example .env',
    '   ```',
    '',
    '2. Start the service:',
    '',
    '   ```bash',
    '   docker compose up -d',
    '   ```',
    '',
    '3. Access the service:',
    '',
    `   Open [http://localhost:${port}](http://localhost:${port}) in your browser.`,
    '',
    '## Configuration',
    '',
    'Edit `.env` to customize the port and other settings. See `.env.example` for available options.',
    '',
    '## Upstream',
    '',
    `- [GitHub](${upstreamLink})`,
    '',
  ].join('\n');
}

// ── Dedup Suffix ───────────────────────────────────────────────────────

function resolveSlug(card) {
  const base = slugify(card.candidate);
  const dir = path.join(TEMPLATES_DIR, base);

  if (fs.existsSync(dir)) {
    // Append source suffix for disambiguation
    const sourceMap = {
      'yunohost': 'yunohost',
      'portainer': 'portainer',
      'umbrel': 'umbrel',
      'awesome-selfhosted': 'awesome',
    };
    const suffix = sourceMap[card.source] || 'other';
    const dedupSlug = `${base}-${suffix}`;
    const dedupDir = path.join(TEMPLATES_DIR, dedupSlug);
    if (fs.existsSync(dedupDir)) {
      // Even dedup slug exists — append index
      let i = 2;
      while (fs.existsSync(path.join(TEMPLATES_DIR, `${dedupSlug}-${i}`))) i++;
      return `${dedupSlug}-${i}`;
    }
    return dedupSlug;
  }

  return base;
}

// ── Main ───────────────────────────────────────────────────────────────

function main() {
  // Validate input
  if (!fs.existsSync(FC_PATH)) {
    console.error(`ERROR: fact-cards-s02.json not found at ${FC_PATH}`);
    process.exit(1);
  }

  let cards;
  try {
    const raw = fs.readFileSync(FC_PATH, 'utf8');
    cards = JSON.parse(raw);
  } catch (err) {
    console.error(`ERROR: Invalid fact-cards JSON — ${err.message}`);
    process.exit(1);
  }

  if (!Array.isArray(cards)) {
    console.error('ERROR: fact-cards-s02.json must contain an array');
    process.exit(1);
  }

  // Filter reachable
  const reachable = cards.filter(c => {
    const img = findReachableImage(c);
    return img !== null;
  });

  const buildLog = [];

  console.log(`Processing ${reachable.length} reachable candidates (${cards.length} total)...`);
  console.log('');

  let created = 0;
  let skipped = 0;
  let errors = 0;

  for (const card of reachable) {
    const slug = resolveSlug(card);
    const img = findReachableImage(card);
    const imageRef = card.recommend_image || img.image;
    const port = pickPort(card);
    const dir = path.join(TEMPLATES_DIR, slug);

    // Check if dir already exists (after dedup resolution)
    if (fs.existsSync(dir)) {
      console.log(`  SKIP: ${slug} — dir already exists`);
      buildLog.push({
        slug,
        status: 'skipped',
        image: imageRef,
        port,
        source: card.source,
        candidate: card.candidate,
        error_message: 'already-exists',
      });
      skipped++;
      continue;
    }

    try {
      fs.mkdirSync(dir, { recursive: true });

      const arcaneJson = buildArcaneJson(card, slug);
      fs.writeFileSync(path.join(dir, 'arcane.json'), JSON.stringify(arcaneJson, null, 2) + '\n', 'utf8');

      const compose = buildCompose(slug, imageRef, port);
      fs.writeFileSync(path.join(dir, 'docker-compose.yml'), compose, 'utf8');

      const envExample = buildEnvExample(card, slug, port);
      fs.writeFileSync(path.join(dir, '.env.example'), envExample, 'utf8');

      const readme = buildReadme(card, slug, port);
      fs.writeFileSync(path.join(dir, 'README.md'), readme, 'utf8');

      console.log(`  OK: ${slug} — ${imageRef} :${port}`);
      buildLog.push({
        slug,
        status: 'created',
        image: imageRef,
        port,
        source: card.source,
        candidate: card.candidate,
        error_message: '',
      });
      created++;
    } catch (err) {
      console.error(`  ERR: ${slug} — ${err.message}`);
      buildLog.push({
        slug,
        status: 'error',
        image: imageRef,
        port,
        source: card.source,
        candidate: card.candidate,
        error_message: err.message,
      });
      errors++;
    }
  }

  // Write build log
  fs.writeFileSync(LOG_PATH, JSON.stringify(buildLog, null, 2) + '\n', 'utf8');

  console.log('');
  console.log(`Created: ${created} | Skipped: ${skipped} | Errors: ${errors}`);
  console.log(`Build log written to build-log-s02.json`);
}

main();
