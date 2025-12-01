# 3d-game-core Add-in Inventory

## Repository Survey
- **Prompts:** No method-level prompt directory present. The add-in will introduce `addons/3d-game-core/prompts/` for opt-in prompt packs.
- **Templates & Specs:** Core templates currently live under `templates/`. Add-in specific spec templates will reside in `addons/3d-game-core/specs/templates/` to keep methodology defaults untouched.
- **Docs & Standards:** Method doctrine is stored in `core/`, `governance/`, and `operations/`. Add-in specific guidance, inventories, and quickstarts live in `addons/3d-game-core/` (this directory).
- **Tools & Scripts:** No global `tools/` or `scripts/` directories exist yet. The add-in will add `addons/3d-game-core/tools/` for runtime utilities and `scripts/addons/` for feature toggles & verifiers.
- **CI / Guards / Validators:** No CI snippets or validator registry folders are present. The add-in introduces `addons/3d-game-core/ci/snippets/` and supporting guard wiring that is only referenced when the feature flag is enabled.
- **Config / Registry:** The central feature registry `addons/config/features.yml` tracks opt-in modules. Add-in budgets & tolerances are stored in `addons/3d-game-core/config/3d-game-core.yml` plus profile overlays.
- **ID / Traceability Validators:** No validators are currently present. The add-in will ship `tools/validate_ids_3d_addin.py` (or extend an existing validator if it appears later) to enforce RJW-IDD identifier schemes across add-in artefacts.

## Next Actions
1. Stand up the add-in directory tree under `addons/3d-game-core/` per requirements.
2. Populate config, prompts, specs, tools, docs, and CI snippets with profile-aware defaults.
3. Register feature toggles & scripts for enable/disable/profile management.
4. Extend validation and acceptance coverage so enable/disable/verify cycles are idempotent.
