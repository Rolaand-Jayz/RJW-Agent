# RJW-IDD Add-in: 3d-game-core

`METHOD-ADDIN-3D-CORE` — Opt-in augmentation of RJW-IDD for teams shipping 3D games across first/third person, isometric/2.5D, platformer, driving, action-RPG, and networked sub-genres. The base methodology remains unchanged; activation flows through the central feature registry and toggle scripts under `scripts/addons/`.

## Capabilities
- Profile-aware default budgets, tolerances, and artefact templates for common 3D sub-genres.
- End-to-end prompts to drive research, design, testing, pact negotiation, and knowledge reconciliation.
- Determinism, tolerant replay, and rollback harnesses with integration stubs for any engine.
- Asset and performance gates wired for CI snippets, plus metrics schema and adapters for Unity, Unreal, Godot, or custom engines.
- Migration & quickstart guides, pact exemplars, and acceptance criteria for enabling/disabling the add-in cleanly.

## Activation Model
1. Keep `addons/config/features.yml` as the single source of truth. `3d_game_core.enabled` defaults to `false`.
2. Run `python scripts/addons/enable_3d_game_core.py` to opt in. The script injects CI hooks, updates documentation links, and confirms idempotency.
3. Switch sub-genre defaults via `python scripts/addons/set_3d_profile.py --profile <profile>`.
4. Disable using `python scripts/addons/disable_3d_game_core.py` to reverse CI/documentation wiring without touching other artefacts.
5. Log the add-in decision in `docs/decisions/`, capture the feature change in `docs/change-log.md`, and note the audit tag in `logs/LOG-0001-stage-audits.md`.

All deliverables honour the RJW-IDD identifier scheme with traceability stubs (`REQ-####`, `SPEC-####`, `TEST-####`, `DEC-####`, `INTEG-####`) so downstream projects can extend with project-specific evidence.
