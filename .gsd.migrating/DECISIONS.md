# Decisions Register

<!-- Append-only. Never edit or remove existing rows.
     To reverse a decision, add a new row that supersedes it.
     Read this file at the start of any planning or research phase. -->

| # | When | Scope | Decision | Choice | Rationale | Revisable? | Made By |
|---|------|-------|----------|--------|-----------|------------|---------|
| D001 |  | audit | Audit tooling language | Node.js | Matches existing tooling in scripts/ (build-registry.js, generate-docs.js). No new language dependencies. | No | collaborative |
| D002 |  | audit | Deploy config verification approach | Static audit only | Static audit covers port mismatches, missing env vars, and stale image references without needing to start containers. Container startup testing would add significant time and complexity for 842 templates. | Yes — future milestone | collaborative |
| D003 |  | documentation | README rewrite approach | Manual rewrite for worst offenders subset | Full auto-generation for all 842 templates was considered but manual review produces better quality. Script-assisted audit identifies the worst ~150-200 for manual rewrite. | Yes | collaborative |
| D004 |  | documentation | Tag taxonomy approach | Polish existing taxonomy, manual review per template | Current 52 tags cover the range but have overlapping categories (authentication/identity) and inconsistent application. Polish rather than redesign to preserve existing browsing experience. | No | collaborative |
