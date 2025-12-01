# SPEC-3D-ENGINE-0001 — Engine Integration Blueprint

- **Active Profile:** `<addons/config/features.yml :: addons.3d_game_core.profile>`
- **Linked Decisions:** `DEC-3D-ENGINE-0001`, `DEC-3D-BUILD-0002`
- **Integration IDs:** `INTEG-3D-ENGINE-0001` (runtime), `INTEG-3D-BUILD-0002` (toolchain)

## 1. Runtime Architecture
- Simulation loop diagram referencing fixed timestep (`randomisation.fixed_timestep_hz`).
- Component authority mapping (server/client/peer) with rollback hooks if `networked` profile is active.
- ECS / scene graph layering, with references to `SPEC-3D-OBS-0001` for telemetry taps.

## 2. Time & Determinism
- Deterministic ordering contracts (`DEC-3D-DETERMINISM-0003`).
- Random seed strategy & reseeding points; align with `randomisation.default_seed`.
- Authoritative state snapshot provider path for `determinism_harness.py` integration.

## 3. Data Flows
- Asset ingest pipeline (importer, conditioning, validation) hooking into `asset_rules`.
- Metrics emission conforming to `docs/metrics_schema.md` (profile overlays may add fields).
- Build variants, target platforms, and toolchain matrix.

## 4. Acceptance Criteria
- `TEST-3D-ENGINE-AC01`: Determinism harness over 10k ticks reports stable hashes for golden tape.
- `TEST-3D-ENGINE-AC02`: Rollback harness misprediction rate < threshold defined by the active profile.
- `TEST-3D-ENGINE-AC03`: CI export produces metrics matching schema & budgets.

## 5. Traceability
| Artefact | Identifier |
| --- | --- |
| Requirements | `REQ-3D-ENGINE-*` |
| Decisions | `DEC-3D-DETERMINISM-*`, `DEC-3D-BUILD-*` |
| Tests | `TEST-3D-ENGINE-*`, `TEST-3D-ROLLBACK-*` |
| Integrations | `INTEG-3D-ENGINE-*`, `INTEG-3D-CI-*` |

> **Profile Hook:** Reference the selected profile file under `addons/3d-game-core/profiles/` when setting subsystem budgets, so downstream scripts can diff against this spec.
