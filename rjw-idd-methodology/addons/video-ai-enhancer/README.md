# RJW-IDD Add-in: video-ai-enhancer

`METHOD-ADDIN-VIDEO-AI` — Opt-in augmentation of RJW-IDD for teams delivering real-time video enhancement and upscaling pipelines that must stream, collaborate, and capture output with deterministic quality. The base methodology remains unchanged; activation flows through the feature registry and toggle scripts under `scripts/addons/`.

## Capabilities
- Latency-aware budgets, model selection templates, and storage governance profiles for live streaming, broadcast mastering, mobile edge, and remote collaboration.
- Prompt suites covering signal research, pipeline architecture, model QA, operations, and knowledge reconciliation tuned for video enhancement.
- Quality, latency, and storage guards with sample payloads for CI integration plus ID validators for add-in artefacts.
- Quickstart, migration, and metrics schema docs to on-board teams and wire telemetry/export with OTLP or custom sinks.
- Clean enable/disable scripts that register CI snippets, documentation links, and feature flags in an idempotent fashion.

## Activation Model
1. Keep `addons/config/features.yml` as the source of truth. `video_ai_enhancer.enabled` defaults to `false`.
2. Run `python scripts/addons/enable_video_ai_enhancer.py` to opt in. The script registers CI snippets, documentation links, and ensures idempotency.
3. Switch latency/quality defaults via `python scripts/addons/set_video_ai_profile.py --profile <profile>`.
4. Disable using `python scripts/addons/disable_video_ai_enhancer.py` to remove CI/documentation wiring without touching other artefacts.
5. Record the enable/disable decision in `docs/decisions/`, update `docs/change-log.md`, and tag the action in `logs/LOG-0001-stage-audits.md`.

All deliverables honour the RJW-IDD identifier scheme with traceability tokens (`SPEC-VIDEO-*`, `REQ-VIDEO-*`, `TEST-VIDEO-*`, etc.) so downstream projects can surface evidence and audit readiness.
