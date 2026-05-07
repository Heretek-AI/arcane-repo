# Requirements

This file is the explicit capability and coverage contract for the project.

## Active

### R001 — MemVid build passes
- Class: core-capability
- Status: active
- Description: The MemVid Docker image builds successfully on GitHub Actions with uv, python 3.12, and all required Python packages installed
- Why it matters: This is a core deliverable of M001
- Source: user
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: unmapped
- Notes: Fix was applied (removed [full] extra, pinned uv-compatible extras). Re-run pending.

### R002 — Streamer-Sales build passes
- Class: core-capability
- Status: active
- Description: The Streamer-Sales Docker image builds successfully. COPY path case mismatch was resolved.
- Why it matters: Core deliverable of M001
- Source: user
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: unmapped
- Notes: Fix applied, confirmed green (run 25471563278)

### R003 — TrendRadar build passes
- Class: core-capability
- Status: active
- Description: The TrendRadar Docker image builds successfully. COPY path case mismatch was resolved.
- Why it matters: Core deliverable of M001
- Source: user
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: unmapped
- Notes: Fix applied, confirmed green (run 25471563288)

### R004 — UNIT3D build passes
- Class: core-capability
- Status: active
- Description: The UNIT3D Docker image builds successfully on GitHub Actions. npm fallback for shallow clone was added.
- Why it matters: Core deliverable of M001
- Source: user
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: unmapped
- Notes: Fix applied in commit a09070a. Build dispatched but may OOM on frontend-builder stage.

### R005 — MLflow build passes
- Class: core-capability
- Status: active
- Description: The MLflow Docker image builds successfully. uv was upgraded via pip before mlflow install.
- Why it matters: Core deliverable of M001
- Source: user
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: unmapped
- Notes: Fix applied. Re-run pending.

### R006 — Sunshine build passes
- Class: core-capability
- Status: active
- Description: The Sunshine Docker image builds successfully. cmake interface compatibility is resolved.
- Why it matters: Core deliverable of M001
- Source: user
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: unmapped
- Notes: Blocked — upstream cmake interface changed in v2025.924.154138. Need to pin to older working tag or patch build script.

### R007 — Runner-starved builds re-dispatch and pass
- Class: core-capability
- Status: active
- Description: AionUI, Harbor-LLM, KAG, WGCloud, Yuxi, CC Gateway all build successfully after re-dispatch
- Why it matters: These builds were runner-starved (failed from resource contention in a large concurrent batch), not from code issues
- Source: user
- Primary owning slice: M001/S01
- Supporting slices: none
- Validation: unmapped
- Notes: Need to re-dispatch each workflow individually or in a smaller batch to avoid runner starvation.

## Traceability

| ID | Class | Status | Primary owner | Supporting | Proof |
|---|---|---|---|---|---|
| R001 | core-capability | active | M001/S01 | none | unmapped |
| R002 | core-capability | active | M001/S01 | none | unmapped |
| R003 | core-capability | active | M001/S01 | none | unmapped |
| R004 | core-capability | active | M001/S01 | none | unmapped |
| R005 | core-capability | active | M001/S01 | none | unmapped |
| R006 | core-capability | active | M001/S01 | none | unmapped |
| R007 | core-capability | active | M001/S01 | none | unmapped |

## Coverage Summary

- Active requirements: 7
- Mapped to slices: 0 (all in M001/S01)
- Validated: 2 (R002, R003 — confirmed green)
- Unmapped active requirements: 5 (R001, R004, R005, R006, R007)
