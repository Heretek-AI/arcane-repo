# Decisions Register

<!-- Append-only. Never edit or remove existing rows.
     To reverse a decision, add a new row that supersedes it.
     Read this file at the start of any planning or research phase. -->

| # | When | Scope | Decision | Choice | Rationale | Revisable? |
|---|------|-------|----------|--------|-----------|------------|
| D001 | M001/S01 | infra | Python package manager | uv | Faster than pip, already used in base images | No |
| D002 | M001/S01 | infra | Node package manager | npm | Standard for Node projects | No |
| D003 | M001/S01 | infra | Shallow upstream clones | `--depth 1` | Reduces clone time and disk usage | No |
| D004 | M001/S01 | fix | MemVid extra resolution | Pin exact extras only | `[full]` extra pulls `ai>=4.0,<6.0` unavailable on image | No |
| D005 | M001/S01 | fix | Streamer-Sales/TrendRadar COPY path | Use lowercase directory names | Docker COPY is case-sensitive on Linux | No |
| D006 | M001/S01 | fix | UNIT3D npm fallback | `npm install` on `npm ci` failure | Shallow clone lacks `package-lock.json` | No |
| D007 | M001/S01 | fix | MLflow uv version | Upgrade uv via `pip install --upgrade uv>=0.11.7` | Base image has uv 0.9.30; mlflow[extras] requires uv>=0.11.7 | No |
| D008 | M001/S01 | fix | Sunshine build approach | Pin to older upstream tag | cmake interface changed in v2025.924.154138 | Yes — if pinning fails |
