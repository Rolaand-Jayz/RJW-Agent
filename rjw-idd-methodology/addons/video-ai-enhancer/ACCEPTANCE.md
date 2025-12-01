# ACCEPTANCE-VIDEO-AI-0001 — Video AI Enhancer Add-in Acceptance Suite

## Entry Conditions
- Repository is clean and the base RJW-IDD methodology files are intact.
- `addons/config/features.yml` exists (create via scripts if missing).
- Python 3.11+ available locally; PyYAML remains optional thanks to the fallback parser.

## Acceptance Tests
1. **Feature Registry Toggle**
   - Run `python scripts/addons/enable_video_ai_enhancer.py`.
   - Verify `addons.video_ai_enhancer.enabled: true` in `addons/config/features.yml`.
   - Confirm `ci/includes.yml` lists the video snippets and `README.md` exposes the add-in link.
2. **Profile Switching**
   - `python scripts/addons/set_video_ai_profile.py --profile live_stream` updates only the video add-in profile.
   - Re-run with `--profile baseline`; output must be idempotent.
3. **Quality Gate**
   - `python addons/video-ai-enhancer/tools/quality_gate_video.py --metrics addons/video-ai-enhancer/docs/samples/quality_metrics_baseline.json --profile baseline` passes.
   - A deliberately degraded payload (e.g. `--metrics ci_samples/video_quality_violation.json`) fails with a clear message.
4. **Latency Guard**
   - `python addons/video-ai-enhancer/tools/latency_guard_video.py --trace addons/video-ai-enhancer/docs/samples/latency_trace_sample.json --profile live_stream` passes.
   - Violating trace data raises a failure summarising the offending metrics.
5. **Storage Validator**
   - `python addons/video-ai-enhancer/tools/storage_capture_validator.py --report addons/video-ai-enhancer/docs/samples/storage_report_sample.json --profile broadcast_mastering` passes.
   - Oversized segments should cause a non-zero exit and explain the thresholds exceeded.
6. **ID Validation**
   - `python addons/video-ai-enhancer/tools/validate_ids_video_addin.py` reports success when run from the repo root.
7. **Verification Harness**
   - `python scripts/addons/verify_video_ai_enhancer.py --mode full` (with feature enabled) checks feature registry alignment, CI wiring, doc links, ID validation, and runs the guard scripts.
   - `python scripts/addons/verify_video_ai_enhancer.py --mode smoke` runs when disabled and ensures no stray references remain.
8. **Disable Flow**
   - `python scripts/addons/disable_video_ai_enhancer.py` resets the feature flag, removes CI entries, and clears the README link without disturbing other content.

## Evidence Log — 2025-09-27
- `python scripts/addons/enable_video_ai_enhancer.py` set the feature flag to `true` and appended both CI snippets to `ci/includes.yml`.
- `python scripts/addons/verify_video_ai_enhancer.py --mode full` completed without errors; guard executions used the default baseline profile and `compileall` succeeded.
- Guard passes (baseline fixtures):
  - `quality_gate_video.py` with `docs/samples/quality_metrics_baseline.json`.
  - `latency_guard_video.py` with `docs/samples/latency_trace_sample.json` and `--variance 0.05` to respect live-stream tolerances.
  - `storage_capture_validator.py` with `docs/samples/storage_report_sample.json`.
  - `validate_ids_video_addin.py` over the add-in root.
- Guard violations exercised with `ci_samples/video_quality_violation.json`, `ci_samples/video_storage_violation.json`, and the shared `../ci_samples/video_latency_violation.json` (pending in-repo copy); each command failed with explicit threshold messages.
- `.github/workflows/video-ai-enhancer.yml` added as the reusable GitHub Actions entry point mirroring the published snippet and wiring repo/project inputs.

## Known Gaps
- Latency quickstart (`addons/video-ai-enhancer/docs/quickstart.md`) still assumes zero variance; update guidance to mention the supported `--variance` margin for live-stream traces.
- The latency violation fixture referenced in acceptance guidance (`ci_samples/video_latency_violation.json`) is only present in the shared samples directory one level up from this repo—consider duplicating it locally for symmetry with quality/storage fixtures.

## Exit Criteria
- All commands above execute without manual edits beyond the scripted toggles.
- Running enable/disable scripts repeatedly produces no diffs (`git diff` clean).
- The add-in can be wired into CI via `scripts/addons/premerge_guard_video_ai_enhancer.py` when `addons.video_ai_enhancer.enabled` is `true`.
- Decision, Change Log, and stage-audit entries updated to reflect the current enablement state.
