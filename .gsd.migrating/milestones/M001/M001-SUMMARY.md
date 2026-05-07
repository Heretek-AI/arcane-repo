# BLOCKER — auto-mode recovery failed

Unit `complete-milestone` for `M001` failed to produce this artifact after idle recovery exhausted all retries.

**Reason**: Deterministic policy rejection for complete-milestone "M001": bash: HARD BLOCK: unit "complete-milestone" runs under tools-policy "planning-dispatch" — bash is restricted to read-only commands (cat/grep/git log/etc); cannot run "cd "C:/Users/Derek/Desktop/arcane-repo" && git branch --show-current 2>&1". This is a mechanical gate enforced by manifest.tools (#4934). You MUST NOT proceed, retry the same call, or rationalize past this block. If you need to write user source, the work belongs in execute-task, not in a planning unit.. Retrying cannot resolve this gate — writing blocker placeholder to advance pipeline.

This placeholder was written by auto-mode so the pipeline can advance.
Review and replace this file before relying on downstream artifacts.