# ACCEPTANCE-3D-CORE-0001 — 3D Game Core Add-in Acceptance Suite

## Entry Conditions
- Repository is clean and the base RJW-IDD methodology files are intact.
- `addons/config/features.yml` exists (scripts create it on demand).
- Python 3.11+ available locally; PyYAML optional (fallback parser provided).

## Acceptance Tests
1. **Feature Registry Toggle**
   - Run `python scripts/addons/enable_3d_game_core.py`.
   - Verify `addons.3d_game_core.enabled: true` in `addons/config/features.yml`.
   - Confirm `ci/includes.yml` lists both CI snippets and `README.md` exposes the add-in link.
2. **Profile Switching**
   - `python scripts/addons/set_3d_profile.py --profile third_person` should update the registry without disturbing other fields.
   - Re-run with `--profile generic`; output must be idempotent.
3. **Determinism Harness**
   - `python addons/3d-game-core/tools/determinism_harness.py --ticks 120 --seed 42 --tape tmp/determinism.json --profile generic` produces stable hashes and aggregate output.
4. **Tolerant Replay Runner**
   - `python addons/3d-game-core/tools/tolerant_replay_runner.py --snapshots ci_samples/tolerant_snapshots.json --profile generic` passes.
   - Re-run with `--scale 0.1` to confirm drift failure handling.
5. **Rollback Simulation Harness**
   - `python addons/3d-game-core/tools/rollback_sim_harness.py --tape ci_samples/rollback_tape.json --profile generic` passes.
   - Failure raised for `ci_samples/rollback_tape_violation.json`.
6. **Asset Linter**
   - `python addons/3d-game-core/tools/asset_linter_3d.py --manifest ci_samples/assets_manifest.json --profile generic` passes.
   - `python addons/3d-game-core/tools/asset_linter_3d.py --manifest ci_samples/assets_manifest_violation.json --profile generic` returns a non-zero code.
7. **Performance Budget Gate**
   - `python addons/3d-game-core/tools/perf_budget_gate_3d.py --metrics addons/3d-game-core/docs/samples/perf_metrics_generic.json --profile generic` passes.
   - `python addons/3d-game-core/tools/perf_budget_gate_3d.py --metrics ci_samples/perf_metrics_violation.json --profile generic` fails with a clear message.
8. **Documentation & CI Wiring**
   - `python scripts/addons/verify_3d_game_core.py --mode full` (with feature enabled) executes the above checks, runs `compileall`, and validates README/CI state.
   - `python scripts/addons/verify_3d_game_core.py --mode smoke` runs when disabled and confirms absence of side-effects.
9. **ID Validation**
   - `python addons/3d-game-core/tools/validate_ids_3d_addin.py` reports success.
10. **Disable Flow**
    - `python scripts/addons/disable_3d_game_core.py` resets the feature flag, removes CI entries, and clears the README link without disturbing other content.

## Exit Criteria
- All commands above run without manual edits beyond the scripted toggles.
- Running enable/disable scripts repeatedly produces no diffs (`git diff` clean).
- Acceptance suite executed in CI via `scripts/addons/premerge_guard_3d_game_core.py` when `addons.3d_game_core.enabled` is `true`.
- Decision, Change Log, and stage-audit entries updated to reflect the current enablement state.
