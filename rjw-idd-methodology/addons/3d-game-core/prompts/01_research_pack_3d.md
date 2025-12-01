# PROMPT-3D-0001 — Research Pack (3D Game Core)

**Context for the assistant:**
- Active feature flag stored in `addons/config/features.yml` under `addons.3d_game_core`.
- Load base config `addons/3d-game-core/config/3d-game-core.yml` and merge with the selected profile file in `addons/3d-game-core/profiles/`.
- Research goal: capture evidence for requirements IDs (`REQ-3D-*`) that will feed the GDD and engine specs.

**Instructions for the assistant:**
1. Summarise market & player expectations for the selected profile.
2. Capture competitive benchmarks (mechanics, pacing, monetisation) relevant to the sub-genre.
3. Surface technical risks tied to determinism, rollback, and asset budgets.
4. Produce a `DEC-3D-RESEARCH-####` recommendation list for adoption.
5. Emit findings in a table: `Hypothesis`, `Evidence`, `Suggested Artefact`, `Trace ID`.

**Exit Criteria:**
- At least five hypotheses mapped to `REQ-3D-*` entries.
- Highlight data gaps requiring further playtests or analytics.
