#!/usr/bin/env node
/**
 * fix-tags.js — Batch tag-correction script for single-tag templates
 *
 * Reads scripts/audit-output/tag-issues.json, identifies all single-tag
 * entries (22 templates), and adds 1-3 appropriate additional tags to
 * each template's arcane.json file.
 *
 * Usage:
 *   node scripts/fix-tags.js            # apply corrections
 *   node scripts/fix-tags.js --dry-run  # print planned corrections only
 *
 * Exit code: 0 on success, non-zero on error
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ── Paths ──────────────────────────────────────────────────────────────

const ROOT = path.resolve(__dirname, '..');
const ISSUES_FILE = path.join(__dirname, 'audit-output', 'tag-issues.json');

// ── Tag correction map ─────────────────────────────────────────────────
// Maps templateId to array of additional tags (from the existing 52-tag taxonomy)
// Derived from the task plan specification.

const CORRECTIONS = {
  'chatwoot':         ['communication'],
  'cog':              ['devops', 'tools'],
  'docker-ipsec-vpn': ['infrastructure', 'tools'],
  'grype':            ['devops', 'tools'],
  'insforge':         ['tools', 'media'],
  'joern':            ['tools', 'research'],
  'matrix-server':    ['communication', 'infrastructure'],
  'mirotalksfu':      ['communication', 'tools'],
  'mlflow':           ['tools', 'workflow'],
  'nginx-ui':         ['proxy', 'web'],
  'ory-hydra':        ['authentication', 'identity', 'api'],
  'redink':           ['tools'],
  'sftpgo':           ['tools', 'security'],
  'streamer-sales':   ['e-commerce', 'automation'],
  'suna':             ['tools', 'automation'],
  'test-app':         ['tools'],
  'tpotce':           ['monitoring', 'infrastructure'],
  'trendradar':       ['analytics', 'monitoring'],
  'trivy':            ['devops', 'tools'],
  'ufw-docker':       ['infrastructure', 'tools'],
  'wgcloud':          ['devops', 'infrastructure'],
  'xiaomusic':        ['ai', 'automation', 'entertainment'],
};

// ── Helpers ────────────────────────────────────────────────────────────

function loadJSON(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch (err) {
    console.error(`ERROR: Could not read or parse "${filePath}": ${err.message}`);
    process.exit(1);
  }
}

/**
 * Deduplicate tags: return tags from `addTags` that are not already in `existingTags`.
 * Comparison is case-insensitive but the added tags use the taxonomy casing.
 */
function deduplicateTags(existingTags, addTags) {
  const existingLower = (existingTags || []).map(t => t.toLowerCase());
  return addTags.filter(t => !existingLower.includes(t.toLowerCase()));
}

/**
 * Load a template's arcane.json, add tags, and write back.
 * Returns { templateId, name, oldTags, newTags } for the summary.
 */
function fixTemplate(templateId, addTags, isDryRun) {
  const templateDir = path.join(ROOT, 'templates', templateId);
  const arcanePath = path.join(templateDir, 'arcane.json');

  if (!fs.existsSync(arcanePath)) {
    console.error(`ERROR: arcane.json not found at "${arcanePath}"`);
    process.exit(1);
  }

  let arcane;
  try {
    arcane = JSON.parse(fs.readFileSync(arcanePath, 'utf-8'));
  } catch (err) {
    console.error(`ERROR: Malformed arcane.json at "${arcanePath}": ${err.message}`);
    process.exit(1);
  }

  const oldTags = Array.isArray(arcane.tags) ? [...arcane.tags] : [];
  const newTagsToAdd = deduplicateTags(oldTags, addTags);

  if (newTagsToAdd.length === 0) {
    return { templateId, name: arcane.name || templateId, oldTags, newTags: oldTags, unchanged: true };
  }

  if (!isDryRun) {
    arcane.tags = [...oldTags, ...newTagsToAdd];
    fs.writeFileSync(arcanePath, JSON.stringify(arcane, null, 2) + '\n', 'utf-8');
  }

  return {
    templateId,
    name: arcane.name || templateId,
    oldTags,
    newTags: [...oldTags, ...newTagsToAdd],
    added: newTagsToAdd,
    unchanged: false,
  };
}

// ── Main ───────────────────────────────────────────────────────────────

function main() {
  const isDryRun = process.argv.includes('--dry-run');

  if (isDryRun) {
    console.log('[DRY RUN] No files will be modified.\n');
  } else {
    console.log('Applying tag corrections...\n');
  }

  const issues = loadJSON(ISSUES_FILE);
  const data = issues.data || [];

  // Filter for single-tag entries only
  const singleTagEntries = data.filter(item =>
    item.issues && item.issues.some(i => i.category === 'single-tag')
  );

  if (singleTagEntries.length === 0) {
    console.log('No single-tag entries found. Nothing to fix.');
    process.exit(0);
  }

  console.log(`Found ${singleTagEntries.length} single-tag template(s) to fix.\n`);

  let fixedCount = 0;
  let unchangedCount = 0;
  const results = [];

  for (const entry of singleTagEntries) {
    const tid = entry.templateId;
    const addTags = CORRECTIONS[tid];

    if (!addTags) {
      console.warn(`  ⚠ No correction mapping for "${tid}" (${entry.name}). Skipping.`);
      continue;
    }

    const result = fixTemplate(tid, addTags, isDryRun);
    results.push(result);

    if (result.unchanged) {
      unchangedCount++;
      const existingTag = result.oldTags[0] || '(none)';
      console.log(`  ${isDryRun ? '  ' : '✓'} ${result.name.padEnd(35)} [${existingTag}] — already has all suggested tags, no change needed`);
    } else {
      fixedCount++;
      const oldStr = result.oldTags.join(', ');
      const newStr = result.newTags.join(', ');
      const addedStr = result.added.join(', ');
      console.log(`  ${isDryRun ? '  ' : '✓'} ${result.name.padEnd(35)} [${oldStr}] → [${newStr}]  (+${addedStr})`);
    }
  }

  // Summary
  console.log('');
  if (isDryRun) {
    console.log(`[DRY RUN] Would fix ${fixedCount} template(s) (${unchangedCount} already up-to-date).`);
  } else {
    console.log(`Applied ${fixedCount} tag correction(s). (${unchangedCount} already up-to-date.)`);
  }

  process.exit(0);
}

main();
