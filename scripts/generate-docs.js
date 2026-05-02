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
const DOCS_DIR = path.join(ROOT, 'docs');
const TEMPLATES_DIR = path.join(DOCS_DIR, 'templates');
const CATEGORIES_DIR = path.join(DOCS_DIR, 'categories');

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
  return `<a href="/categories/${slug}" class="tag-badge">${escapeHtml(tag)}</a>`;
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

  // 2. Build tag index: tag -> [{ id, name, description, tags }]
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

  // 6. Generate docs/categories/{tag}.md for each populated tag
  for (const [tag, tagTemplates] of sortedTags) {
    const slug = tagSlug(tag);
    const sorted = [...tagTemplates].sort((a, b) =>
      (a.name || a.id).localeCompare(b.name || b.id)
    );

    let page = `---
title: "${tag}"
description: ${sorted.length} templates tagged with "${tag}"
---

# ${tag}

${sorted.length} templates.

<div class="template-grid">
`;

    for (const t of sorted) {
      const name = escapeHtml(t.name || t.id);
      const desc = escapeHtml(t.description || '');
      const badges = (t.tags || []).map(badgeHtml).join(' ');
      page += `
<div class="template-card">

### [${name}](/templates/${t.id})

${desc}

${badges}

</div>
`;
    }

    page += `</div>\n`;
    fs.writeFileSync(path.join(CATEGORIES_DIR, `${slug}.md`), page, 'utf-8');
  }
  console.log(`Wrote ${sortedTags.length} category pages`);

  // 7. Generate docs/templates/{id}.md for each template — detail page
  for (const t of templates) {
    const name = escapeHtml(t.name || t.id);
    const desc = escapeHtml(t.description || '');
    const badges = (t.tags || []).map(badgeHtml).join(' ');

    let links = '';
    if (t.compose_url) {
      links += `- [docker-compose.yml](${t.compose_url})\n`;
    }
    if (t.env_url) {
      links += `- [.env.example](${t.env_url})\n`;
    }
    if (t.documentation_url) {
      links += `- [Documentation](${t.documentation_url})\n`;
    }

    const page = `---
title: "${name}"
description: "${desc}"
---

# ${name}

${desc}

## Tags

${badges || 'No tags'}

## Links

${links || 'No links available'}

## Metadata

| Field | Value |
|-------|-------|
| ID | \`${t.id}\` |
| Version | ${t.version || 'N/A'} |
| Author | ${t.author || 'N/A'} |
| Content Hash | \`${t.content_hash || 'N/A'}\` |
`;

    fs.writeFileSync(path.join(TEMPLATES_DIR, `${t.id}.md`), page, 'utf-8');
  }
  console.log(`Wrote ${templates.length} template detail pages`);

  // 8. Update VitePress sidebar config dynamically
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
