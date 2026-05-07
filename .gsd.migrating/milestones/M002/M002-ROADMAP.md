# M002: Template Quality & Documentation Audit

**Vision:** Audit and fix content quality across all 842 templates. The registry has grown through automated batch processing but descriptions, tags, upstream links, and deploy configs have degraded. Fix the worst offenders with manual rewrites, clean up the tag taxonomy, verify deploy config consistency, and rebuild the docs site.

## Success Criteria

- Audit script finds zero critical errors across all 842 templates
- Worst-offender READMEs rewritten with real upstream links and accurate config docs
- All 842 templates have appropriate tags from polished taxonomy, zero single-tag entries
- npm run docs:build completes with no errors

## Slices

- [ ] **S01: Build audit tooling and run baseline** `risk:high` `depends:[]`
  > After this: Audit script exists at scripts/audit-templates.js, produces ranked error lists per fix category, and has been run against all 842 templates

- [ ] **S02: Fix deploy config issues** `risk:medium` `depends:[S01]`
  > After this: All port mismatches resolved, env vars consistent between docker-compose.yml and .env.example across all templates

- [ ] **S03: Rewrite worst-offender READMEs** `risk:medium` `depends:[S01]`
  > After this: Worst-offender templates have READMEs with real upstream links, accurate env var documentation, and clear setup steps

- [ ] **S04: Polish tag taxonomy and review all templates** `risk:low` `depends:[S01]`
  > After this: All 842 templates have appropriate tags, zero single-tag entries, clean taxonomy

- [ ] **S05: Rebuild website from updated content** `risk:low` `depends:[S02,S03,S04]`
  > After this: npm run docs:build completes with no errors, site renders updated descriptions and links

## Boundary Map

### S01 → S02, S03, S04
Produces:
  scripts/audit-templates.js → audit script (runnable, outputs ranked error lists)
  audit output (in console/file) → per-category lists of templates needing fixes
Consumes: nothing (leaf node)

### S02 → S05
Produces:
  templates/*/docker-compose.yml → fixed port mappings, consistent env vars
  templates/*/.env.example → defaults matching compose file
Consumes from S01: audit output (deploy config issues list)

### S03 → S05
Produces:
  templates/*/README.md → rewritten with real upstream links, accurate docs
  registry.json → updated content_hash (auto, on next build)
Consumes from S01: audit output (worst-offender list)

### S04 → S05
Produces:
  templates/*/arcane.json → corrected tags
  registry.json → updated templates with clean tags (auto, on next build)
Consumes from S01: audit output (tag issues list)

### S05
Produces:
  docs/ (regenerated) → updated template pages, sidebar, descriptions
  docs/.vitepress/dist/ → built site
Consumes from S02, S03, S04: all file content changes
