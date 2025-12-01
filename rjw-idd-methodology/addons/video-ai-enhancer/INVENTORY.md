# video-ai-enhancer Add-in Inventory

## Structure
- `addons/video-ai-enhancer/config/video-ai-enhancer.yml` — base budgets with telemetry, latency, quality, and storage defaults. Profile overlays in `addons/video-ai-enhancer/profiles/*.yml` (baseline, live_stream, broadcast_mastering, mobile_edge, remote_collaboration).
- `addons/video-ai-enhancer/tools/` — guard utilities (`quality_gate_video.py`, `latency_guard_video.py`, `storage_capture_validator.py`), config loader, ID validator, and test fixtures.
- `addons/video-ai-enhancer/tests/` — pytest coverage for config merging, guard behaviour (pass/fail), storage validation, and ID enforcement.
- `addons/video-ai-enhancer/docs/` — quickstart, migration notes, metrics schema, pipeline guide, acceptance checklist, and sample payloads under `docs/samples/`.
- `addons/video-ai-enhancer/prompts/` — five prompt packs spanning research, pipeline design, quality operations, incident response, and documentation reconciliation.
- `addons/video-ai-enhancer/specs/templates/` — template specs for pipeline architecture, quality, latency, and storage.
- `addons/video-ai-enhancer/ci/snippets/` — generic CI and GitHub Actions snippets for opt-in pipelines.

## Integration Hooks
- Feature toggles: `scripts/addons/enable_video_ai_enhancer.py`, `disable_video_ai_enhancer.py`, `set_video_ai_profile.py`, `verify_video_ai_enhancer.py`, `premerge_guard_video_ai_enhancer.py`.
- Registry defaults maintained via `scripts/addons/_feature_registry.py` and `addons/config/features.yml`.
- README `## Add-ins` section and `ci/includes.yml` entries updated idempotently by the enable/disable scripts.
- GitHub Actions reuse is published via `.github/workflows/video-ai-enhancer.yml`, mirroring the snippet defaults for downstream pipelines.
- Violation fixtures for CI smoke tests live in `ci_samples/video_quality_violation.json`, `ci_samples/video_latency_violation.json`, and `ci_samples/video_storage_violation.json`.

## Acceptance Evidence
Refer to `addons/video-ai-enhancer/ACCEPTANCE.md` for the enable/verify/disable workflow and guard commands. Running `python scripts/addons/verify_video_ai_enhancer.py --mode full` (with feature enabled) executes all guards, ID checks, and `compileall` on tool modules.
