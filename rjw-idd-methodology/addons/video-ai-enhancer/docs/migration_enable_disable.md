# DOC-VIDEO-MIGRATION-0001 — Enable/Disable Migration Notes

## Enabling
1. Update stakeholders that the video enhancer tooling is opt-in and confirm telemetry consent.
2. Run:
   ```bash
   python scripts/addons/enable_video_ai_enhancer.py
   python scripts/addons/set_video_ai_profile.py --profile baseline
   ```
3. Wire CI snippets referenced in `ci/includes.yml`.
4. Drop prompt packs or spec templates into the project repo as needed.

## Disabling
1. Ensure quality, latency, and storage gates are no longer referenced in CI.
2. Run `python scripts/addons/disable_video_ai_enhancer.py`.
3. Confirm `addons/config/features.yml` sets `video_ai_enhancer.enabled: false` and README no longer lists the add-in.
4. Optional: archive artefacts under project-specific doc control using the RJW-IDD ID schema.

## Rollback Safety
- Scripts are idempotent and leave telemetry samples untouched for audit.
- Verification harness (`scripts/addons/verify_video_ai_enhancer.py`) can be executed before or after toggling to ensure clean state.
