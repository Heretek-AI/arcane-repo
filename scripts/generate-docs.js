#!/usr/bin/env node
/**
 * generate-docs.js
 * Reads registry.json and generates VitePress markdown pages:
 *   - docs/templates/index.md          (alphabetical listing)
 *   - docs/templates/{id}.md           (per-template detail)
 *   - docs/categories/index.md         (category overview)
 *   - docs/categories/{tag}.md         (per-category listing)
 *
 * Follows D004: Node.js for CI scripting.
 * Single-pass read, batch write for 785+ templates.
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const REGISTRY_PATH = path.join(ROOT, 'registry.json');
const TEMPLATES_SRC = path.join(ROOT, 'templates');
const DOCS_DIR = path.join(ROOT, 'docs');
const TEMPLATES_DIR = path.join(DOCS_DIR, 'templates');
const CATEGORIES_DIR = path.join(DOCS_DIR, 'categories');
const DATA_DIR = path.join(DOCS_DIR, '.vitepress', 'data');

// --- Helpers ---

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function tagSlug(tag) {
  return tag.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function badgeHtml(tag) {
  const slug = tagSlug(tag);
  return `<a href="/arcane-repo/categories/${slug}.html" class="tag-badge">${escapeHtml(tag)}</a>`;
}

// Section name → camelCase key mapping (exact match and prefix match for variants)
const SECTION_MAP = {
  'Project Overview': 'projectOverview',
  'Architecture': 'architecture',
  'Quick Start': 'quickStart',
  'Configuration': 'configuration',
  'Troubleshooting': 'troubleshooting',
  'Links': 'links',
  'Backup & Recovery': 'backup',
  'Prerequisites': 'prerequisites',
  'API Endpoints': 'apiEndpoints',
  'Service Details': 'serviceDetails',
  'Health Check': 'healthCheck',
  'Upstream': 'upstream',
};

/**
 * Resolve a section header to its camelCase key.
 * Tries exact match first, then prefix match for variants like "Quick Start (Headless)".
 */
function resolveSectionKey(sectionName) {
  if (SECTION_MAP[sectionName]) return SECTION_MAP[sectionName];
  // Prefix match: find the longest matching key
  for (const [name, key] of Object.entries(SECTION_MAP)) {
    if (sectionName.startsWith(name + ' ') || sectionName.startsWith(name + '(')) {
      return key;
    }
  }
  return null;
}

/**
 * Parse a README.md into structured sections.
 * Returns { title, intro, sections: { key: markdownString, ... } }
 * Missing sections are omitted (not empty strings).
 */
function parseReadme(readmePath) {
  if (!fs.existsSync(readmePath)) return null;
  const content = fs.readFileSync(readmePath, 'utf-8');
  const lines = content.split('\n');

  let title = '';
  let introLines = [];
  const sections = {};
  let currentKey = null;
  let currentLines = [];
  let inCodeBlock = false;
  let firstHeadingSeen = false;

  for (const line of lines) {
    // Track code fences so we don't split inside them
    if (line.trimStart().startsWith('```')) {
      inCodeBlock = !inCodeBlock;
    }

    // Detect ## headers (but not inside code blocks)
    if (!inCodeBlock && line.startsWith('## ')) {
      // Flush previous section
      if (currentKey !== null) {
        const text = currentLines.join('\n').trim();
        if (text) sections[currentKey] = text;
      } else if (!firstHeadingSeen) {
        // We were collecting intro before the first ## header
        // (title is the # heading, intro is everything between title and first ##)
      }

      const sectionName = line.slice(3).trim();
      currentKey = resolveSectionKey(sectionName); // null = skip unknown sections
      currentLines = [];
      firstHeadingSeen = true;
      continue;
    }

    // Detect # title (only the first one)
    if (!firstHeadingSeen && line.startsWith('# ') && !line.startsWith('## ')) {
      title = line.slice(2).trim();
      continue;
    }

    // Accumulate lines into current section or intro
    if (currentKey !== null) {
      currentLines.push(line);
    } else if (firstHeadingSeen) {
      // Between first # and first ## — ignore (usually empty)
    } else {
      introLines.push(line);
    }
  }

  // Flush last section
  if (currentKey !== null) {
    const text = currentLines.join('\n').trim();
    if (text) sections[currentKey] = text;
  }

  const intro = introLines.join('\n').trim();

  return { title, intro, sections };
}

// --- Main ---

function main() {
  // 1. Read registry
  const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf-8'));
  const templates = registry.templates;

  if (!templates || !templates.length) {
    console.error('ERROR: registry.json contains no templates');
    process.exit(1);
  }

  console.log(`Loaded ${templates.length} templates from registry.json`);

  // 2. Parse all READMEs and build enriched data
  const templatesData = [];
  let parsedCount = 0;
  let sectionStats = {};

  for (const t of templates) {
    const readmePath = path.join(TEMPLATES_SRC, t.id, 'README.md');
    const parsed = parseReadme(readmePath);

    const entry = {
      id: t.id,
      name: t.name || t.id,
      description: t.description || '',
      version: t.version || '',
      author: t.author || '',
      compose_url: t.compose_url || '',
      env_url: t.env_url || '',
      documentation_url: t.documentation_url || '',
      content_hash: t.content_hash || '',
      tags: t.tags || [],
      sections: parsed ? parsed.sections : {},
      intro: parsed ? parsed.intro : '',
    };

    templatesData.push(entry);

    if (parsed) {
      parsedCount++;
      for (const key of Object.keys(parsed.sections)) {
        sectionStats[key] = (sectionStats[key] || 0) + 1;
      }
    }
  }

  console.log(`Parsed ${parsedCount} READMEs`);
  console.log('Section counts:', JSON.stringify(sectionStats, null, 2));

  // 3. Write templates.data.json
  ensureDir(DATA_DIR);
  const dataPath = path.join(DATA_DIR, 'templates.data.json');
  fs.writeFileSync(dataPath, JSON.stringify(templatesData, null, 2), 'utf-8');
  console.log(`Wrote ${dataPath} (${templatesData.length} templates)`);

  // 4. Build tag index: tag -> [{ id, name, description, tags }]
  const tagMap = new Map();
  for (const t of templates) {
    for (const tag of (t.tags || [])) {
      if (!tagMap.has(tag)) tagMap.set(tag, []);
      tagMap.get(tag).push(t);
    }
  }

  // Sort tags by count descending
  const sortedTags = [...tagMap.entries()].sort((a, b) => b[1].length - a[1].length);

  console.log(`Found ${sortedTags.length} unique tags`);

  // 3. Ensure output directories
  ensureDir(TEMPLATES_DIR);
  ensureDir(CATEGORIES_DIR);

  // 4. Generate docs/templates/index.md — alphabetical listing
  const sortedTemplates = [...templates].sort((a, b) =>
    (a.name || a.id).localeCompare(b.name || b.id)
  );

  let templatesIndex = `---
title: All Templates
description: Browse all ${templates.length} templates in the Arcane registry
---

# All Templates

${templates.length} templates in the registry. Use \`Ctrl+K\` to search.

<div class="template-grid">
`;

  for (const t of sortedTemplates) {
    const name = escapeHtml(t.name || t.id);
    const desc = escapeHtml(t.description || '');
    const badges = (t.tags || []).map(badgeHtml).join(' ');
    templatesIndex += `
<div class="template-card">

### [${name}](/templates/${t.id})

${desc}

${badges}

</div>
`;
  }

  templatesIndex += `</div>\n`;
  fs.writeFileSync(path.join(TEMPLATES_DIR, 'index.md'), templatesIndex, 'utf-8');
  console.log(`Wrote templates/index.md (${sortedTemplates.length} entries)`);

  // 5. Generate docs/categories/index.md — category overview
  let categoriesIndex = `---
title: Categories
description: Browse templates by category
---

# Categories

${sortedTags.length} categories covering ${templates.length} templates.

<div class="category-grid">
`;

  for (const [tag, tagTemplates] of sortedTags) {
    const slug = tagSlug(tag);
    categoriesIndex += `
<div class="category-card">

<div class="count">${tagTemplates.length}</div>

<div class="label">[${tag}](/categories/${slug})</div>

</div>
`;
  }

  categoriesIndex += `</div>\n`;
  fs.writeFileSync(path.join(CATEGORIES_DIR, 'index.md'), categoriesIndex, 'utf-8');
  console.log(`Wrote categories/index.md (${sortedTags.length} categories)`);

  // 6. Generate docs/categories/{tag}.md for each populated tag — frontmatter-only (dynamic CategoryView)
  for (const [tag, tagTemplates] of sortedTags) {
    const slug = tagSlug(tag);

    let page = `---
layout: category
category: ${tag}
title: "${tag}"
description: "${tagTemplates.length} templates tagged with \\"${tag}\\""
---
`;
    fs.writeFileSync(path.join(CATEGORIES_DIR, `${slug}.md`), page, 'utf-8');
  }
  console.log(`Wrote ${sortedTags.length} category pages (frontmatter-only)`);

  // 8. Generate docs/templates/{id}.md for each template — custom layout detail page
  for (const t of templates) {
    const name = escapeHtml(t.name || t.id);
    const desc = escapeHtml(t.description || '');

    const page = `---
title: "${name}"
description: "${desc}"
layout: template-detail
templateId: "${t.id}"
---
`;

    fs.writeFileSync(path.join(TEMPLATES_DIR, `${t.id}.md`), page, 'utf-8');
  }
  console.log(`Wrote ${templates.length} template detail pages (custom layout)`);

  // 9. Update VitePress sidebar config dynamically
  //    Build sidebar items for categories
  const categorySidebarItems = sortedTags.map(([tag]) => ({
    text: `${tag} (${tagMap.get(tag).length})`,
    link: `/categories/${tagSlug(tag)}`
  }));

  // Read current config and inject sidebar
  const configPath = path.join(DOCS_DIR, '.vitepress', 'config.mts');
  let configContent = fs.readFileSync(configPath, 'utf-8');

  // Replace the categories sidebar items
  const sidebarMarker = '// CATEGORIES_SIDEBAR_START';
  const sidebarEndMarker = '// CATEGORIES_SIDEBAR_END';

  const sidebarBlock = `${sidebarMarker}
        {
          text: 'Categories',
          items: [
            { text: 'Overview', link: '/categories/' },
${categorySidebarItems.map(item => `            { text: '${item.text.replace(/'/g, "\\'")}', link: '${item.link}' }`).join(',\n')}
          ]
        }
      ${sidebarEndMarker}`;

  if (configContent.includes(sidebarMarker)) {
    configContent = configContent.replace(
      new RegExp(`${sidebarMarker}[\\s\\S]*?${sidebarEndMarker}`),
      sidebarBlock
    );
  } else {
    // Inject markers around the categories sidebar section
    configContent = configContent.replace(
      `'/categories/': [
        {
          text: 'Categories',
          items: [
            { text: 'Overview', link: '/categories/' }
          ]
        }
      ]`,
      `'/categories/': [
      ${sidebarBlock}
      ]`
    );
  }

  fs.writeFileSync(configPath, configContent, 'utf-8');
  console.log('Updated VitePress sidebar config');

  console.log('\nDone! Run `npm run docs:build` in docs/ to build the site.');
}

main();
