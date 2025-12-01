# METHOD-0002 — RJW-IDD Unified Lifecycle & Checklists

Use these checklists to force the same lifecycle run that originally created RJW-IDD. Every box must be checked before advancing to the next phase. Record completion in `docs/change-log.md` and append the relevant `DEC-####` entry each time you revisit the method.

> **TL;DR:** This document is the single source of truth for all process checklists—Standard, Streamlined, and Prototype pathways. Start by classifying your risk level below, then follow the appropriate pathway.

---

## 1. Risk Selection Logic — Entry Point

**Start here.** Classify your change risk level first, then follow the appropriate pathway.

### Risk Classification Flowchart

```text
START
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ Is this prototype/POC/spike work?                           │
│ (Not intended for immediate production)                     │
└─────────────────────────────────────────────────────────────┘
  │ Yes                                        │ No
  ▼                                            ▼
Prototype Mode                    ┌─────────────────────────────────────┐
(Section 6)                       │ Does this change behavior?          │
                                  └─────────────────────────────────────┘
                                    │ No                     │ Yes
                                    ▼                        ▼
                              Minimal Risk             ┌─────────────────────────────────────┐
                              (Section 2.1)            │ Is the change easily reversible?    │
                                                       └─────────────────────────────────────┘
                                                         │ Yes                  │ No
                                                         ▼                      ▼
                                                   Low Risk            ┌─────────────────────────────────────┐
                                                   (Section 2.2)       │ Does it affect multiple components  │
                                                                       │ or external interfaces?             │
                                                                       └─────────────────────────────────────┘
                                                                         │ No                  │ Yes
                                                                         ▼                     ▼
                                                                   Medium Risk        ┌─────────────────────────────────────┐
                                                                   (Section 2.3)      │ Does it involve security, data      │
                                                                                      │ integrity, or availability?         │
                                                                                      └─────────────────────────────────────┘
                                                                                        │ No             │ Yes
                                                                                        ▼                ▼
                                                                                  High Risk        Critical Risk
                                                                                  (Section 3)      (Section 4)
```

### Risk Classification Summary

| Risk Level | Characteristics | Examples | Pathway |
|------------|-----------------|----------|---------|
| **Minimal** | No behavior change; typo/formatting | Doc typos, comment updates, formatting | Section 2.1 |
| **Low** | Additive only; easily reversible | New tests, new docs, config defaults | Section 2.2 |
| **Medium** | Behavior change within component | Bug fixes, refactors, internal API changes | Section 2.3 |
| **High** | Cross-component or user-visible | Feature additions, external API changes | Section 3 |
| **Critical** | Security, data, or availability | Auth changes, data migrations, prod config | Section 4 |
| **Prototype** | POC/spike/experimental (not production) | Feasibility studies, technology evaluation | Section 6 |

---

## 2. Streamlined Pathways (Minimal/Low/Medium Risk)

### 2.1 Minimal Risk Path (5 min)

**Use for:** Non-behavioral changes (typo fixes, formatting, comment updates)

**Process:** Commit → Auto-verify → Merge

- [ ] Commit with message: `docs: [brief description]`
- [ ] Automated lint/format check passes
- [ ] Merge on pass

**Documentation:** Commit message only

**Approval:** None (automated merge permitted)

### 2.2 Low Risk Path (30 min)

**Use for:** Additive, easily reversible changes (new tests, new docs, config defaults)

**Process:** Commit → Auto-verify → Change log → Merge

- [ ] Automated checks pass
- [ ] Change log entry added (simplified format)
- [ ] Artefact IDs follow scheme
- [ ] Optional peer review

**Documentation:**
- Change log row (simplified)
- Link to commit

**Approval:** Auto-approve if checks pass; optional peer review

### 2.3 Medium Risk Path (2 hours)

**Use for:** Behavior changes within a single component (bug fixes, refactors, internal API changes)

**Process:** Commit → Verify → Review → Change log → Merge

- [ ] Risk classification documented in commit
- [ ] Full automated verification suite passes
- [ ] Peer review completed
- [ ] Tests cover changes
- [ ] Documentation updated
- [ ] Standard change log entry added
- [ ] One reviewer sign-off obtained

**Documentation:**
- Standard change log entry
- Updated specs if behavior changed
- Test coverage report

**Approval:** One reviewer sign-off

---

## 3. High Risk Path — Full Discovery + Execution Loop

**Use for:** Cross-component or user-visible changes (feature additions, external API changes)

### 3.1 Phase 0 — Governance Setup

- [ ] `docs/decisions/` directory exists with sequential `DEC-####.md` records; new work starts by drafting a decision stub.
- [ ] `docs/change-log.md` initialised and ready to track `change-YYYYMMDD-##` entries.
- [ ] Roles confirmed (Evidence Lead, Spec Architect, Security Liaison, Implementation Wrangler).
- [ ] Stage audit log initialised (`logs/LOG-0001-stage-audits.md`) with audit tag `⟦audit-id:1⟧` reserved.

### 3.2 Layer 1 — Discovery (Research + Specification)

#### Research Loop

1. **Plan**
   - [ ] Draft `DEC-####` describing the harvest goal, sources, and date range.
   - [ ] Update `research/evidence_tasks.json` with focus areas.
2. **Harvest & Curate**
   - [ ] Run the automated harvester (`tools/rjw_idd_evidence_harvester.py`) capturing raw output.
   - [ ] Promote curated entries into `research/evidence_index.json` and log any gaps.
3. **Validate & Log**
   - [ ] Execute validators (`scripts/validate_evidence.py`, `scripts/validate_ids.py --paths research/evidence_index.json`).
   - [ ] Append Change Log row in `docs/change-log.md` detailing harvest, validator status, and outstanding gaps.
   - [ ] Complete `⟦audit-id:n⟧ <reflect/>` entry in stage audit log summarising coverage and open items.

#### Specification Loop

1. **Prep**
   - [ ] Draft or update `DEC-####` capturing spec scope and trade-offs (e.g., provisional observability guidance).
   - [ ] Ensure requirement ledger template is ready.
2. **Author & Align**
   - [ ] Create/update specs across functional, quality, observability, security, integration, cost bands.
   - [ ] Refresh the requirement ledger linking each work item ID to evidence, specs, and planned tests.
   - [ ] Update living documentation reconciliation log with any outstanding doc gaps.
3. **Validate & Log**
   - [ ] Run ID validator on updated specs/ledger.
   - [ ] Record change in `docs/change-log.md` with linked `DEC-####` and validation results.
   - [ ] Capture `⟦audit-id:n⟧ <reflect/>` stage summary noting remaining assumptions and scheduled micro-harvests.

#### Discovery Exit Gate (must be true)

- [ ] Curated evidence meets recency requirement; gaps tracked to owners and due dates.
- [ ] Requirement ledger, specs, and reconciliation log are aligned and reference the supporting evidence IDs.
- [ ] Scope freeze captured in latest `DEC-####`; Discovery exit signed by Evidence Lead and Spec Architect.

### 3.3 Layer 2 — Execution

1. **Readiness**
   - [ ] Implementation decision (`DEC-####`) crafted describing scope of the sprint/run.
   - [ ] Tooling (test guard, consent manager, metric emitter) configured locally or ported to the new environment.
2. **Execution Loops**
   - [ ] For each change, write failing tests first; record guard output or log refusal until tests exist.
   - [ ] Update documentation (standards, runbooks, implementation notes) alongside code modifications.
   - [ ] Archive integration transcripts for cross-system changes under `artifacts/integration/...`.
   - [ ] Maintain consent records and metrics receipts when instrumentation is exercised.
3. **Validation & Log**
   - [ ] Run full test suite (`python -m unittest ...` or equivalent) and capture artefacts.
   - [ ] Update `docs/change-log.md` with guard/test results, consent receipt paths, and transcript locations.
   - [ ] Add `⟦audit-id:n⟧ <reflect/>` noting whether observability, security, and cost controls remain intact.
4. **Exit Gate (must be true)**
   - [ ] Tests, docs, and transcripts present for the change set.
   - [ ] Telemetry consent artefacts up to date.
   - [ ] Stage audit signed by Implementation Wrangler and Security Liaison.

### 3.4 Parallel-First Architecture

Maximize efficiency by running independent tracks concurrently. Restructure work to reduce bottlenecks:

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

**Independent Tracks (may run concurrently):**

- Functional spec ↔ Quality spec ↔ Security spec ↔ Ops spec
- Unit tests ↔ Integration tests ↔ Documentation updates
- Different feature implementations (non-overlapping scope)

**Sync Points (required checkpoints):**

| Sync Point | Purpose | Participants | Duration |
|------------|---------|--------------|----------|
| Post-Research | Align on findings before spec work | Evidence Lead, Spec Architect | 30 min |
| Pre-Implementation | Confirm specs compatible; resolve conflicts | All spec authors | 1 hour |
| Pre-Deploy | Verify all streams complete and consistent | Governance Sentinel | 15 min |

**Dependent Tracks (must wait):**

- Implementation → after spec sync
- Deployment → after all verification
- Scope changes → after governance review

**Time Savings Estimate:**

| Scenario | Sequential | Parallel | Savings |
|----------|------------|----------|---------|
| Typical feature | 10 days | 6 days | 40% |
| Minor enhancement | 3 days | 2 days | 33% |
| Major initiative | 30 days | 18 days | 40% |

### 3.5 Continuous Governance (applies every cycle)

- [ ] Every new insight spawns a `DEC-####` log before being institutionalised.
- [ ] Stage audits kept current; every follow-up noted in `logs/LOG-0001-stage-audits.md` is tracked to closure.
- [ ] Change Log verification column always references tangible artefacts (validator outputs, logs, receipts).

Use this checklist pack as a gatekeeper. If any box stays unchecked, loop back, capture a new decision, or schedule additional Discovery work before progressing.

---

## 4. Critical Risk Path — Enhanced Governance

**Use for:** Security, data integrity, or availability changes (auth changes, data migrations, production config)

**Process:** Full Discovery + Execution loop + Security review

**All High Risk requirements apply, plus:**

- [ ] Security & Privacy Liaison review completed
- [ ] Rollback plan documented and tested
- [ ] Staged deployment strategy defined
- [ ] Post-deployment verification plan ready

**Additional Documentation:**
- Security impact assessment
- Rollback procedure
- Staged deployment log
- Post-deployment verification results

**Approval:** Governance Board + Security sign-off

---

## 5. Agent Trust Integration

When AI agents execute these checklists, apply trust-level constraints:

### Trust Ladder Model

| Trust Level | Name | Autonomy | Pathway Access |
|-------------|------|----------|----------------|
| Level 0 | Supervised | All actions require human approval | Minimal Risk only; all others require approval |
| Level 1 | Guided | Pre-approved categories proceed automatically | Minimal/Low Risk; Medium+ require human co-pilot |
| Level 2 | Autonomous | Operates independently with post-hoc review | Minimal/Low/Medium Risk; High+ require approval |
| Level 3 | Trusted Partner | Participates in planning and prioritization | All pathways; serves as approver for others |

### Trust Level Promotion Criteria

**To Level 1 (from Level 0):**
- [ ] 10+ consecutive proposals approved without modification
- [ ] Zero rejected proposals due to safety/quality issues
- [ ] Demonstrated understanding of project context
- [ ] Completed at least one full Discovery→Execution cycle under supervision

**To Level 2 (from Level 1):**
- [ ] 50+ actions executed at Level 1 without escalation failures
- [ ] Escalation judgment accuracy ≥95%
- [ ] Zero guardrail violations
- [ ] Positive assessment from Governance Sentinel on audit samples

**To Level 3 (from Level 2):**
- [ ] 90+ days at Level 2 without demotion triggers
- [ ] Audit findings consistently meet or exceed expectations
- [ ] Demonstrated judgment in ambiguous situations
- [ ] Cross-project track record available

### Self-Classification Risk Levels (Level 2+ Agents)

| Risk Level | Agent Authority | Documentation Required | Review Timing |
|------------|-----------------|------------------------|---------------|
| Low | Execute immediately | Standard change log entry | Weekly batch |
| Medium | Execute with notification | Detailed rationale + change log | 24-hour async |
| High | Propose only; await approval | Full DEC-#### decision record | Synchronous |

### Demotion Triggers

**Level 2 → Level 1:**
- Risk misclassification (high-risk action classified as low/medium)
- Audit finding of incomplete documentation
- Guardrail violation (any severity)
- Scope creep without escalation

**Level 3 → Level 2:**
- Strategic recommendation leads to significant rework
- Trust calibration audit finds overconfidence
- Methodology contribution rejected due to safety concerns

---

## 6. Lifecycle Variant: Prototype Mode

**Use for:** Proof-of-concept, spike, feasibility study, or experimental work that isn't intended for immediate production.

### 6.1 When to Use Prototype Mode

| Prototype Type | Description | Default Time-Box | Maximum |
|----------------|-------------|------------------|---------|
| **Quick Spike** | Time-boxed investigation to reduce uncertainty | 2–3 days | 1 week |
| **Standard POC** | Validating a technical approach or architecture | 1–2 weeks | 3 weeks |
| **Complex Feasibility** | Determining if a capability is achievable within constraints | 2–3 weeks | 4 weeks |
| **Technology Evaluation** | Comparing frameworks, libraries, or approaches hands-on | 1–2 weeks | 3 weeks |

**Hard Limit:** No prototype may exceed 4 weeks without a forced exit decision. If more time is needed, formally archive or promote the work and start fresh with a new PROTO record.

### 6.2 Distinction from Production Pathways

| Aspect | Prototype Mode | Production Paths (Sections 2-4) |
|--------|----------------|--------------------------------|
| **Goal** | Learn / Prove / Explore | Ship / Deploy / Maintain |
| **Time Horizon** | Days to weeks (max 4 weeks) | Variable (driven by scope) |
| **Quality Bar** | "Good enough to learn" | "Ready for users" |
| **Review** | Self-review acceptable | Peer review required (Medium+) |
| **Testing** | Smoke tests sufficient | Full coverage expected |
| **Documentation** | Inline comments + PROTO record | Full specifications and runbooks |
| **Exit** | Promote / Archive / Abandon | Release / Maintain |

### 6.3 Keep/Flex/Unknown Tagging System

Semantic tags help distinguish between essential prototype elements and temporary scaffolding during code review and when promoting to production.

| Tag | Variants | Meaning | Action on Promotion |
|-----|----------|---------|---------------------|
| **Keep** | `⟦keep⟧` or `[KEEP]` | Core to the proof-of-concept; essential for the prototype to function | Preserve and enhance to production quality |
| **Flex** | `⟦flex⟧` or `[FLEX]` | Scaffolding, shortcuts, or experimental approaches | Replace with production-grade implementation |
| **Unknown** | `⟦unknown⟧` or `[UNKNOWN]` | Uncertain whether essential; needs evaluation | Review during promotion; decide keep or replace |

**Example in code:**

```python
# ⟦keep⟧ Core connection pooling logic - proven to handle load
class ConnectionPool:
    def __init__(self, max_connections):
        self.pool = []  # ⟦flex⟧ Replace with thread-safe queue
        self.max = max_connections

    # ⟦unknown⟧ Retry logic may need adjustment for production
    def get_connection(self, retry=3):
        ...
```

**Tagging Guidelines:**

1. **Tag at the component level:** Tag functions, classes, or modules rather than individual lines
2. **Be honest about unknowns:** It's better to mark something `[UNKNOWN]` than guess wrong
3. **Update tags as you learn:** If you discover a `[FLEX]` item is actually essential, change it to `[KEEP]`
4. **Document rationale:** Brief notes explaining why something is tagged a certain way help during promotion

### 6.4 Relaxed Gates in Prototype Mode

**What Is NOT Required:**

| Gate | Production Requirement | Prototype Allowance |
|------|------------------------|---------------------|
| **Peer Review** | Required (Medium+ risk) | Self-review acceptable |
| **Test Coverage** | Full coverage expected | Smoke tests sufficient |
| **Documentation** | Specs, runbooks, full docs | Inline comments + PROTO record |
| **Security Review** | Required for security-relevant | Not required unless handling real user data |
| **Performance Benchmarks** | Expected for affected areas | Not required unless performance is the thing being proven |
| **Full DEC Record** | Required (Medium+ risk) | PROTO record sufficient |
| **Evidence Harvesting** | Full research loop | Prior knowledge or quick research acceptable |

**What IS Still Required:**

| Requirement | Rationale |
|-------------|-----------|
| **PROTO decision record** | Ensures intent is captured; prevents drift |
| **Keep/Flex tagging** | Enables informed promotion decisions |
| **Time-box adherence** | Prevents prototypes from becoming shadow production systems |
| **Exit decision** | Every prototype must end with Promote, Archive, or Abandon |
| **Basic functionality** | Code should run and demonstrate the intended capability |
| **No real user data** | Unless explicitly authorized with proper consent handling |

**Security Exceptions:** If the prototype must handle real user data or integrate with production systems, Security review IS required. Consider using the Low Risk production path (Section 2.2) instead.

### 6.5 Prototype Workflow

```text
1. Receive or propose prototype assignment
2. Draft PROTO-#### record with intent, criteria, time-box
3. Work iteratively toward success criteria
   - Tag components as ⟦keep⟧/⟦flex⟧/⟦unknown⟧ as you build
   - Self-review; iterate quickly
   - Document surprises and learnings
4. Assess against success criteria at midpoint
5. At time-box end or completion:
   - Evaluate against success criteria
   - Recommend exit decision with rationale
   - If promoting: identify DEC-#### pathway and risk level
6. Update PROTO record with exit decision
```

### 6.6 Exit Options

Every prototype must conclude with one of three exit decisions documented in the PROTO record.

**Option 1: Promote to Production**

When to choose: The prototype proved its hypothesis and the approach should be productionized.

1. Review all `[KEEP]`, `[FLEX]`, and `[UNKNOWN]` tags
2. Create a `DEC-####` decision record referencing the PROTO record as evidence
3. Initiate full production pathway at appropriate risk level (Sections 2-4)
4. Queue `[FLEX]` items for production-grade replacement
5. Evaluate `[UNKNOWN]` items and classify as keep or flex
6. Update PROTO record status to "Promoted" with link to DEC-####

**Traceability Chain:**
```text
PROTO-#### (evidence) → DEC-#### (decision) → Full production execution
```

**Option 2: Archive**

When to choose: The prototype provided valuable learnings but won't be productionized now.

1. Document learnings in PROTO record
2. Capture what worked, what didn't, and why archiving vs promoting
3. Preserve code in a designated archive location or branch
4. Update PROTO record status to "Archived"
5. Ensure learnings are findable for future reference

**Option 3: Abandon**

When to choose: The prototype proved the approach doesn't work or is not worth pursuing.

1. Document why the approach failed in PROTO record
2. Capture lessons learned (negative knowledge is valuable)
3. Code may be deleted (no preservation requirement)
4. Update PROTO record status to "Abandoned"

### 6.7 Agent Trust Adjustments for Prototype Work

Prototype mode does not change an agent's trust level, but it does adjust how that trust is applied:

| Trust Level | Standard Mode | Prototype Mode |
|-------------|---------------|----------------|
| Level 0 | All actions require approval | PROTO-scoped actions may batch for approval |
| Level 1 | Pre-approved categories only | All prototype work is pre-approved within scope |
| Level 2 | Autonomous with post-hoc review | Autonomous; review at prototype exit |
| Level 3 | Strategic participation | May approve PROTO records and exit decisions |

### 6.8 Working on Promoted Prototype Code

When encountering code promoted from a prototype (referenced by PROTO-#### in DEC-####):

- **`[KEEP]` code:** Preserve core logic; may enhance for production quality
- **`[FLEX]` code:** Explicitly marked for replacement; use standard production approach
- **`[UNKNOWN]` code:** Stop, evaluate, reclassify as KEEP or FLEX, then proceed

---

## 7. Human-Centered Artefact Design

### 7.1 Progressive Disclosure Structure

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

### 7.2 Simplified Change Log Format

Replace verbose change log entries with scannable format:

**Simplified Format:**

| ID | Date | Risk | Summary | Links |
|----|------|------|---------|-------|
| 2024-03-27-01 | 2024-03-27 | High | Anchor governance artefacts | [DEC-0001] [audit:1] |

Detailed description moves to linked decision record.

### 7.3 Visual Checklists

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

### 7.4 Automation over Ceremony

Replace manual steps with automated defaults where possible:

| Manual Step | Automated Alternative |
|-------------|----------------------|
| Create change log entry | Auto-generate from commit + template |
| Assign artefact IDs | Auto-increment from registry |
| Link cross-references | Auto-link on save |
| Check format compliance | Pre-commit hooks |
| Verify ID uniqueness | CI validation |
| Calculate audit tags | Auto-increment on audit |

---

## 8. Quick-Start Pathways Summary

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
1. Classify risk (use flowchart in Section 1)
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

### Pathway E: Prototype/POC (Prototype Mode)

```text
1. Draft PROTO-#### record with intent, criteria, time-box
2. Iterate rapidly toward success criteria
3. Tag components as Keep/Flex/Unknown
4. Self-review; document learnings
5. At time-box end: Promote, Archive, or Abandon
```

**Time:** 2 days to 4 weeks (hard limit)

---

## 9. Related Documentation

- `core/METHOD-0001-core-method.md` — Core methodology principles
- `governance/METHOD-0003-role-handbook.md` — Role definitions and responsibilities
- `operations/METHOD-0004-ai-agent-workflows.md` — AI Agent Handbook (unified agent rules)
- `operations/METHOD-0005-operations-production-support.md` — Operations and production support
- `operations/METHOD-0006-context-curation-engine.md` — Context Curation Engine
- `templates/DEC-LITE-template.md` — Lightweight decision template for Low/Medium risk
- `templates/PROTO-template.md` — Prototype record template
- `templates/AGENT-TRUST-template.md` — Trust level change record template
- `templates/context/CTX-INDEX-template.md` — Task context index template
- `templates/context/LIVING-DOCS-template.md` — Living documentation template
