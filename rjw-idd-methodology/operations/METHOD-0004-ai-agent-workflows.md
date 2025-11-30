# METHOD-0004 — RJW-IDD Workflow for AI Coding Agents

This playbook turns the RJW-IDD method pack into concrete steps for teams working with AI coding agents. Follow it to reproduce the evidence → spec → implementation loop captured in the scaffold.

> **Quick Start:** Classify your change risk level using [METHOD-0002 Quick Start](#streamlined-workflow-selection) before proceeding. Low-risk changes can skip directly to [Streamlined Pathways](#streamlined-pathways).

## 0. Assign Roles and Trust Levels

Record role owners in `rjw-idd-methodology/governance/METHOD-0003-role-handbook.md` and the active row in `docs/change-log.md`.

| Role | Responsibilities | Companion Artefacts |
|------|------------------|---------------------|
| Agent Conductor | Runs prompts, captures transcripts, executes guard scripts. | `docs/prompts/`, `artifacts/integration/transcript-archive/`, `logs/ci/` |
| Spec Curator | Maintains ledgers, specs, reconciliation log, and decision links. | `specs/`, `artifacts/ledgers/`, `docs/living-docs-reconciliation.md` |
| Doc Steward | Updates living documentation and verifies Change Log entries. | `docs/standards/DOC-0006`, `docs/runbooks/` |
| Governance Sentinel | Runs validators, records audits, blocks releases missing artefacts. | `scripts/validate_ids.py`, `logs/LOG-0001-stage-audits.md` |

### Agent Trust Levels

Before starting work, confirm the agent's trust level per `METHOD-0006`:

| Trust Level | Autonomy | Process Access |
|-------------|----------|----------------|
| Level 0 (Supervised) | All actions require human approval | Minimal Risk path only |
| Level 1 (Guided) | Pre-approved categories proceed automatically | Minimal/Low Risk paths |
| Level 2 (Autonomous) | Operates independently with post-hoc review | Minimal/Low/Medium Risk paths |
| Level 3 (Trusted Partner) | Participates in planning and prioritization | All paths; can approve others |

## Streamlined Workflow Selection

**Classify risk first** — not all changes require the full workflow:

| Risk Level | Examples | Pathway |
|------------|----------|---------|
| **Minimal** | Doc typos, formatting, comments | Commit → Auto-verify → Merge |
| **Low** | New tests, new docs, config defaults | Commit → Verify → Change log → Merge |
| **Medium** | Bug fixes, refactors, internal API changes | Full verification + peer review |
| **High** | Feature additions, external API changes | Full Discovery→Execution loop |
| **Critical** | Security, data, availability changes | Full loop + Security review |

For Minimal/Low/Medium risk, use the [Streamlined Pathways](#streamlined-pathways) below.

## Streamlined Pathways

### Minimal Risk (5 min)

```bash
# 1. Make change
# 2. Commit
git commit -m "docs: [brief description]"
# 3. Auto-verify and merge
```

### Low Risk (30 min)

```bash
# 1. Make change
# 2. Verify
[automated checks pass]
# 3. Update change log (simplified entry)
# 4. Commit and merge
```

### Medium Risk (2 hours)

1. Classify risk in commit message
2. Run full automated verification
3. Request peer review
4. Ensure tests cover changes
5. Update documentation
6. Add standard change log entry
7. Merge with reviewer sign-off

---

**For High/Critical risk, proceed with full workflow below.**

## 1. Inputs Before Work (High/Critical Risk)
1. Copy `rjw-idd-starter-kit/docs/change-log.md` into your repository and open a new `change-YYYYMMDD-##` row.
2. Draft a `DEC-####` stub using `rjw-idd-methodology/templates/PROJECT-DEC-template.md` for the problem you are addressing.
3. Review `docs/living-docs-reconciliation.md`; log and assign any documentation gaps.
4. Schedule audit tags (`⟦audit-id:n⟧ <reflect/>`) and note them in the stage audit log.

## 2. Stage Workflows
### Layer 1 — Discovery
**Research Loop**
- Run `tools/rjw_idd_evidence_harvester.py` with `research/evidence_tasks.json`.
- Store logs under `logs/discovery-harvest/` (or your chosen path) and validate results with `scripts/validate_evidence.py`.
- Promote curated evidence into `research/evidence_index.json` via `scripts/promote_evidence.py`.
- Update requirement ledger entries with new evidence IDs and log the harvest in `docs/change-log.md`.

**Specification Loop**
- Author/update specs using templates in `specs/`, linking to relevant evidence and planned tests.
- Reserve requirement/test IDs in `artifacts/ledgers/*.csv` (or equivalent datasets).
- Resolve items in `docs/living-docs-reconciliation.md` before declaring Discovery complete.
- Capture outcomes in `docs/decisions/` and update `docs/change-log.md` with verification details.

### Layer 2 — Execution (TDD, Living Docs, Delivery)
- Use `docs/prompts/PROMPT-0001-omega-engineering.md` (or a customised prompt) to drive the agent.
- Enforce test-first and governance guards via `scripts/ci/test_gate.sh`, which now executes:
  - `tools/testing/red_green_guard.py` to require failing tests before implementation.
  - `scripts/validate_ids.py` to keep ledgers, specs, and change-log references aligned.
  - `scripts/validate_evidence.py` (triggered when research assets change) to ensure Execution sticks to fresh Discovery insight using a 14-day recency window.
  - `tools/testing/change_log_guard.py` to block merges that skip the change log.
  - `tools/testing/living_docs_guard.py` to reject outstanding living-doc gaps and demand documentation updates alongside implementation.
  - `tools/testing/governance_alignment_guard.py` to keep specification changes, ledgers, and decision logs synchronized.
- Capture full integration transcripts under `artifacts/integration/transcript-archive/`.
- Update living documentation according to `docs/standards/DOC-0006`.
- Append `⟦audit-id:n⟧ <reflect/>` when the layer exits.

## 3. Living Documentation Enforcement
- Before work: log gaps in `docs/living-docs-reconciliation.md`.
- During work: update docs, runbooks, and specs with new IDs and Change Log references.
- After work: validate docs/IDs, link outputs in `docs/change-log.md`, and ensure doc updates ship with code.

## 4. Integration Transcript Checklist
For every AI-assisted integration:
1. Scaffold a directory with `tools/integration/archive_scaffold.py <task-slug>`.
2. Complete `context.md` with scope, linked IDs, roles, and planned doc updates.
3. Log prompts/responses in `prompts.log`, store diffs in `diffs/`, and document verification steps in `verification.md`.
4. Reference the archive path in `docs/change-log.md` and in the living documentation.

## 5. Cost, Security, and Observability Controls
- Run cost dashboards using `scripts/cost/run_weekly_dashboard.py`; store outputs and finance sign-offs under `logs/cost/`.
- Execute sandbox drills with `scripts/sandbox/drill.py` and record artefacts under `logs/security/`.
- Maintain telemetry/observability artefacts per `specs/SPEC-0301` and `specs/SPEC-0401`, ensuring consent receipts and metric snapshots are logged.

## 6. Decision & Audit Hygiene
- Every major choice gets a `DEC-####` entry referencing evidence, specs, and follow-up actions.
- Governance Sentinel keeps `logs/LOG-0001-stage-audits.md` current with stage reflections.
- Quarterly reviews revisit evidence recency, cost thresholds, security posture, and method changes; record outcomes as new decisions or spec updates.

## 7. Companion Assets
- `METHOD-0001` — Core methodology principles.
- `METHOD-0002` — Phase checklists (with Quick Start pathway selection).
- `METHOD-0003` — Role handbook.
- `METHOD-0006` — Agent trust and autonomy framework.
- `METHOD-0007` — Streamlined operations and human-friendly design.
- `rjw-idd-methodology/templates/DEC-template.md` — Full decision boilerplate (High/Critical risk).
- `rjw-idd-methodology/templates/DEC-LITE-template.md` — Lightweight decision template (Low/Medium risk).

Run this workflow step-by-step. When artefacts, prompts, or scripts evolve, update the corresponding specs/runbooks so the scaffold remains reusable for the next project.
