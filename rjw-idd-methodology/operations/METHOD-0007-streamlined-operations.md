# METHOD-0007 — Streamlined Operations and Human-Friendly Design

This document refines the RJW-IDD methodology to improve speed, reduce overhead, and enhance human accessibility without sacrificing auditability. It introduces parallel execution paths, risk-proportionate process weight, and human-centered artefact design.

## 1. Purpose

**Goal:** Make RJW-IDD faster and easier to use by eliminating unnecessary ceremony while preserving governance where it matters.

**Principles:**

- **Process weight proportional to risk** — Simple changes deserve simple processes
- **Parallel by default** — Sequential gates only where dependencies require
- **Progressive disclosure** — Essential information first, details on demand
- **Automation over ceremony** — Machines handle routine checks; humans handle judgment
- **Defaults optimized for common cases** — Heavy process available when needed

## 2. Parallel-First Architecture

### Current State Problem

The standard Discovery → Execution flow enforces sequential gates that can bottleneck progress even when work streams are independent.

```text
Traditional Sequential Flow:
Research ──► Curate ──► Spec ──► Gate ──► Implement ──► Test ──► Gate ──► Deploy
   ▲                                  │
   └──────── blocked until ◄──────────┘
```

### Parallel Architecture

Restructure to maximize concurrent work where dependencies allow:

```text
Parallel-First Flow:
                    ┌─► Spec: Functional ─┐
Research ──► Curate ┼─► Spec: Quality ────┼─► Sync ──► Implement ──► Verify ──► Deploy
                    ├─► Spec: Security ───┤     ▲
                    └─► Spec: Ops ────────┘     │
                                                │
                    ┌─► Test: Unit ────────┐    │
                    ├─► Test: Integration ─┼────┘
                    └─► Doc: Updates ──────┘
```

### Sync Points

Synchronization required at these checkpoints:

| Sync Point | Purpose | Participants | Duration |
|------------|---------|--------------|----------|
| Post-Research | Align on findings before spec work | Evidence Lead, Spec Architect | 30 min |
| Pre-Implementation | Confirm specs compatible; resolve conflicts | All spec authors | 1 hour |
| Pre-Deploy | Verify all streams complete and consistent | Governance Sentinel | 15 min |

### Parallel Track Rules

**Independent Tracks (may run concurrently):**

- Functional spec ↔ Quality spec ↔ Security spec ↔ Ops spec
- Unit tests ↔ Integration tests ↔ Documentation updates
- Different feature implementations (non-overlapping scope)

**Dependent Tracks (must wait):**

- Implementation → after spec sync
- Deployment → after all verification
- Scope changes → after governance review

### Time Savings Estimate

| Scenario | Sequential | Parallel | Savings |
|----------|------------|----------|---------|
| Typical feature | 10 days | 6 days | 40% |
| Minor enhancement | 3 days | 2 days | 33% |
| Major initiative | 30 days | 18 days | 40% |

## 3. Risk-Proportionate Process

### Risk Classification

Classify changes by risk to determine appropriate process weight:

| Risk Level | Characteristics | Examples |
|------------|-----------------|----------|
| **Minimal** | No behavior change; typo/formatting | Doc typos, comment updates, formatting |
| **Low** | Additive only; easily reversible | New tests, new docs, config defaults |
| **Medium** | Behavior change within component | Bug fixes, refactors, internal API changes |
| **High** | Cross-component or user-visible | Feature additions, external API changes |
| **Critical** | Security, data, or availability | Auth changes, data migrations, prod config |

### Process Weight by Risk

#### Minimal Risk Path

**Process:** Commit → Auto-verify → Merge

**Requirements:**

- [ ] Automated lint/format check passes
- [ ] No functional changes detected

**Documentation:** Commit message only

**Approval:** None (automated merge permitted)

#### Low Risk Path

**Process:** Commit → Auto-verify → Change log → Merge

**Requirements:**

- [ ] Automated checks pass
- [ ] Change log entry added
- [ ] Artifact IDs follow scheme

**Documentation:**

- Change log row (simplified)
- Link to commit

**Approval:** Auto-approve if checks pass; optional peer review

#### Medium Risk Path

**Process:** Commit → Verify → Review → Change log → Merge

**Requirements:**

- [ ] Full automated verification suite
- [ ] Peer review completed
- [ ] Tests cover changes
- [ ] Documentation updated

**Documentation:**

- Standard change log entry
- Updated specs if behavior changed
- Test coverage report

**Approval:** One reviewer sign-off

#### High Risk Path

**Process:** Full Discovery + Execution loop

**Requirements:**

- [ ] DEC-#### decision record
- [ ] Spec updates (all affected areas)
- [ ] Comprehensive test coverage
- [ ] Living doc reconciliation cleared

**Documentation:**

- Decision record with full analysis
- All affected specs updated
- Integration transcripts archived
- Change log with verification links

**Approval:** Role-appropriate sign-offs per METHOD-0003

#### Critical Risk Path

**Process:** Enhanced governance with security review

**Requirements:**

- [ ] All High Risk requirements
- [ ] Security & Privacy Liaison review
- [ ] Rollback plan documented
- [ ] Staged deployment strategy
- [ ] Post-deployment verification plan

**Documentation:**

- Security impact assessment
- Rollback procedure
- Staged deployment log
- Post-deployment verification results

**Approval:** Governance Board + Security sign-off

### Process Selection Guide

```text
START
  │
  ▼
┌─────────────────────────────────────┐
│ Does this change behavior?          │──No──► Minimal Risk Path
└─────────────────────────────────────┘
  │ Yes
  ▼
┌─────────────────────────────────────┐
│ Is the change easily reversible?    │──Yes──► Low Risk Path
└─────────────────────────────────────┘
  │ No
  ▼
┌─────────────────────────────────────┐
│ Does it affect multiple components  │──No──► Medium Risk Path
│ or external interfaces?             │
└─────────────────────────────────────┘
  │ Yes
  ▼
┌─────────────────────────────────────┐
│ Does it involve security, data      │──No──► High Risk Path
│ integrity, or availability?         │
└─────────────────────────────────────┘
  │ Yes
  ▼
Critical Risk Path
```

## 4. Human-Centered Artifact Design

### Progressive Disclosure Structure

Restructure all methodology artefacts to front-load essential information:

```markdown
# [Document Title]

> **TL;DR:** One-sentence summary of purpose and key takeaway.

## Quick Reference
[Most frequently needed information: key dates, contacts, commands]

## Summary
[2-3 paragraph overview for scanning]

## Details
[Full content organized by topic]

## Reference
[Appendices, deep dives, historical context]
```

### Simplified Change Log Format

Replace verbose change log entries with scannable format:

**Before:**

```markdown
| change_id | date (UTC) | description | impacted_ids | operator | verification |
|-----------|------------|-------------|--------------|----------|--------------|
| change-20240327-01 | 2024-03-27 | Anchor governance artefacts and align method doctrine (DEC-0001). Includes creation of decision logs, change logs, stage-audit logs... [200+ words] | METHOD-0001;METHOD-0002;METHOD-0003;DEC-0001 | Governance Board | validator:pending; audit:⟦audit-id:1⟧ |
```

**After:**

```markdown
| ID | Date | Risk | Summary | Links |
|----|------|------|---------|-------|
| 2024-03-27-01 | 2024-03-27 | High | Anchor governance artefacts | [DEC-0001] [audit:1] |
```

Detailed description moves to linked decision record.

### Visual Checklists

Replace text-heavy checklists with visual progress indicators:

```markdown
## Phase Status

### Discovery ████████░░ 80%

- [x] Research planned
- [x] Harvest executed
- [x] Evidence curated
- [x] Gaps documented
- [ ] Specs aligned

### Execution ░░░░░░░░░░ 0%

- [ ] Implementation started
- [ ] Tests created
- [ ] Docs updated
- [ ] Integration verified
- [ ] Deployment ready
```

### Decision Record Simplification

Provide a lightweight decision template for low/medium risk changes:

```markdown
# DEC-LITE-#### — [Brief Title]

**Date:** YYYY-MM-DD | **Risk:** Low/Medium | **Owner:** [Name]

## Decision
[One paragraph: what we decided and why]

## Alternatives Considered
- Option A — rejected because [one line]
- Option B — rejected because [one line]

## Impact
- Changes: [list affected artefacts]
- Risks: [key risks and mitigations]

## Verification
- [ ] [Specific verification steps]
```

### Cognitive Load Reduction

**Before (METHOD-0002 excerpt):**

> "Run the automated harvester (`tools/rjw_idd_evidence_harvester.py`) capturing raw output. Store logs under `logs/discovery-harvest/` (or your chosen path) and validate results with `scripts/validate_evidence.py`. Promote curated entries into `research/evidence_index.json` via `scripts/promote_evidence.py`. Update requirement ledger entries with new evidence IDs and log the harvest in `docs/change-log.md`."

**After:**

> **Harvest Evidence**
>
> ```bash
> # 1. Run harvester
> python tools/rjw_idd_evidence_harvester.py
>
> # 2. Validate and promote
> python scripts/validate_evidence.py
> python scripts/promote_evidence.py
>
> # 3. Update logs
> [Auto-generated change log entry suggested]
> ```

## 5. Automation over Ceremony

### Automated Defaults

Replace manual steps with automated defaults where possible:

| Manual Step | Automated Alternative |
|-------------|----------------------|
| Create change log entry | Auto-generate from commit + template |
| Assign artefact IDs | Auto-increment from registry |
| Link cross-references | Auto-link on save |
| Check format compliance | Pre-commit hooks |
| Verify ID uniqueness | CI validation |
| Calculate audit tags | Auto-increment on audit |

### Smart Templates

Templates should pre-populate based on context:

```markdown
# DEC-0042 — [Auto-suggested: based on branch name or recent commits]

**Decision Date:** 2024-11-29 [Auto-filled]
**Participants:** [Auto-filled from CODEOWNERS or recent activity]

## Problem Statement
[Cursor starts here]

## Candidate Thoughts
1. [Template suggests common option patterns]

## Cross-Links
- [Auto-linked: recently changed specs]
- [Auto-linked: related evidence]
```

### Pre-Commit Verification

Automate verification that currently requires manual checking:

```yaml
# .pre-commit-config.yaml additions
repos:
  - repo: local
    hooks:
      - id: check-artefact-ids
        name: Verify artefact ID format and uniqueness
        entry: scripts/validate_ids.py
        language: python
        files: '\.(md|json|csv)$'

      - id: check-cross-refs
        name: Verify cross-references resolve
        entry: scripts/validate_refs.py
        language: python
        files: '\.md$'

      - id: suggest-change-log
        name: Suggest change log entry
        entry: scripts/suggest_change_log.py
        language: python
        stages: [pre-push]
```

## 6. Streamlined Checklists

### Universal Pre-Flight (All Changes)

```markdown
## Pre-Flight Checklist

- [ ] Risk level classified: ________
- [ ] Appropriate process path selected
- [ ] Required approvals identified
```

### Minimal/Low Risk Checklist

```markdown
## Quick Checklist

- [ ] Automated checks pass
- [ ] Change log updated (if Low risk)
- [ ] Commit message follows convention
```

### Medium Risk Checklist

```markdown
## Standard Checklist

- [ ] Pre-flight complete
- [ ] Tests cover changes
- [ ] Peer review obtained
- [ ] Documentation current
- [ ] Change log entry complete
```

### High/Critical Risk Checklist

> Use full METHOD-0002 checklists with Critical Risk additions for security review.

## 7. Quick-Start Pathways

### Pathway A: Documentation Update (Minimal Risk)

```text
1. Edit documentation
2. Commit with message: "docs: [brief description]"
3. Auto-verification runs
4. Merge on pass
```

**Time:** 5 minutes

### Pathway B: Bug Fix (Low-Medium Risk)

```text
1. Classify risk (use flowchart in Section 3)
2. Create failing test
3. Implement fix
4. Verify fix + no regressions
5. Update change log
6. Request review (Medium) or auto-merge (Low)
```

**Time:** 30 minutes to 2 hours

### Pathway C: New Feature (High Risk)

```text
1. Create DEC-#### with options analysis
2. Run parallel spec tracks:
   - Functional spec
   - Quality/test spec
   - Security review (if needed)
3. Sync checkpoint
4. Implement with test coverage
5. Update living documentation
6. Full verification + review
7. Stage deployment + monitor
```

**Time:** 1-5 days depending on scope

### Pathway D: Critical Change (Critical Risk)

```text
1. Full Pathway C requirements
2. Security & Privacy Liaison review
3. Governance Board approval
4. Rollback plan documented and tested
5. Staged deployment with extended monitoring
6. Post-deployment verification
```

**Time:** 5-15 days including staged rollout

## 8. Metrics and Feedback

### Efficiency Metrics

Track to validate streamlining effectiveness:

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Low-risk cycle time | 2 days | 30 min | Commit to merge |
| Medium-risk cycle time | 5 days | 2 days | Start to merge |
| Documentation overhead | 40% of effort | 15% | Time tracking |
| Process compliance | — | >95% | Audit sampling |
| Rework due to process skip | — | <5% | Incident tracking |

### Feedback Collection

After each completed work item, capture:

```markdown
## Streamlining Feedback

**Work Item:** [ID or description]
**Risk Level:** [Minimal/Low/Medium/High/Critical]
**Process Path:** [A/B/C/D]

**Worked Well:**
- [What made this efficient?]

**Friction Points:**
- [What slowed things down unnecessarily?]

**Suggestions:**
- [How could the process improve?]
```

Aggregate feedback quarterly to refine pathways.

## 9. Integration with Trust Framework

Streamlined processes interact with METHOD-0006 trust levels:

| Trust Level | Process Access |
|-------------|----------------|
| Level 0 | Pathway A only; all others require approval |
| Level 1 | Pathways A-B; C-D require human co-pilot |
| Level 2 | Pathways A-C; D requires human approval |
| Level 3 | All pathways; serves as approver for others |

Risk classification by agents verified against trust level authorization.

## 10. Companion Assets

- `METHOD-0001` — Core methodology principles
- `METHOD-0002` — Full checklists (used for High/Critical paths)
- `METHOD-0006` — Agent trust framework
- `templates/DEC-LITE-template.md` — Lightweight decision template
- `templates/CHANGE-LOG-ENTRY-template.md` — Simplified change log format

## 11. Method Adoption Steps

1. Classify existing work queue by risk level
2. Route new work through appropriate pathway
3. Set up pre-commit hooks for automated verification
4. Update templates with progressive disclosure structure
5. Track efficiency metrics for first quarter
6. Refine pathways based on feedback
7. Document lessons learned in methodology updates

By implementing these streamlined operations, teams can move faster on routine work while maintaining full governance for decisions that matter.
