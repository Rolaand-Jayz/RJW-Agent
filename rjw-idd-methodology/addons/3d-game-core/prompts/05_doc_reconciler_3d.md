# PROMPT-3D-0005 — Documentation Reconciler

**Purpose:**
Ensure method doctrine, project artefacts, and add-in outputs stay consistent after each iteration.

**Assistant Guidance:**
1. Load latest GDD, Engine, Perf, AI, Network, Observability, and Build specs (`SPEC-3D-*`).
2. Compare against `addons/config/features.yml` and profile overlays to detect drift.
3. Generate diffs highlighting:
   - Budget/tolerance mismatches.
   - Unlinked `REQ-####` / `SPEC-####` / `TEST-####` entries.
   - Pacts missing verification hooks.
4. Recommend updates in priority order, citing relevant artefacts and decisions.
5. Output a changelog-style summary plus a checklist for the next enable/verify cycle.

**Exit Criteria:**
- Every reported discrepancy ties to a trace ID.
- Provide scripts/commands to resolve (e.g., rerun `set_3d_profile.py`, update `perf_budget_gate` inputs).
