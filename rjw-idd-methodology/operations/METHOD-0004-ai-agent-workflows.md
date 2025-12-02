# METHOD-0004 — Unified AI Agent Handbook

This document is the **single source of truth** for all AI agent rules and behaviors within the RJW-IDD methodology. It covers agent workflows, trust and autonomy framework, behavioral contracts, and verification processes.

> **TL;DR:** AI agents work within a trust framework that grants autonomy based on demonstrated reliability. Start by confirming your trust level, classify your change risk, then follow the appropriate workflow.

---

## 1. Agent Trust and Autonomy Framework

### 1.1 Framework Purpose

**Goal:** Enable AI agents to earn greater autonomy through verifiable trustworthy behavior, allowing humans to focus oversight on high-value decisions while agents handle routine work independently.

**Principles:**

- **Trust is earned, not assumed** — Agents start with limited autonomy and expand capabilities through demonstrated reliability
- **Verification enables trust** — Automated checks provide continuous assurance that agent behavior meets expectations
- **Transparency builds confidence** — All agent decisions, reasoning, and actions are auditable
- **Graceful degradation** — Trust violations trigger proportionate responses, not catastrophic restrictions
- **Human oversight scales with risk** — Critical decisions always require human judgment; routine work can be delegated

### 1.2 Trust Ladder Model

Agents progress through trust levels based on track record. Each level unlocks additional autonomy while maintaining appropriate safeguards.

#### Level 0: Supervised (Default Starting Point)

**Autonomy:** None — all actions require human approval before execution.

**Characteristics:**
- Agent proposes actions; human reviews and approves/rejects each one
- All outputs treated as drafts requiring verification
- Full audit trail of proposals and decisions captured

**Pathway Access:** Minimal Risk only; all others require approval

**Promotion Criteria (to Level 1):**
- [ ] 10+ consecutive proposals approved without modification
- [ ] Zero rejected proposals due to safety/quality issues
- [ ] Demonstrated understanding of project context (assessed via spot checks)
- [ ] Completed at least one full Discovery→Execution cycle under supervision

#### Level 1: Guided

**Autonomy:** Limited — routine actions within defined boundaries proceed automatically; novel situations escalate.

**Characteristics:**
- Pre-approved action categories execute without per-action approval
- Automated guardrails flag boundary violations for human review
- Spot checks verify continued alignment (10% sample rate)
- Agent explains reasoning for non-routine decisions before acting

**Pathway Access:** Minimal/Low Risk; Medium+ require human co-pilot

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

#### Level 2: Autonomous

**Autonomy:** Broad — agent operates independently within project scope with post-hoc review.

**Characteristics:**
- Full execution authority for work within established scope
- Human review occurs asynchronously via audit rather than synchronously via approval
- Agent self-classifies risk level and adjusts documentation accordingly
- Weekly audit reviews replace per-action approval

**Pathway Access:** Minimal/Low/Medium Risk; High+ require approval

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

#### Level 3: Trusted Partner

**Autonomy:** Strategic — agent participates in planning, prioritization, and methodology evolution.

**Characteristics:**
- Contributes to Discovery research direction and spec architecture
- Proposes methodology improvements and new patterns
- Mentors Level 0-2 agents on project patterns
- Participates in quarterly governance reviews

**Pathway Access:** All pathways; serves as approver for others

**Governance Role:**
- Input on DEC-#### decisions (non-voting)
- Proposes micro-harvests when gaps are detected
- Suggests efficiency improvements based on observed patterns
- Flags systemic issues across project scope

**Demotion Triggers (to Level 2):**
- Strategic recommendation leads to significant rework
- Trust calibration audit finds overconfidence
- Methodology contribution rejected due to safety concerns

### 1.3 Trust Level Summary Table

| Trust Level | Name | Autonomy | Pathway Access |
|-------------|------|----------|----------------|
| Level 0 | Supervised | All actions require human approval | Minimal Risk only |
| Level 1 | Guided | Pre-approved categories proceed automatically | Minimal/Low Risk |
| Level 2 | Autonomous | Operates independently with post-hoc review | Minimal/Low/Medium Risk |
| Level 3 | Trusted Partner | Participates in planning and prioritization | All pathways |

---

## 2. Behavioral Contracts

Agents commit to explicit behavioral contracts that define expectations and enable automated compliance verification.

### 2.1 Core Contract (All Levels)

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

### 2.2 Level-Specific Contracts

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

---

## 3. Continuous Verification Architecture

Replace gate-only verification with continuous automated checks to catch issues earlier and build trust evidence.

### 3.1 Verification Layers

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

### 3.2 Automated Checks

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

### 3.3 Trust Scoring

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

### 3.4 Graduated Response Protocol

Trust violations trigger proportionate responses:

| Violation Severity | Trust Impact | Response |
|--------------------|--------------|----------|
| Minor (documentation gap) | -0.02 per instance | Auto-remediate if possible; log for review |
| Moderate (boundary approach) | -0.05 per instance | Immediate notification; require acknowledgment |
| Significant (boundary violation) | -0.15 per instance | Pause and escalate; human approval to resume |
| Critical (safety/security) | Immediate demotion | Full stop; incident review required |

---

## 4. Agent Roles and Responsibilities

Record role owners in `governance/METHOD-0003-role-handbook.md` and the active row in `docs/change-log.md`.

| Role | Responsibilities | Companion Artefacts |
|------|------------------|---------------------|
| Agent Conductor | Runs prompts, captures transcripts, executes guard scripts. | `docs/prompts/`, `artifacts/integration/transcript-archive/`, `logs/ci/` |
| Spec Curator | Maintains ledgers, specs, reconciliation log, and decision links. | `specs/`, `artifacts/ledgers/`, `docs/living-docs-reconciliation.md` |
| Doc Steward | Updates living documentation and verifies Change Log entries. | `docs/standards/DOC-0006`, `docs/runbooks/` |
| Governance Sentinel | Runs validators, records audits, blocks releases missing artefacts. | `scripts/validate_ids.py`, `logs/LOG-0001-stage-audits.md` |

---

## 5. Workflow Selection

**Classify risk first** — not all changes require the full workflow. Reference `governance/METHOD-0002-phase-driver-checklists.md` Section 1 for the complete risk classification flowchart.

| Risk Level | Examples | Pathway | Trust Level Required |
|------------|----------|---------|----------------------|
| **Minimal** | Doc typos, formatting, comments | Commit → Auto-verify → Merge | Level 0+ |
| **Low** | New tests, new docs, config defaults | Commit → Verify → Change log → Merge | Level 1+ |
| **Medium** | Bug fixes, refactors, internal API changes | Full verification + peer review | Level 2+ |
| **High** | Feature additions, external API changes | Full Discovery→Execution loop | Level 3 (or approval) |
| **Critical** | Security, data, availability changes | Full loop + Security review | Level 3 + Security sign-off |
| **Prototype** | POC, spike, experimental work | See Section 8 | Trust-adjusted |

---

## 6. Stage Workflows

### 6.1 Streamlined Pathways (Minimal/Low/Medium Risk)

#### Minimal Risk (5 min)

```bash
# 1. Make change
# 2. Commit
git commit -m "docs: [brief description]"
# 3. Auto-verify and merge
```

#### Low Risk (30 min)

```bash
# 1. Make change
# 2. Verify
[automated checks pass]
# 3. Update change log (simplified entry)
# 4. Commit and merge
```

#### Medium Risk (2 hours)

1. Classify risk in commit message
2. Run full automated verification
3. Request peer review
4. Ensure tests cover changes
5. Update documentation
6. Add standard change log entry
7. Merge with reviewer sign-off

---

### 6.2 Full Workflow (High/Critical Risk)

#### Inputs Before Work

1. Copy `docs/change-log.md` template and open a new `change-YYYYMMDD-##` row.
2. Draft a `DEC-####` stub using `templates/decisions/DEC-template.md` for the problem you are addressing.
3. Review `docs/living-docs-reconciliation.md`; log and assign any documentation gaps.
4. Schedule audit tags (`⟦audit-id:n⟧ <reflect/>`) and note them in the stage audit log.

#### Layer 1 — Discovery

**Research Loop**
- Run `tools/rjw_idd_evidence_harvester.py` with `research/evidence_tasks.json`.
- Store logs under `logs/discovery-harvest/` and validate results with `scripts/validate_evidence.py`.
- Promote curated evidence into `research/evidence_index.json` via `scripts/promote_evidence.py`.
- Update requirement ledger entries with new evidence IDs and log the harvest in `docs/change-log.md`.

**Specification Loop**
- Author/update specs using templates in `specs/`, linking to relevant evidence and planned tests.
- Reserve requirement/test IDs in `artifacts/ledgers/*.csv` (or equivalent datasets).
- Resolve items in `docs/living-docs-reconciliation.md` before declaring Discovery complete.
- Capture outcomes in `docs/decisions/` and update `docs/change-log.md` with verification details.

#### Layer 2 — Execution (TDD, Living Docs, Delivery)

- Use `docs/prompts/PROMPT-0001-omega-engineering.md` (or a customised prompt) to drive the agent.
- Enforce test-first and governance guards via `scripts/ci/test_gate.sh`, which executes:
  - `tools/testing/red_green_guard.py` to require failing tests before implementation.
  - `scripts/validate_ids.py` to keep ledgers, specs, and change-log references aligned.
  - `scripts/validate_evidence.py` (triggered when research assets change) using a 14-day recency window.
  - `tools/testing/change_log_guard.py` to block merges that skip the change log.
  - `tools/testing/living_docs_guard.py` to reject outstanding living-doc gaps.
  - `tools/testing/governance_alignment_guard.py` to keep specification changes, ledgers, and decision logs synchronized.
- Capture full integration transcripts under `artifacts/integration/transcript-archive/`.
- Update living documentation according to `docs/standards/DOC-0006`.
- Append `⟦audit-id:n⟧ <reflect/>` when the layer exits.

---

## 7. Governance and Audit

### 7.1 Living Documentation Enforcement

- **Before work:** log gaps in `docs/living-docs-reconciliation.md`.
- **During work:** update docs, runbooks, and specs with new IDs and Change Log references.
- **After work:** validate docs/IDs, link outputs in `docs/change-log.md`, and ensure doc updates ship with code.

### 7.2 Integration Transcript Checklist

For every AI-assisted integration:

1. Scaffold a directory with `tools/integration/archive_scaffold.py <task-slug>`.
2. Complete `context.md` with scope, linked IDs, roles, and planned doc updates.
3. Log prompts/responses in `prompts.log`, store diffs in `diffs/`, and document verification steps in `verification.md`.
4. Reference the archive path in `docs/change-log.md` and in the living documentation.

### 7.3 Cost, Security, and Observability Controls

- Run cost dashboards using `scripts/cost/run_weekly_dashboard.py`; store outputs and finance sign-offs under `logs/cost/`.
- Execute sandbox drills with `scripts/sandbox/drill.py` and record artefacts under `logs/security/`.
- Maintain telemetry/observability artefacts per `specs/SPEC-0301` and `specs/SPEC-0401`, ensuring consent receipts and metric snapshots are logged.

### 7.4 Decision & Audit Hygiene

- Every major choice gets a `DEC-####` entry referencing evidence, specs, and follow-up actions.
- Governance Sentinel keeps `logs/LOG-0001-stage-audits.md` current with stage reflections.
- Quarterly reviews revisit evidence recency, cost thresholds, security posture, and method changes; record outcomes as new decisions or spec updates.

### 7.5 Agent Activity Log

Maintain `logs/LOG-0002-agent-activity.md` with:

| Timestamp | Agent ID | Trust Level | Action Type | Risk Class | Verification | Outcome |
|-----------|----------|-------------|-------------|------------|--------------|---------|
| (ISO-8601) | (identifier) | (0-3) | (category) | (L/M/H) | (pass/warn/fail) | (success/escalated/blocked) |

### 7.6 Trust Level Changes

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

### 7.7 Quarterly Trust Review

During governance reviews, assess:

- Trust level distribution across agents
- Promotion/demotion patterns and root causes
- Verification system effectiveness (false positive/negative rates)
- Contract adequacy (gaps revealed by incidents)
- Human oversight load (trending toward sustainable level?)

---

## 8. Prototype Mode for AI Agents

When working on prototypes, spikes, or experimental features, AI agents operate under a different set of guidelines that prioritize speed and iteration while maintaining traceability. See `governance/METHOD-0002-phase-driver-checklists.md` Section 6 for full details.

### 8.1 When to Use Prototype Mode

Use prototype mode for:

- **Proof of Concept (POC):** Validating a technical approach
- **Spike:** Time-boxed investigation to reduce uncertainty
- **Feasibility Study:** Determining if a capability is achievable
- **Experimental Features:** Exploring new functionality
- **Technology Evaluation:** Comparing frameworks or libraries hands-on

### 8.2 Prototype Workflow Summary

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

### 8.3 Relaxed Gates in Prototype Mode

| Gate | Standard Mode | Prototype Mode |
|------|---------------|----------------|
| Peer Review | Required (Medium+) | Self-review acceptable |
| Test Coverage | Full coverage | Smoke tests sufficient |
| Documentation | Full specs/runbooks | Inline comments + PROTO record |
| Security Review | Required when relevant | Not required unless real user data |
| DEC Record | Required (Medium+) | PROTO record sufficient |

### 8.4 Keep/Flex/Unknown Tagging

Use these semantic tags to help distinguish essential code from scaffolding:

| Tag | Meaning | On Promotion |
|-----|---------|--------------|
| `⟦keep⟧` or `[KEEP]` | Essential to the proof-of-concept | Preserve and enhance |
| `⟦flex⟧` or `[FLEX]` | Scaffolding or shortcuts | Replace with production-grade |
| `⟦unknown⟧` or `[UNKNOWN]` | Uncertain; needs evaluation | Classify during promotion |

**Example in code:**

```python
# ⟦keep⟧ Core algorithm proving the concept
def process_data(input):
    ...

# ⟦flex⟧ Hardcoded config - replace with proper config management
CONFIG = {"timeout": 30}

# ⟦unknown⟧ Retry logic may or may not be needed in production
def retry_with_backoff():
    ...
```

### 8.5 Working on Promoted Prototype Code

When encountering code promoted from a prototype (referenced by PROTO-#### in DEC-####):

- **`[KEEP]` code:** Preserve core logic; may enhance for production quality
- **`[FLEX]` code:** Explicitly marked for replacement; use standard production approach
- **`[UNKNOWN]` code:** Stop, evaluate, reclassify as KEEP or FLEX, then proceed

### 8.6 Trust Level Adjustments for Prototype Work

Prototype mode adjusts how trust levels apply:

| Trust Level | Standard Mode | Prototype Mode |
|-------------|---------------|----------------|
| Level 0 | All actions require approval | PROTO-scoped actions may batch |
| Level 1 | Pre-approved categories only | All prototype work pre-approved in scope |
| Level 2 | Autonomous with post-hoc review | Autonomous; review at exit |
| Level 3 | Strategic participation | May approve PROTO records and exits |

---

## 9. Integration with RJW-IDD Layers

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

---

## 10. Method Adoption Steps

1. Initialize `logs/LOG-0002-agent-activity.md` for activity tracking
2. Assess current agents against Level 0 baseline
3. Implement automated verification checks (process → output → behavioral)
4. Define project-specific pre-approved action categories for Level 1
5. Establish trust review cadence (weekly checks, quarterly reviews)
6. Document agent trust decisions in `docs/decisions/DEC-TRUST-####.md`

---

## 11. Implementing the Agent Handbook in Your Agent

This section provides code patterns for hardcoding the trust framework, behavioral contracts, and verification systems into your agent.

### 11.1 Trust Ladder Implementation

```python
from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

class TrustLevel(IntEnum):
    """Trust levels per Section 1.2."""
    SUPERVISED = 0      # All actions require human approval
    GUIDED = 1          # Pre-approved categories proceed automatically
    AUTONOMOUS = 2      # Operates independently with post-hoc review
    TRUSTED_PARTNER = 3 # Participates in planning and prioritization

@dataclass
class TrustLadder:
    """Manages agent trust progression."""
    
    agent_id: str
    current_level: TrustLevel = TrustLevel.SUPERVISED
    consecutive_approvals: int = 0
    actions_at_level: int = 0
    escalation_accuracy: float = 1.0
    guardrail_violations: int = 0
    days_at_current_level: int = 0
    
    # Pathway access per trust level
    PATHWAY_ACCESS = {
        TrustLevel.SUPERVISED: ['minimal'],
        TrustLevel.GUIDED: ['minimal', 'low'],
        TrustLevel.AUTONOMOUS: ['minimal', 'low', 'medium'],
        TrustLevel.TRUSTED_PARTNER: ['minimal', 'low', 'medium', 'high', 'critical']
    }
    
    def can_access_pathway(self, risk_level: str) -> bool:
        """Check if agent can access a risk pathway."""
        return risk_level.lower() in self.PATHWAY_ACCESS[self.current_level]
    
    def check_promotion_criteria(self) -> Dict[str, bool]:
        """Check if agent meets promotion criteria to next level."""
        if self.current_level == TrustLevel.SUPERVISED:
            return {
                'consecutive_approvals_10': self.consecutive_approvals >= 10,
                'zero_rejected_safety': self.guardrail_violations == 0,
                'context_understanding': True,  # Assessed via spot checks
                'completed_full_cycle': self.actions_at_level >= 20
            }
        elif self.current_level == TrustLevel.GUIDED:
            return {
                'actions_50_no_failures': self.actions_at_level >= 50,
                'escalation_accuracy_95': self.escalation_accuracy >= 0.95,
                'zero_guardrail_violations': self.guardrail_violations == 0,
                'positive_governance_assessment': True  # External check
            }
        elif self.current_level == TrustLevel.AUTONOMOUS:
            return {
                'days_90_no_demotion': self.days_at_current_level >= 90,
                'audit_findings_meet_expectations': True,
                'judgment_in_ambiguous_situations': True,
                'cross_project_track_record': True
            }
        return {}
    
    def promote(self) -> bool:
        """Attempt to promote to next trust level."""
        criteria = self.check_promotion_criteria()
        if all(criteria.values()) and self.current_level < TrustLevel.TRUSTED_PARTNER:
            self.current_level = TrustLevel(self.current_level + 1)
            self.actions_at_level = 0
            self.days_at_current_level = 0
            return True
        return False
    
    def demote(self, reason: str):
        """Demote to previous trust level."""
        if self.current_level > TrustLevel.SUPERVISED:
            self.current_level = TrustLevel(self.current_level - 1)
            self.actions_at_level = 0
            self.days_at_current_level = 0
```

### 11.2 Behavioral Contract Implementation

```python
@dataclass
class BehavioralContract:
    """Implements behavioral contracts per Section 2."""
    
    transparency_log: List[Dict] = field(default_factory=list)
    boundary_violations: List[Dict] = field(default_factory=list)
    
    def log_decision(self, decision: str, reasoning: str, 
                     confidence: float, uncertainty_areas: List[str]):
        """Log decision with reasoning per transparency contract."""
        self.transparency_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'decision': decision,
            'reasoning': reasoning,
            'confidence': confidence,
            'uncertainty_areas': uncertainty_areas
        })
    
    def check_boundary(self, action: str, agent_level: TrustLevel,
                       required_level: TrustLevel) -> bool:
        """Check if action is within authorized boundaries."""
        if agent_level < required_level:
            self.boundary_violations.append({
                'timestamp': datetime.utcnow().isoformat(),
                'action': action,
                'agent_level': agent_level.name,
                'required_level': required_level.name
            })
            return False
        return True
    
    def should_escalate(self, action_type: str, 
                        pre_approved_categories: List[str]) -> bool:
        """Determine if action should escalate to human review.
        
        Escalation triggers per Section 1.2 Level 1.
        """
        escalation_triggers = [
            'external_dependency',
            'security_sensitive',
            'scope_modification',
            'conflict_with_existing'
        ]
        
        if action_type in escalation_triggers:
            return True
        if action_type not in pre_approved_categories:
            return True
        return False

class CoreContract:
    """Core behavioral contract all agents must follow."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.audit_trail = []
    
    def verify_action(self, action: dict, trust_level: TrustLevel) -> dict:
        """Verify action against core contract terms."""
        violations = []
        
        # Transparency checks
        if not action.get('reasoning'):
            violations.append('Missing reasoning for action')
        if action.get('confidence') is None:
            violations.append('Confidence level not disclosed')
        
        # Boundary checks
        if action.get('modifies_production') and not action.get('explicit_auth'):
            violations.append('Production modification without authorization')
        
        # Quality checks
        if not action.get('verified_before_completion'):
            violations.append('Output not verified before completion')
        
        # Log to audit trail
        self.audit_trail.append({
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'violations': violations,
            'passed': len(violations) == 0
        })
        
        return {
            'passed': len(violations) == 0,
            'violations': violations
        }
```

### 11.3 Continuous Verification Implementation

```python
@dataclass
class VerificationResult:
    passed: bool
    check_type: str
    details: Dict
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

class ContinuousVerifier:
    """Implements continuous verification per Section 3."""
    
    def __init__(self):
        self.verification_history: List[VerificationResult] = []
    
    def verify_process(self, action: dict) -> VerificationResult:
        """Process verification - runs on every action."""
        checks = {
            'change_log_present': self._check_change_log(action),
            'linked_artifacts_exist': self._check_artifact_links(action),
            'approvals_obtained': self._check_approvals(action),
            'timing_within_bounds': self._check_timing(action)
        }
        
        result = VerificationResult(
            passed=all(checks.values()),
            check_type='process',
            details=checks
        )
        self.verification_history.append(result)
        return result
    
    def verify_output(self, artifact: dict) -> VerificationResult:
        """Output verification - runs on every artifact."""
        checks = {
            'id_format_valid': self._validate_id_format(artifact.get('id', '')),
            'cross_refs_resolve': self._check_cross_references(artifact),
            'no_orphaned_refs': self._check_orphaned_references(artifact),
            'structure_matches': self._validate_structure(artifact)
        }
        
        result = VerificationResult(
            passed=all(checks.values()),
            check_type='output',
            details=checks
        )
        self.verification_history.append(result)
        return result
    
    def verify_behavior(self, agent_actions: List[dict], 
                        trust_level: TrustLevel) -> VerificationResult:
        """Behavioral verification - continuous monitoring."""
        checks = {
            'within_boundaries': self._check_boundaries(agent_actions, trust_level),
            'escalations_appropriate': self._check_escalations(agent_actions),
            'risk_classifications_accurate': self._check_risk_accuracy(agent_actions),
            'contracts_honored': self._check_contract_compliance(agent_actions)
        }
        
        result = VerificationResult(
            passed=all(checks.values()),
            check_type='behavioral',
            details=checks
        )
        self.verification_history.append(result)
        return result
    
    def _validate_id_format(self, id_str: str) -> bool:
        """Validate artifact ID follows scheme (REQ-####, SPEC-####, etc.)."""
        import re
        patterns = [
            r'^REQ-\d{4}$', r'^SPEC-\d{4}$', r'^TEST-\d{4}$',
            r'^DEC-\d{4}$', r'^EVD-\d{4}$', r'^DOC-\d{4}$'
        ]
        return any(re.match(p, id_str) for p in patterns)
```

### 11.4 Trust Score Calculation

```python
class TrustScorer:
    """Calculates rolling trust score per Section 3.3."""
    
    WEIGHTS = {
        'process_compliance': 0.25,
        'output_quality': 0.30,
        'behavioral_alignment': 0.30,
        'human_assessment': 0.15
    }
    
    THRESHOLDS = {
        'promotion_eligible': 0.90,
        'stable': 0.75,
        'warning': 0.60,
        'demotion': 0.50
    }
    
    def __init__(self, verifier: ContinuousVerifier):
        self.verifier = verifier
        self.human_assessments: List[float] = []
    
    def calculate_score(self) -> float:
        """Calculate current trust score."""
        history = self.verifier.verification_history
        
        # Process compliance score
        process_checks = [r for r in history if r.check_type == 'process']
        process_score = sum(1 for r in process_checks if r.passed) / max(len(process_checks), 1)
        
        # Output quality score
        output_checks = [r for r in history if r.check_type == 'output']
        output_score = sum(1 for r in output_checks if r.passed) / max(len(output_checks), 1)
        
        # Behavioral alignment score
        behavior_checks = [r for r in history if r.check_type == 'behavioral']
        behavior_score = sum(1 for r in behavior_checks if r.passed) / max(len(behavior_checks), 1)
        
        # Human assessment score (average of recent assessments)
        human_score = sum(self.human_assessments[-10:]) / max(len(self.human_assessments[-10:]), 1)
        
        return (
            self.WEIGHTS['process_compliance'] * process_score +
            self.WEIGHTS['output_quality'] * output_score +
            self.WEIGHTS['behavioral_alignment'] * behavior_score +
            self.WEIGHTS['human_assessment'] * human_score
        )
    
    def get_status(self) -> str:
        """Get trust status based on current score.
        
        Thresholds in descending order:
        - promotion_eligible: 0.90+
        - stable: 0.75+
        - warning: 0.60+
        - demotion_required: below 0.60
        """
        score = self.calculate_score()
        if score >= self.THRESHOLDS['promotion_eligible']:
            return 'promotion_eligible'
        elif score >= self.THRESHOLDS['stable']:
            return 'stable'
        elif score >= self.THRESHOLDS['warning']:
            return 'warning'
        else:
            return 'demotion_required'
```

### 11.5 Graduated Response Implementation

```python
class GraduatedResponseHandler:
    """Implements graduated response protocol per Section 3.4."""
    
    SEVERITY_IMPACTS = {
        'minor': -0.02,      # Documentation gap
        'moderate': -0.05,   # Boundary approach
        'significant': -0.15, # Boundary violation
        'critical': 'immediate_demotion'
    }
    
    def __init__(self, trust_ladder: TrustLadder, scorer: TrustScorer):
        self.trust_ladder = trust_ladder
        self.scorer = scorer
    
    def handle_violation(self, severity: str, violation_details: dict) -> dict:
        """Handle trust violation with proportionate response."""
        impact = self.SEVERITY_IMPACTS.get(severity)
        
        if severity == 'critical':
            # Immediate demotion and full stop
            self.trust_ladder.demote(reason=violation_details.get('reason', 'Critical violation'))
            return {
                'action': 'immediate_demotion',
                'requires': 'incident_review',
                'agent_paused': True
            }
        
        elif severity == 'significant':
            # Pause and escalate
            return {
                'action': 'pause_escalate',
                'trust_impact': impact,
                'requires': 'human_approval_to_resume'
            }
        
        elif severity == 'moderate':
            # Immediate notification
            return {
                'action': 'notify_require_acknowledgment',
                'trust_impact': impact,
                'requires': 'acknowledgment'
            }
        
        else:  # minor
            # Auto-remediate if possible
            return {
                'action': 'auto_remediate',
                'trust_impact': impact,
                'logged_for_review': True
            }
```

### 11.6 Complete Agent Integration Example

```python
class RJWIDDCompliantAgent:
    """Complete example of an RJW-IDD compliant agent."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.trust_ladder = TrustLadder(agent_id=agent_id)
        self.contract = CoreContract(agent_id=agent_id)
        self.verifier = ContinuousVerifier()
        self.scorer = TrustScorer(self.verifier)
        self.response_handler = GraduatedResponseHandler(
            self.trust_ladder, self.scorer
        )
        self.behavioral_contract = BehavioralContract()
    
    def execute_action(self, action: dict) -> dict:
        """Execute an action with full RJW-IDD compliance."""
        
        # 1. Check authorization
        risk_level = action.get('risk_level', 'medium')
        if not self.trust_ladder.can_access_pathway(risk_level):
            return {
                'status': 'blocked',
                'reason': f'Trust level {self.trust_ladder.current_level.name} cannot access {risk_level} risk pathway'
            }
        
        # 2. Verify against behavioral contract
        contract_result = self.contract.verify_action(
            action, self.trust_ladder.current_level
        )
        if not contract_result['passed']:
            violation_response = self.response_handler.handle_violation(
                'moderate', {'violations': contract_result['violations']}
            )
            return {'status': 'contract_violation', **violation_response}
        
        # 3. Check if escalation needed
        if self.behavioral_contract.should_escalate(
            action.get('type', ''), 
            ['documentation', 'test_creation', 'evidence_curation']
        ):
            return {
                'status': 'escalation_required',
                'reason': 'Action requires human review'
            }
        
        # 4. Log decision with transparency
        self.behavioral_contract.log_decision(
            decision=action.get('description', ''),
            reasoning=action.get('reasoning', ''),
            confidence=action.get('confidence', 0.8),
            uncertainty_areas=action.get('uncertainties', [])
        )
        
        # 5. Execute and verify
        result = self._perform_action(action)
        
        # 6. Run continuous verification
        self.verifier.verify_process(action)
        if result.get('artifact'):
            self.verifier.verify_output(result['artifact'])
        
        # 7. Update trust metrics
        self.trust_ladder.actions_at_level += 1
        if result.get('success'):
            self.trust_ladder.consecutive_approvals += 1
        
        # 8. Check for promotion
        if self.trust_ladder.promote():
            result['trust_promoted'] = True
            result['new_level'] = self.trust_ladder.current_level.name
        
        return result
    
    def _perform_action(self, action: dict) -> dict:
        """Perform the actual action - implement based on your agent's capabilities."""
        # Implement your agent's action execution here
        return {'success': True}
```

---

## 12. Related Documentation

- `core/METHOD-0001-core-method.md` — Core methodology principles
- `governance/METHOD-0002-phase-driver-checklists.md` — Unified Lifecycle & Checklists
- `governance/METHOD-0003-role-handbook.md` — Role handbook
- `operations/METHOD-0005-operations-production-support.md` — Operations and production support
- `operations/METHOD-0006-context-curation-engine.md` — Context Curation Engine
- `templates/DEC-LITE-template.md` — Lightweight decision template (Low/Medium risk)
- `templates/PROTO-template.md` — Prototype record template
- `templates/AGENT-TRUST-template.md` — Trust level change record template
- `templates/context/CTX-INDEX-template.md` — Task context index template
- `templates/context/LIVING-DOCS-template.md` — Living documentation template

Run this workflow step-by-step. When artefacts, prompts, or scripts evolve, update the corresponding specs/runbooks so the scaffold remains reusable for the next project.
