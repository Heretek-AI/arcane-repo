# Requirements

This file is the explicit capability and coverage contract for the project.

## Active

### R014 — Template audit tool identifies all quality issues across 842 templates
- Class: quality-attribute
- Status: active
- Description: Node.js audit script scans all templates for broken upstream links, placeholder descriptions, port mismatches between docker-compose.yml and .env.example, missing env vars, stale image references, and missing tags
- Why it matters: Without a complete audit, manual fixes can't be prioritized and regressions aren't detectable
- Source: user
- Primary owning slice: M002/S01
- Supporting slices: none
- Validation: unmapped
- Notes: Audit must produce ranked lists per fix category (worst offenders first) to guide manual work in subsequent slices

### R015 — Deploy configs (docker-compose.yml + .env.example) are internally consistent and correct
- Class: quality-attribute
- Status: active
- Description: Port mappings in docker-compose.yml match .env.example defaults; all referenced volumes exist; no stale or unreferenced variables; health checks present where applicable
- Why it matters: Users should be able to cp .env.example → .env and docker compose up without hitting mismatches
- Source: user
- Primary owning slice: M002/S02
- Supporting slices: none
- Validation: unmapped
- Notes: Static audit only — no container startup testing

### R016 — READMEs for worst-offender templates have accurate upstream links, real env var tables, and working setup instructions
- Class: quality-attribute
- Status: active
- Description: ~150-200 templates with placeholder descriptions or missing upstream links get manually rewritten READMEs with correct project homepage, accurate environment variable documentation, and troubleshooting guidance
- Why it matters: Template descriptions like "X — self-hosted via Docker Compose" provide no useful information. Upstream links are the primary discovery mechanism.
- Source: user
- Primary owning slice: M002/S03
- Supporting slices: none
- Validation: unmapped
- Notes: Manual rewrites for the worst offenders identified by the S01 audit

### R017 — Tags are consistently applied across all templates using a clean taxonomy
- Class: quality-attribute
- Status: active
- Description: All 842 templates have appropriate tags from a polished 52-category taxonomy. Duplicate/overlapping categories merged. No template is missing tags or miscategorized.
- Why it matters: Tag-based browsing and filtering only works if tags are consistent and accurate
- Source: user
- Primary owning slice: M002/S04
- Supporting slices: none
- Validation: unmapped
- Notes: Manual review per template. Merge overlapping categories like authentication/identity, business/e-commerce.

### R018 — Website rebuilds cleanly from updated template content
- Class: quality-attribute
- Status: active
- Description: Running docs:generate + docs:build produces a clean site build with all 842 template pages, updated sidebar, and no dead links
- Why it matters: The user-facing site must reflect the improved content
- Source: user
- Primary owning slice: M002/S05
- Supporting slices: none
- Validation: unmapped
- Notes: Must re-run after S02-S04 changes

### R012 — Sunshine Docker build passes with cmake, gcc-13, and submodule support
- Class: integration
- Status: active
- Description: Sunshine Docker build passes with cmake, gcc-13, and submodule support
- Why it matters: Sunshine had cmake configure errors hidden by shell-pipefail wrapper; needed gcc-13 PPA, tag pin, and --recurse-submodules fix
- Source: M001/S01
- Primary owning slice: S01
- Validation: gh run view 25497271164 returned conclusion: success — gcc-13 PPA, v2025.924.154138 pin, --recurse-submodules

### R013 — Runner-starved batch (Harbor-LLM, KAG, CC Gateway) pass on re-dispatch
- Class: integration
- Status: active
- Description: Runner-starved batch (Harbor-LLM, KAG, CC Gateway) pass on re-dispatch
- Why it matters: 6 workflows were runner-starved; 3 confirmed passing, 3 identified as having real build errors (not starvation)
- Source: M001/S01
- Primary owning slice: S01
- Validation: gh run list confirmed Harbor-LLM, KAG, CC Gateway passing; AionUI/WGCloud/Yuxi failures documented as build issues

## Validated

### R001 — MemVid Docker build passes reliably
- Status: validated
- Description: MemVid Docker build passes reliably
- Validation: gh run view 25474465254 returned conclusion: success

### R004 — Untitled
- Status: validated
- Validation: UNIT3D Docker build confirmed passing — run 25474468047 returned conclusion: success on gh run view

### R005 — Untitled
- Status: validated
- Validation: MLflow Docker build confirmed passing — run 25474469087 returned conclusion: success on gh run view

### R006 — Untitled
- Status: validated
- Validation: Sunshine Docker build confirmed passing — run 25497271164 returned conclusion: success after gcc-13 PPA fix, tag pin to v2025.924.154138, and --recurse-submodules for third-party deps

### R007 — Untitled
- Status: validated
- Validation: Harbor-LLM (run 25484829333), KAG (run 25484889320), CC Gateway (run 25485314077) confirmed passing. AionUI, WGCloud, Yuxi still fail — root cause is build issues, not runner starvation (sequential dispatch with 30s intervals did not resolve)
- Notes: AionUI (run 25495898323), WGCloud (run 25495943070), Yuxi (run 25495982501) still failing — not runner-starved. Need deeper build diagnosis in follow-up.

### R008 — Streamer-Sales Docker build passes reliably
- Class: integration
- Status: validated
- Description: Streamer-Sales Docker build passes reliably
- Why it matters: Part of the 5 structurally fixed Docker builds that needed verification
- Source: M001/S01
- Primary owning slice: S01
- Validation: gh run view 25474466236 returned conclusion: success

### R009 — TrendRadar Docker build passes reliably
- Class: integration
- Status: validated
- Description: TrendRadar Docker build passes reliably
- Why it matters: Part of the 5 structurally fixed Docker builds that needed verification
- Source: M001/S01
- Primary owning slice: S01
- Validation: gh run view 25474467220 returned conclusion: success

### R010 — UNIT3D Docker build passes reliably
- Class: integration
- Status: validated
- Description: UNIT3D Docker build passes reliably
- Why it matters: Part of the 5 structurally fixed Docker builds that needed verification
- Source: M001/S01
- Primary owning slice: S01
- Validation: gh run view 25474468047 returned conclusion: success

### R011 — MLflow Docker build passes reliably
- Class: integration
- Status: validated
- Description: MLflow Docker build passes reliably
- Why it matters: Part of the 5 structurally fixed Docker builds that needed verification
- Source: M001/S01
- Primary owning slice: S01
- Validation: gh run view 25474469087 returned conclusion: success

## Deferred

## Out of Scope

## Traceability

| ID | Class | Status | Primary owner | Supporting | Proof |
|---|---|---|---|---|---|
| R001 |  | validated | none | none | gh run view 25474465254 returned conclusion: success |
| R004 |  | validated | none | none | UNIT3D Docker build confirmed passing — run 25474468047 returned conclusion: success on gh run view |
| R005 |  | validated | none | none | MLflow Docker build confirmed passing — run 25474469087 returned conclusion: success on gh run view |
| R006 |  | validated | none | none | Sunshine Docker build confirmed passing — run 25497271164 returned conclusion: success after gcc-13 PPA fix, tag pin to v2025.924.154138, and --recurse-submodules for third-party deps |
| R007 |  | validated | none | none | Harbor-LLM (run 25484829333), KAG (run 25484889320), CC Gateway (run 25485314077) confirmed passing. AionUI, WGCloud, Yuxi still fail — root cause is build issues, not runner starvation (sequential dispatch with 30s intervals did not resolve) |
| R008 | integration | validated | S01 | none | gh run view 25474466236 returned conclusion: success |
| R009 | integration | validated | S01 | none | gh run view 25474467220 returned conclusion: success |
| R010 | integration | validated | S01 | none | gh run view 25474468047 returned conclusion: success |
| R011 | integration | validated | S01 | none | gh run view 25474469087 returned conclusion: success |
| R012 | integration | active | S01 | none | gh run view 25497271164 returned conclusion: success — gcc-13 PPA, v2025.924.154138 pin, --recurse-submodules |
| R013 | integration | active | S01 | none | gh run list confirmed Harbor-LLM, KAG, CC Gateway passing; AionUI/WGCloud/Yuxi failures documented as build issues |

## Coverage Summary

- Active requirements: 2
- Mapped to slices: 2
- Validated: 9 (R001, R004, R005, R006, R007, R008, R009, R010, R011)
- Unmapped active requirements: 0
