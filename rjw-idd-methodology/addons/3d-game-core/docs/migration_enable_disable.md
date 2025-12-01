# DOC-3D-MIGRATION-0001 — Enable / Disable Playbook

## Enabling the Add-in
1. Confirm clean workspace: `git status --short` (or manual check).
2. Run `python scripts/addons/enable_3d_game_core.py`.
3. Script effects:
   - Sets `addons.3d_game_core.enabled: true` in `addons/config/features.yml`.
   - Includes CI snippets (GitHub Actions or generic) based on repo conventions.
   - Adds `Add-ins` section to root `README.md` if absent, linking to `addons/3d-game-core/README.md`.
4. Choose a profile: `python scripts/addons/set_3d_profile.py --profile <profile>`.
5. Capture `DEC-3D-ADOPTION-0002` summarising rationale.

## Disabling the Add-in
1. Run `python scripts/addons/disable_3d_game_core.py`.
2. Script effects:
   - Removes CI snippet includes and resets the feature flag to `false`.
   - Leaves documentation references intact but marks add-in as inactive.
3. Validate: `python scripts/addons/verify_3d_game_core.py --mode smoke`.
4. Record a decommissioning decision (e.g., `DEC-3D-RETIRE-0001`).

## Re-enabling After Disable
1. Ensure old artefacts (metrics, tapes) are archived.
2. Re-run enable + profile selection scripts.
3. Rehydrate acceptance artefacts via `python scripts/addons/verify_3d_game_core.py`.

## Idempotency Notes
- All scripts are safe to re-run; they diff existing files before writing.
- Manual edits to CI or feature registry should be avoided—use scripts to prevent drift.

> Always document toggles in your project decision log to preserve audit history.
