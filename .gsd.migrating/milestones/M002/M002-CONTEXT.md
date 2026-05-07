---
---

# M002: Template Quality & Documentation Audit

**Gathered:** 2026-05-07
**Status:** Ready for planning

## Project Description

Audit and fix content quality across the 842-template Arcane template registry. The site was recently fixed (`.html` extensions, base path) but many template descriptions are generic placeholders ("X — self-hosted via Docker Compose"), upstream links are missing, tags are inconsistently applied, and deploy configs (docker-compose.yml + .env.example) may have port mismatches or stale variables.

## Why This Milestone

The registry has grown to 842 templates through automated batch processing, but content quality hasn't kept pace. 688 of 842 descriptions are generic. Tags are inconsistently applied across 52 categories. READMEs follow a template structure but many have placeholder upstream links and generic setup sections. Without this fix, browsing and deploying from the site is a poor experience — users hit 404s on upstream links, get generic descriptions that don't help them choose, and may find broken configs when they try to deploy.

## User-Visible Outcome

### When this milestone is complete, the user can:

- Browse the site and see accurate descriptions and upstream project links on every template page
- Filter by tags and find consistently-categorized results
- Clone a template, check the README, and find real setup guidance with correct env vars and port values
- Run the audit script themselves to verify template quality

### Entry point / environment

- Entry point: GitHub Pages site at `/arcane-repo/browse.html`, then click any template
- Environment: Static site, templates/ directory on disk
- Live dependencies involved: none (static audit)

## Completion Class

- Contract complete means: Audit script detects no critical issues (missing upstream links, port mismatches, single-tag templates), worst-offender READMEs rewritten, tags consistently applied, site builds clean
- Integration complete means: Site content matches disk content, tag filters produce correct results
- Operational complete means: none (no live system)

## Final Integrated Acceptance

To call this milestone complete, we must prove:

- Audit script passes with zero critical errors (missing upstream links, port mismatches)
- Site rebuilds cleanly after all content changes
- Tag count per template averages ≥2 (eliminates single-tag cases)

## Scope

### In Scope

- Build a Node.js audit script that checks all 842 templates for: missing upstream links, generic descriptions, port mismatches between docker-compose.yml and .env.example, missing env vars, stale image tags, single-tag entries
- Fix deploy config issues identified by the audit (port mismatches, missing vars)
- Manually rewrite READMEs for the worst ~150-200 templates (generic descriptions, missing upstream links)
- Polish the 52-category tag taxonomy (merge duplicates, fix miscategorized templates)
- Manually review and fix tags on all 842 templates
- Rebuild the VitePress docs site

### Out of Scope / Non-Goals

- Container startup testing (static audit only)
- Full README rewrite for all 842 templates (subset only)
- Adding new templates
- Build hardening or caching improvements (M001 residual)

## Architectural Decisions

### Audit Script Language

**Decision:** Node.js (same as existing tooling)

**Rationale:** build-registry.js and generate-docs.js are both Node.js. An audit script in the same stack means zero new dependencies and consistent JSON handling.

**Alternatives Considered:**
- Python — would work but introduces a second runtime for this project's tooling

### Tag Taxonomy Approach

**Decision:** Polish the existing 52-category taxonomy, don't redesign

**Rationale:** The current tags cover the right range. Some overlap exists (authentication/identity, business/e-commerce) that can be merged. All 842 templates need a manual tag review but the categories themselves mostly work.

**Alternatives Considered:**
- Trim to 20 — loses granularity needed for filtering
- Keep as-is — doesn't fix the miscategorized templates

### Deploy Config Verification

**Decision:** Static audit only

**Rationale:** Port mismatches, missing env vars, and stale image references are all detectable by reading files. Container startup would add significant time for minimal additional signal.

## Error Handling Strategy

The audit script logs errors per template and continues. Non-blocking warnings (e.g., "description could be better") are separated from blocking errors (e.g., "missing upstream URL"). The milestone succeeds when the worst offenders are fixed, not when every template is perfect.

## Risks and Unknowns

- Some templates may have no known upstream project URL — these need a researched link or a "no known upstream" note in arcane.json
- ~38 non-serviceable templates may not need tag fixes or README rewrites — worth flagging during audit
- The worst-offender count (~150-200) is a guess until the audit runs. Could be higher or lower
- Tag taxonomy polish needs judgment calls on which categories to merge

## Existing Codebase / Prior Art

- `scripts/build-registry.js` — registry builder, reads arcane.json + template files
- `scripts/generate-docs.js` — doc page generator, reads registry.json and template READMEs
- `docs/.vitepress/components/TemplateGrid.vue` — browse page, links to `/templates/{id}.html`
- `docs/.vitepress/data/templates.data.json` — enriched template data for Vue components
- Template READMEs follow a structured pattern (Quick Start → Architecture → Configuration → Troubleshooting → Backup → Links → Prerequisites) but content quality varies

## Relevant Requirements

- R014 — Audit tool identifies all quality issues
- R015 — Deploy configs are internally consistent
- R016 — Worst-offender READMEs rewritten
- R017 — Tags consistently applied
- R018 — Site rebuilds cleanly

## Technical Constraints

- Audit script must be compatible with `scripts/build-registry.js` conventions (same directory, similar output format)
- README changes that affect `content_hash` in registry.json are expected — registry will rebuild on next deploy
- `docs:generate` must be re-run after content changes to update the site

## Integration Points

- `scripts/build-registry.js` — consumes templates/* files, produces registry.json; content_hash changes don't break anything
- `scripts/generate-docs.js` — consumes registry.json + template READMEs; must be re-run after README changes
- `docs/.vitepress/config.mts` — sidebar auto-generated; re-run docs:generate to update

## Testing Requirements

- Audit script run against all 842 templates produces zero unexpected errors
- `npm run docs:build` completes with no errors after all changes
- Spot-check 5-10 templates on the deployed site to verify links render correctly

## Acceptance Criteria

- S01: Audit script exists in `scripts/`, runnable, outputs ranked error lists
- S02: All port mismatches between docker-compose.yml and .env.example fixed
- S03: Worst-offender READMEs rewritten with real upstream links and accurate config docs
- S04: All 842 templates have appropriate tags from polished taxonomy, zero single-tag entries
- S05: VitePress site rebuilds cleanly, browse page shows updated descriptions

## Open Questions

- Should the audit script be run in CI on PRs to prevent quality regressions? (Future concern, not M002 scope)
