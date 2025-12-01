# SPEC-3D-GDD-0001 — Game Design Document (3D)

- **Active Profile:** `<pull from addons/config/features.yml :: addons.3d_game_core.profile>`
- **Linked Decision:** `DEC-3D-GDD-0001`
- **Owning Phase:** `METHOD-0001 :: Discover` → `METHOD-0002 :: Phase Kick-off`

## 1. Experience Overview
- `REQ-3D-GAMEPLAY-0001` — Core fantasy & loops summarised for the chosen profile.
- `REQ-3D-WORLD-0002` — Biome diversity, traversal verbs, and verticality targets.
- `REQ-3D-CAMERA-0003` — Camera modes, FOV ranges, collision handling, and assist behaviours.

## 2. Systems Grid
Document the primary systems and their interplay. For each, capture:
- Purpose, major states, and failure cases.
- Ties to profile tolerances e.g., deterministic inputs for `first_person`, or rollback resilience for `networked`.
- A pointer to the engineering spec section that elaborates the implementation.

| System | Key Decisions (`DEC-####`) | Spec Reference (`SPEC-####`) | Tests (`TEST-####`) |
| --- | --- | --- | --- |
| Input & Camera | `DEC-3D-INPUT-0001` | `SPEC-3D-ENGINE-0003` | `TEST-3D-CAM-0004` |
| Locomotion & Physics | `DEC-3D-LOCO-0005` | `SPEC-3D-PHYSICS-0002` | `TEST-3D-MOVE-0006` |
| Combat / Interaction | `DEC-3D-COMBAT-0007` | `SPEC-3D-AI-0001` | `TEST-3D-COMBAT-0008` |

## 3. Content Pillars
- Narrative arcs, quest topology, meta-progression.
- Asset scale targets: meshes per biome, animation sets per archetype, SFX coverage, VFX budget.
- Accessibility & localisation commitments (e.g., camera comfort, colour-blind shaders).

## 4. Acceptance Criteria (Profile-aware)
- `TEST-3D-GDD-AC01`: Gameplay prototypes meet the motion/combat feel metrics listed in profile `performance_budgets.scene`.
- `TEST-3D-GDD-AC02`: Tutorial beats validate latency, readability, and onboarding gates for the active profile tolerances.
- `TEST-3D-GDD-AC03`: Player archetype coverage matches `asset_rules` entries (skeletal/audio) for the selected profile.

## 5. Traceability Matrix
| Artefact | Identifier |
| --- | --- |
| Upstream Requirements | `REQ-3D-*`
| Supporting Decisions | `DEC-3D-*`
| Implementation Specs | `SPEC-3D-*`
| Verification Assets | `TEST-3D-*`
| Integration Touchpoints | `INTEG-3D-*`

> **Profiling Tip:** Reference `scripts/addons/set_3d_profile.py --profile <name>` outputs in this document to prove alignment whenever the team pivots sub-genre coverage.
