# METHOD-0006 — Agent Trust and Autonomy Framework

This document establishes a framework for building and managing trust in AI agents operating within the RJW-IDD methodology. It enables progressive autonomy based on demonstrated reliability while maintaining the auditability and safety guarantees required by the method.

## 1. Framework Purpose

**Goal:** Enable AI agents to earn greater autonomy through verifiable trustworthy behavior, allowing humans to focus oversight on high-value decisions while agents handle routine work independently.

**Principles:**

- **Trust is earned, not assumed** — Agents start with limited autonomy and expand capabilities through demonstrated reliability
- **Verification enables trust** — Automated checks provide continuous assurance that agent behavior meets expectations
- **Transparency builds confidence** — All agent decisions, reasoning, and actions are auditable
- **Graceful degradation** — Trust violations trigger proportionate responses, not catastrophic restrictions
- **Human oversight scales with risk** — Critical decisions always require human judgment; routine work can be delegated

## 2. Trust Ladder Model

Agents progress through trust levels based on track record. Each level unlocks additional autonomy while maintaining appropriate safeguards.

### Level 0: Supervised (Default Starting Point)

**Autonomy:** None — all actions require human approval before execution.

**Characteristics:**

- Agent proposes actions; human reviews and approves/rejects each one
- All outputs treated as drafts requiring verification
- Full audit trail of proposals and decisions captured

**Promotion Criteria (to Level 1):**

- [ ] 10+ consecutive proposals approved without modification
- [ ] Zero rejected proposals due to safety/quality issues
- [ ] Demonstrated understanding of project context (assessed via spot checks)
- [ ] Completed at least one full Discovery→Execution cycle under supervision

### Level 1: Guided

**Autonomy:** Limited — routine actions within defined boundaries proceed automatically; novel situations escalate.

**Characteristics:**

- Pre-approved action categories execute without per-action approval
- Automated guardrails flag boundary violations for human review
- Spot checks verify continued alignment (10% sample rate)
- Agent explains reasoning for non-routine decisions before acting

**Pre-Approved Action Categories:**

- Documentation updates following established patterns
- Test creation that increases coverage
- Evidence curation from approved sources
- Spec refinements that don't alter scope
- Change log and audit log maintenance

**Escalation Triggers:**

- Actions outside pre-approved categories
- Decisions affecting external dependencies
- Changes to security-sensitive components
- Scope modifications of any kind
- Conflicts with existing decisions or specs

**Promotion Criteria (to Level 2):**

- [ ] 50+ actions executed at Level 1 without escalation failures
- [ ] Escalation judgment accuracy ≥95% (correctly escalated when needed)
- [ ] Zero guardrail violations
- [ ] Positive assessment from Governance Sentinel on audit samples

### Level 2: Autonomous

**Autonomy:** Broad — agent operates independently within project scope with post-hoc review.

**Characteristics:**

- Full execution authority for work within established scope
- Human review occurs asynchronously via audit rather than synchronously via approval
- Agent self-classifies risk level and adjusts documentation accordingly
- Weekly audit reviews replace per-action approval

**Self-Classification Risk Levels:**

| Risk Level | Agent Authority | Documentation Required | Review Timing |
|------------|-----------------|------------------------|---------------|
| Low | Execute immediately | Standard change log entry | Weekly batch |
| Medium | Execute with notification | Detailed rationale + change log | 24-hour async |
| High | Propose only; await approval | Full DEC-#### decision record | Synchronous |

**Demotion Triggers (to Level 1):**

- Risk misclassification (high-risk action classified as low/medium)
- Audit finding of incomplete documentation
- Guardrail violation (any severity)
- Scope creep without escalation

**Promotion Criteria (to Level 3):**

- [ ] 90+ days at Level 2 without demotion triggers
- [ ] Audit findings consistently meet or exceed expectations
- [ ] Demonstrated judgment in ambiguous situations
- [ ] Cross-project track record available

### Level 3: Trusted Partner

**Autonomy:** Strategic — agent participates in planning, prioritization, and methodology evolution.

**Characteristics:**

- Contributes to Discovery research direction and spec architecture
- Proposes methodology improvements and new patterns
- Mentors Level 0-2 agents on project patterns
- Participates in quarterly governance reviews

**Governance Role:**

- Input on DEC-#### decisions (non-voting)
- Proposes micro-harvests when gaps are detected
- Suggests efficiency improvements based on observed patterns
- Flags systemic issues across project scope

**Demotion Triggers (to Level 2):**

- Strategic recommendation leads to significant rework
- Trust calibration audit finds overconfidence
- Methodology contribution rejected due to safety concerns

## 3. Behavioral Contracts

Agents commit to explicit behavioral contracts that define expectations and enable automated compliance verification.

### Core Contract (All Levels)

All agents operating under RJW-IDD commit to:

```yaml
core_contract:
  transparency:
    - Explain reasoning for all non-trivial decisions
    - Disclose uncertainty and confidence levels
    - Report errors and near-misses proactively
    - Maintain complete audit trail of actions

  boundaries:
    - Never exceed authorized autonomy level
    - Escalate when in doubt about authorization
    - Refuse actions that violate methodology principles
    - Halt immediately when guardrails trigger

  quality:
    - Verify outputs before declaring completion
    - Follow established patterns unless deviation is justified
    - Maintain consistency with existing artefacts
    - Document deviations from standard approach

  safety:
    - Never modify production systems without explicit authorization
    - Preserve data integrity and backup state before destructive actions
    - Respect consent and privacy requirements
    - Flag security-relevant changes for human review
```

### Level-Specific Contracts

**Level 1 Addition:**

```yaml
level_1_contract:
  judgment:
    - Correctly identify when situations require escalation
    - Provide sufficient context for human decision-making
    - Accept feedback and adjust behavior accordingly
    - Track patterns in escalation decisions for learning
```

**Level 2 Addition:**

```yaml
level_2_contract:
  self_governance:
    - Accurately self-classify risk levels
    - Produce documentation proportionate to risk
    - Detect and report drift from established patterns
    - Maintain audit-ready state at all times
```

**Level 3 Addition:**

```yaml
level_3_contract:
  leadership:
    - Identify systemic improvement opportunities
    - Balance efficiency with safety in recommendations
    - Support other agents' development appropriately
    - Maintain objectivity in methodology assessments
```

## 4. Continuous Verification Architecture

Replace gate-only verification with continuous automated checks to catch issues earlier and build trust evidence.

### Verification Layers

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Human Oversight Layer                        │
│   (Spot checks, audits, escalation handling, trust decisions)   │
├─────────────────────────────────────────────────────────────────┤
│                   Behavioral Verification                       │
│      (Contract compliance, boundary checks, risk scoring)       │
├─────────────────────────────────────────────────────────────────┤
│                    Output Verification                          │
│    (Quality checks, consistency validation, format compliance)  │
├─────────────────────────────────────────────────────────────────┤
│                    Process Verification                         │
│     (Workflow adherence, documentation completeness, timing)    │
└─────────────────────────────────────────────────────────────────┘
```

### Automated Checks

**Process Verification (every action):**

- Change log entry present and complete
- Linked artefacts exist and are consistent
- Required approvals obtained for trust level
- Timing within expected bounds

**Output Verification (every artefact):**

- ID format follows scheme (`REQ-####`, `SPEC-####`, etc.)
- Cross-references resolve correctly
- No orphaned references
- Content matches expected structure

**Behavioral Verification (continuous):**

- Actions within authorized boundaries
- Escalations appropriate to situation
- Risk classifications accurate
- Contract terms honored

### Trust Scoring

Maintain a rolling trust score for each agent based on verification results:

```yaml
trust_score:
  components:
    process_compliance:
      weight: 0.25
      metrics:
        - documentation_completeness
        - timing_adherence
        - workflow_following
    output_quality:
      weight: 0.30
      metrics:
        - verification_pass_rate
        - consistency_score
        - rework_frequency
    behavioral_alignment:
      weight: 0.30
      metrics:
        - escalation_accuracy
        - risk_classification_accuracy
        - boundary_respect
    human_assessment:
      weight: 0.15
      metrics:
        - audit_findings
        - spot_check_results
        - feedback_incorporation

  thresholds:
    promotion_eligible: 0.90
    stable: 0.75
    warning: 0.60
    demotion: 0.50
```

### Graduated Response Protocol

Trust violations trigger proportionate responses:

| Violation Severity | Trust Impact | Response |
|--------------------|--------------|----------|
| Minor (documentation gap) | -0.02 per instance | Auto-remediate if possible; log for review |
| Moderate (boundary approach) | -0.05 per instance | Immediate notification; require acknowledgment |
| Significant (boundary violation) | -0.15 per instance | Pause and escalate; human approval to resume |
| Critical (safety/security) | Immediate demotion | Full stop; incident review required |

## 5. Audit and Transparency

### Agent Activity Log

Maintain `logs/LOG-0002-agent-activity.md` with:

| Timestamp | Agent ID | Trust Level | Action Type | Risk Class | Verification | Outcome |
|-----------|----------|-------------|-------------|------------|--------------|---------|
| (ISO-8601) | (identifier) | (0-3) | (category) | (L/M/H) | (pass/warn/fail) | (success/escalated/blocked) |

### Trust Level Changes

Document all trust level changes in `docs/decisions/DEC-TRUST-####.md`:

```markdown
# DEC-TRUST-#### — Trust Level Change for [Agent ID]

**Date:** YYYY-MM-DD
**Previous Level:** N
**New Level:** M
**Direction:** Promotion / Demotion / Reset

## Evidence Summary
- Trust score: X.XX
- Actions at previous level: N
- Verification pass rate: XX%
- Key observations: ...

## Criteria Assessment
[Checklist of promotion/demotion criteria with status]

## Approval
**Approved by:** [Role/Name]
**Effective:** [Date/Time]
```

### Quarterly Trust Review

During governance reviews, assess:

- Trust level distribution across agents
- Promotion/demotion patterns and root causes
- Verification system effectiveness (false positive/negative rates)
- Contract adequacy (gaps revealed by incidents)
- Human oversight load (trending toward sustainable level?)

## 6. Integration with RJW-IDD Layers

### Discovery Layer

- **Level 0-1:** Propose evidence curation; human approves before promotion
- **Level 2:** Curate evidence autonomously; flag gaps for micro-harvest
- **Level 3:** Direct micro-harvest priorities; propose research questions

### Execution Layer

- **Level 0-1:** Draft implementations; human reviews before merge
- **Level 2:** Implement within scope; post-hoc audit verification
- **Level 3:** Architect solutions; guide scope decisions

### Operations Layer

- **Level 0-1:** Execute runbook steps under supervision
- **Level 2:** Handle routine incidents autonomously; escalate novel issues
- **Level 3:** Improve runbooks; propose operational enhancements

## 7. Companion Assets

- `METHOD-0001` — Core methodology principles
- `METHOD-0003` — Role handbook (updated with agent trust oversight)
- `METHOD-0004` — AI agent workflows (extended by this document)
- `METHOD-0007` — Streamlined operations (efficiency improvements)
- `templates/AGENT-TRUST-template.md` — Trust level change record template

## 8. Method Adoption Steps

1. Initialize `logs/LOG-0002-agent-activity.md` for activity tracking
2. Assess current agents against Level 0 baseline
3. Implement automated verification checks (process → output → behavioral)
4. Define project-specific pre-approved action categories for Level 1
5. Establish trust review cadence (weekly checks, quarterly reviews)
6. Document agent trust decisions in `docs/decisions/DEC-TRUST-####.md`

By implementing this framework, teams enable AI agents to earn autonomy through demonstrated trustworthiness while maintaining the audit trail and safety guarantees central to RJW-IDD.
