#!/usr/bin/env node
/**
 * build-m012-templates.js — Create Arcane templates from M012 fact cards
 *
 * Reads fact-cards-m012.json (from T02-T03), creates template directories
 * with all 4 required files for each reachable candidate.
 *
 * Usage: node scripts/build-m012-templates.js
 */

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const FC_PATH = path.join(ROOT, 'fact-cards-m012.json');
const TEMPLATES_DIR = path.join(ROOT, 'templates');

// ── Helpers ────────────────────────────────────────────────────────────

function slugify(name) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function findReachableImage(card) {
  for (const img of (card.images_checked || [])) {
    if (img.reachable) return img;
  }
  return null;
}

function pickPort(card, img) {
  // Known ports from M012 candidates
  const knownPorts = {
    'auto-gpt': 8000,
    'comfyui': 8188,
    'screenshot-to-code': 3000,
    'open-interpreter': 8080,
    'qdrant': 6333,
    'crewai': 8080,
    'llamaindex': 8080,
    'aider': 8080,
    'promptfoo': 15500,
    'continue': 8080,
    'composio': 8080,
    'haystack': 8000,
    'letta': 8283,
    'swe-agent': 8080,
    'text-generation-inference': 8080,
    'diffsynth-studio': 7860,
    'traefik': 8080,
    'vault': 8200,
    'sysdig': 8080,
    'nginx-proxy-manager': 81,
    'consul': 8500,
    'pulumi': 8080,
    'frp': 7000,
    'ansible-semaphore': 3000,
    'netmaker': 8080,
    'firezone': 9443,
    'keycloak': 8080,
    'supertokens': 3567,
    'zitadel': 8080,
    'logto': 3001,
    'ory-kratos': 4433,
    'hanko': 8000,
    'casdoor': 8000,
    'ory-oathkeeper': 4456,
    'lemonldap-ng': 80,
  };
  const slug = slugify(card.candidate);
  return knownPorts[slug] || 8080;
}

function pickTags(card) {
  const name = card.candidate.toLowerCase();
  const tags = [];
  // AI/LLM indicators
  if (/ai|llm|gpt|model|inference|agent|lang|prompt|rag|embed/i.test(name)) {
    tags.push('ai', 'llm');
  } else if (/llamaindex|crewai|haystack|langchain/i.test(slugify(name))) {
    tags.push('ai', 'llm');
  }
  // DevOps indicators
  if (/proxy|traefik|vault|consul|pulumi|terraform|ansible|kubernetes|container|docker|ci|cd|pipeline|sysdig|frp|netmaker|firezone/i.test(name)) {
    tags.push('devops', 'infrastructure');
  }
  // Identity indicators
  if (/keycloak|supertokens|zitadel|logto|kratos|hanko|casdoor|oathkeeper|lemonldap|auth|sso|identity/i.test(name)) {
    tags.push('identity', 'authentication');
  }
  if (tags.length === 0) tags.push('self-hosted', 'tools');
  return tags;
}

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

function buildCompose(card, slug, imageRef, port) {
  const envVarName = slug.toUpperCase().replace(/-/g, '_') + '_PORT';
  const lines = ['version: \'3.8\'', '', 'services:'];
  lines.push(`  ${slug}:`);
  lines.push(`    image: ${imageRef}`);
  lines.push(`    container_name: ${slug}`);
  lines.push(`    hostname: ${slug}`);
  lines.push(`    ports:`);
  lines.push(`      - "\${${envVarName}:-${port}}:${port}"`);
  lines.push(`    restart: unless-stopped`);

  // Named volume for data
  if (!/traefik|frp|sysdig|ctop/i.test(card.candidate)) {
    lines.push(`    volumes:`);
    lines.push(`      - ${slug}_data:/data`);
  }

  lines.push('');
  lines.push('volumes:');
  lines.push(`  ${slug}_data:`);
  lines.push(`    name: ${slug}_data`);

  return lines.join('\n') + '\n';
}

function buildEnvExample(card, slug, port) {
  const envVarName = slug.toUpperCase().replace(/-/g, '_') + '_PORT';
  const lines = [`# ── ${card.candidate} Configuration ──`, '# Copy this file to .env and adjust values as needed.', ''];
  lines.push(`# Host port (default: ${port})`);
  lines.push(`${envVarName}=${port}`);
  return lines.join('\n') + '\n';
}

function buildReadme(card, slug, port) {
  return `# ${card.candidate}

[${card.candidate}](${card.github_url}) — self-hosted via Docker Compose.

## Quick Start

1. Copy the environment file and adjust as needed:

   \`\`\`bash
   cp .env.example .env
   \`\`\`

2. Start the service:

   \`\`\`bash
   docker compose up -d
   \`\`\`

3. Access the service:

   Open [http://localhost:${port}](http://localhost:${port}) in your browser.

## Configuration

Edit \`.env\` to customize port and other settings. See \`.env.example\` for available options.

## Upstream

- [GitHub](${card.github_url})
`;
}

// ── Main ───────────────────────────────────────────────────────────────

const raw = fs.readFileSync(FC_PATH, 'utf8');
const cards = JSON.parse(raw);

const reachable = cards.filter(c => {
  const img = findReachableImage(c);
  return img !== null;
});

console.log(`Processing ${reachable.length} reachable candidates...`);

let created = 0;
let skipped = 0;
const errors = [];

for (const card of reachable) {
  const slug = slugify(card.candidate);
  const img = findReachableImage(card);
  const imageRef = card.recommend_image || img.image;
  const port = pickPort(card, img);

  const dir = path.join(TEMPLATES_DIR, slug);

  if (fs.existsSync(dir)) {
    console.log(`  SKIP: ${slug} — dir already exists`);
    skipped++;
    continue;
  }

  try {
    fs.mkdirSync(dir, { recursive: true });

    const arcaneJson = buildArcaneJson(card, slug);
    fs.writeFileSync(path.join(dir, 'arcane.json'), JSON.stringify(arcaneJson, null, 2) + '\n', 'utf8');

    const compose = buildCompose(card, slug, imageRef, port);
    fs.writeFileSync(path.join(dir, 'docker-compose.yml'), compose, 'utf8');

    const envExample = buildEnvExample(card, slug, port);
    fs.writeFileSync(path.join(dir, '.env.example'), envExample, 'utf8');

    const readme = buildReadme(card, slug, port);
    fs.writeFileSync(path.join(dir, 'README.md'), readme, 'utf8');

    console.log(`  OK: ${slug} — ${imageRef} :${port}`);
    created++;
  } catch (err) {
    console.error(`  ERR: ${slug} — ${err.message}`);
    errors.push({ slug, error: err.message });
  }
}

console.log(`\nCreated: ${created} | Skipped: ${skipped} | Errors: ${errors.length}`);
if (errors.length) {
  console.log('\nErrors:');
  errors.forEach(e => console.log(`  ${e.slug}: ${e.error}`));
}
