# METHOD-0001 — RJW-IDD Core Method (Decision Synthesis)

This document distils the Rolaand Jayz Wayz – Coding with Natural Language: Intelligence Driven Development (RJW-IDD) method into a self-contained playbook drawn directly from the research-stage Tree-of-Thought decisions (`DEC-0001`‒`DEC-0006`). Evidence artefacts and product-specific scaffolding are intentionally excluded; only the reasoning outcomes that define the methodology remain.

## 1. Method Orientation
- **Mission:** Replace vibe-driven agent work with a disciplined loop where reality (fresh research, explicit trade-offs) leads specification and implementation.
- **Lifecycle Spine (`DEC-0004`):** Two auditable layers — Discovery (research intake + specification synthesis) and Execution (test-first delivery + integration readiness) — coordinated through explicit decision logs and change records.
- **Traceable Decisions (`DEC-0001`):** Every strategic choice is captured in an individual Markdown decision record using a consistent schema to keep Tree-of-Thought context human-readable and auditable.

## 2. Governance Baseline
- Maintain a dedicated decisions directory with monotonically increasing `DEC-####` identifiers (`DEC-0001`).
- Keep method doctrine inside `rjw-idd-methodology/` under the `METHOD-####` namespace and store project artefacts in the starter kit using project prefixes (`DEC-####`, `DOC-####`, `SPEC-####`, etc.).
- Each change to the method must be paired with an updated decision entry and an aligned change-log row so downstream teams can understand rationale without rereading the full history.
- Standard operating documents (runbooks, standards, prompts) mirror the decision identifiers they depend on, creating a direct map from thinking to practice.

## 3. Discovery Layer
Discovery keeps reality in front of design by pairing continuous evidence intake with specification synthesis.

### 3.1 Research Loop
- **Automated Harvest (`DEC-0002`):** Run the scripted harvester across primary communities (e.g., Reddit, GitHub, forums) to gather current practitioner insight. Automation guarantees consistent metadata, recency filters, and reruns on demand.
- **Dual-Layer Evidence Store (`DEC-0003`):**
  - Keep a raw index as an immutable transcript of every harvested item.
  - Promote a curated subset after human validation to power requirements, specs, and decisions without losing provenance.
- **Research Operations:**
  - Log each harvest execution and keep tooling lightweight enough to operate inside constrained environments.
  - After promotion, rerun validators to ensure every curated entry still links back to the raw source.

### 3.2 Specification Loop
- **Trigger:** Starts only after the research loop surfaces curated insight that clears the intake gate.
- **Outputs:** Refreshed requirement ledger, a full specification stack, and an updated living-document reconciliation log.
- **Approach (`DEC-0004`, `DEC-0005`):**
  - Overproduce specifications across functional, quality, observability, security, integration, and cost dimensions.
  - Where research gaps remain (e.g., observability practices), proceed with provisional guidance while logging explicit assumptions and scheduling focused micro-harvests to close gaps.
- **Governance:** Every spec update references the decision that justified it and the curated insight that inspired it, keeping the Discovery layer accountable to real-world signals.

### 3.3 Discovery Governance
- Treat research-to-spec as a closed loop: new evidence opens a discovery ticket, spec changes cite the ticket ID, and backlog gaps trigger micro-harvests before work proceeds.
- Maintain the discovery ledger so that every requirement, assumption, or gap links back to the harvest that informed it.

## 4. Execution Layer
Execution begins once Discovery locks scope and continues until the release package clears all gates.

### 4.1 Parallel Engines
- **Test-Driven Development:** Work enters the codebase only with failing tests first; guards reject changes that lack accompanying tests.
- **Living Documentation:** Docs and runbooks evolve in the same change-set that introduces code updates, eliminating stale knowledge.
- **Integration-First Delivery:** Cross-system work is archived with transcripts and diffs so future audits can replay the context.

### 4.2 Telemetry & Observability (`DEC-0005`, `DEC-0006`)
- Persist consent decisions and metric streams as JSON artefacts for audit and reconciliation.
- Keep observability specs active even when practitioner guidance is partially incomplete; log assumptions and instruct Discovery to backfill insight quickly.

### 4.3 Cost Awareness (`DEC-0004` synthesised)
- Treat cost instrumentation as part of the Execution gate: every release must attach updated dashboards and finance acknowledgements when thresholds are crossed.

## 6. Stage Gates & Checklists
The method is enforced via repeatable checklists at each boundary:

| Gate | Required Signals | Derived From |
|------|------------------|--------------|
| **Discovery Intake** | Curated evidence index ≥ target coverage, raw index archived, harvest logs stored, open gaps recorded for follow-up | `DEC-0002`, `DEC-0003` |
| **Discovery ➜ Execution** | Requirement ledger refreshed, scope freeze recorded, spec stack updated (including provisional observability guidance), living-doc reconciliation cleared or deferred with plan | `DEC-0004`, `DEC-0005` |
| **Execution ➜ Release** | Tests guard enforced, documentation updated alongside code, integration transcripts stored, consent tooling active with audit artefacts | `DEC-0004`, `DEC-0006` |

Each gate adds a new decision record, audit tag, and change-log entry so the lifecycle never advances without an accountable narrative.

## 7. Operating Cadence
- **Decisions as First-Class Artefacts:** Before altering the method, capture options, trade-offs, and chosen outcomes in a new `DEC-####`. This keeps the method evolvable without losing prior reasoning.
- **Micro-Harvest Rhythm:** When assumptions appear (e.g., provisional observability guidance), immediately schedule a targeted research sprint to validate or replace them.
- **Audit Trail:** Maintain the shared stage-audit log (`logs/LOG-0001-stage-audits.md`) that summarises phase readiness and records outstanding items until they are cleared.

## 8. Method Adoption Steps
1. Clone this document and the companion decision set into the target environment.
2. Stand up the decision logging structure (`docs/decisions/`) and Change Log template (`docs/change-log.md`) before beginning new research.
3. Run the automated harvest, curate results, and document gaps.
4. Drive the Discovery specification loop, leaning on decision outcomes to keep specifications honest and provisional guidance well-marked.
5. Launch the Execution layer with consent-aware tooling and red→green→refactor cycles.
6. Perform stage audits at every gate, logging outcomes in `logs/LOG-0001-stage-audits.md` and refreshing decisions whenever the method shifts.

## 9. Implementing the Core Method in Your Agent

This section provides code patterns for hardcoding the RJW-IDD core method into your agent implementation.

### 9.1 Governance Baseline Implementation

Implement decision tracking and change logging in your agent:

```python
import os
import json
from datetime import datetime
from pathlib import Path

class GovernanceManager:
    """Manages decision records and change logs per RJW-IDD governance baseline."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.decisions_dir = self.project_root / "docs" / "decisions"
        self.change_log_path = self.project_root / "docs" / "change-log.md"
        self._next_decision_id = self._get_next_decision_id()
    
    def _get_next_decision_id(self) -> int:
        """Get next monotonically increasing DEC-#### identifier."""
        existing = list(self.decisions_dir.glob("DEC-*.md"))
        if not existing:
            return 1
        ids = []
        for f in existing:
            try:
                ids.append(int(f.stem.split("-")[1]))
            except (IndexError, ValueError):
                continue
        return max(ids, default=0) + 1
    
    def create_decision(self, title: str, options: list, 
                        chosen: str, rationale: str, evidence_ids: list = None) -> str:
        """Create a DEC-#### record for strategic choices."""
        dec_id = f"DEC-{self._next_decision_id:04d}"
        self._next_decision_id += 1
        
        content = f"""# {dec_id} — {title}

**Date:** {datetime.utcnow().strftime('%Y-%m-%d')}
**Status:** Accepted

## Context
[Describe the situation requiring a decision]

## Options Considered
{chr(10).join(f'- **Option {i+1}:** {opt}' for i, opt in enumerate(options))}

## Decision
{chosen}

## Rationale
{rationale}

## Evidence
{chr(10).join(f'- {eid}' for eid in (evidence_ids or [])) or '- None cited'}

## Consequences
[Document expected outcomes and follow-up actions]
"""
        decision_path = self.decisions_dir / f"{dec_id}.md"
        decision_path.write_text(content)
        self._update_change_log(dec_id, title)
        return dec_id
    
    def _update_change_log(self, dec_id: str, summary: str):
        """Append entry to change log."""
        entry = f"\n| {datetime.utcnow().strftime('%Y-%m-%d')} | {dec_id} | {summary} |"
        with open(self.change_log_path, 'a') as f:
            f.write(entry)
```

### 9.2 Discovery Layer Implementation

Implement the research and specification loops:

```python
class DiscoveryLayer:
    """Implements the Discovery layer: research intake + specification synthesis."""
    
    def __init__(self, governance: GovernanceManager):
        self.governance = governance
        self.evidence_index = []
        self.requirement_ledger = []
        self.spec_stack = []
    
    def harvest_evidence(self, sources: list, filters: dict) -> list:
        """Run research loop - gather evidence from sources.
        
        Corresponds to Section 3.1 Research Loop.
        """
        raw_evidence = []
        for source in sources:
            # Implement source-specific harvesting
            items = self._fetch_from_source(source, filters)
            raw_evidence.extend(items)
        
        # Store raw index as immutable transcript
        self._store_raw_index(raw_evidence)
        return raw_evidence
    
    def curate_evidence(self, raw_items: list, validation_fn) -> list:
        """Promote validated evidence to curated subset.
        
        Maintains provenance link to raw source per DEC-0003.
        """
        curated = []
        for item in raw_items:
            if validation_fn(item):
                curated_item = {
                    **item,
                    'evd_id': f"EVD-{len(self.evidence_index)+1:04d}",
                    'curated_date': datetime.utcnow().isoformat(),
                    'raw_source_ref': item.get('id')
                }
                curated.append(curated_item)
                self.evidence_index.append(curated_item)
        return curated
    
    def synthesize_requirements(self, curated_evidence: list) -> list:
        """Drive specification loop from curated evidence.
        
        Corresponds to Section 3.2 Specification Loop.
        """
        requirements = []
        for evd in curated_evidence:
            req = {
                'req_id': f"REQ-{len(self.requirement_ledger)+1:04d}",
                'evidence_refs': [evd['evd_id']],
                'description': '',  # To be filled
                'acceptance_criteria': [],
                'status': 'draft'
            }
            requirements.append(req)
            self.requirement_ledger.append(req)
        return requirements
    
    def check_discovery_exit_gate(self) -> dict:
        """Verify Discovery layer exit criteria per Section 6 Stage Gates."""
        return {
            'evidence_coverage': len(self.evidence_index) > 0,
            'requirements_linked': all(
                r.get('evidence_refs') for r in self.requirement_ledger
            ),
            'gaps_documented': True,  # Implement gap tracking
            'ready_for_execution': True
        }
```

### 9.3 Execution Layer Implementation

Implement test-driven development and living documentation:

```python
class ExecutionLayer:
    """Implements the Execution layer: TDD, living docs, integration-first delivery."""
    
    def __init__(self, governance: GovernanceManager):
        self.governance = governance
        self.test_results = []
        self.integration_transcripts = []
    
    def enforce_test_first(self, change_request: dict) -> bool:
        """Enforce test-first development per Section 4.1.
        
        Returns True only if failing tests exist before implementation.
        """
        related_tests = self._find_related_tests(change_request)
        if not related_tests:
            raise ValueError(
                "Cannot proceed: No tests found. Write failing tests first."
            )
        
        # Run tests - should fail before implementation
        results = self._run_tests(related_tests)
        has_failing = any(not r['passed'] for r in results)
        
        if not has_failing:
            raise ValueError(
                "Cannot proceed: All tests pass. Add failing tests for new behavior."
            )
        
        return True
    
    def update_living_docs(self, change_id: str, doc_updates: dict):
        """Update documentation alongside code changes.
        
        Docs evolve in the same change-set per Section 4.1.
        """
        for doc_path, content in doc_updates.items():
            self._update_document(doc_path, content)
            self._log_doc_update(change_id, doc_path)
    
    def archive_integration_transcript(self, task_slug: str, 
                                       context: dict, 
                                       prompts_log: list,
                                       diffs: list):
        """Archive integration transcripts for cross-system work.
        
        Per Section 4.1: archived with transcripts and diffs for future audits.
        """
        transcript = {
            'task_slug': task_slug,
            'timestamp': datetime.utcnow().isoformat(),
            'context': context,
            'prompts_log': prompts_log,
            'diffs': diffs
        }
        self.integration_transcripts.append(transcript)
        return transcript
    
    def check_execution_exit_gate(self) -> dict:
        """Verify Execution layer exit criteria."""
        return {
            'tests_present': len(self.test_results) > 0,
            'all_tests_pass': all(t['passed'] for t in self.test_results),
            'docs_updated': True,  # Implement doc check
            'transcripts_archived': len(self.integration_transcripts) > 0
        }
```

### 9.4 Stage Gate Enforcement

Implement stage gate validation:

```python
class StageGateEnforcer:
    """Enforces stage gates between lifecycle phases."""
    
    GATES = {
        'discovery_intake': [
            'curated_evidence_coverage',
            'raw_index_archived',
            'harvest_logs_stored',
            'gaps_recorded'
        ],
        'discovery_to_execution': [
            'requirement_ledger_refreshed',
            'scope_freeze_recorded',
            'spec_stack_updated',
            'living_doc_reconciliation_cleared'
        ],
        'execution_to_release': [
            'test_guard_enforced',
            'documentation_updated',
            'integration_transcripts_stored',
            'consent_tooling_active'
        ]
    }
    
    def validate_gate(self, gate_name: str, checks: dict) -> tuple:
        """Validate all requirements for a stage gate.
        
        Returns (passed: bool, missing: list).
        """
        required = self.GATES.get(gate_name, [])
        missing = [req for req in required if not checks.get(req, False)]
        return (len(missing) == 0, missing)
    
    def record_gate_passage(self, gate_name: str, audit_log_path: str):
        """Record gate passage in audit log."""
        entry = {
            'gate': gate_name,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'passed'
        }
        # Append to stage audit log
        self._append_audit_entry(audit_log_path, entry)
```

For hands-on execution, pair this overview with:
- `governance/METHOD-0002-phase-driver-checklists.md` for unified lifecycle and gate-by-gate tasks (Standard, Streamlined, and Prototype pathways).
- `governance/METHOD-0003-role-handbook.md` to keep ownership clear.
- `operations/METHOD-0004-ai-agent-workflows.md` for AI agent workflows, trust framework, and behavioral contracts.
- `operations/METHOD-0005-operations-production-support.md` for post-deployment phases.
- `operations/METHOD-0006-context-curation-engine.md` for context management during AI agent implementation.
- `templates/decisions/DEC-template.md` when drafting new Tree-of-Thought decisions.

By following the decision-derived structure above, teams can transplant RJW-IDD into any project while keeping the method faithful to the original Tree-of-Thought reasoning that shaped it.
