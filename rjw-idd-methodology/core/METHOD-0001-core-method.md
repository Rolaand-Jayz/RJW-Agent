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



For hands-on execution, pair this overview with:
- `governance/METHOD-0002-phase-driver-checklists.md` for unified lifecycle and gate-by-gate tasks (Standard, Streamlined, and Prototype pathways).
- `governance/METHOD-0003-role-handbook.md` to keep ownership clear.
- `operations/METHOD-0004-ai-agent-workflows.md` for AI agent workflows, trust framework, and behavioral contracts.
- `operations/METHOD-0005-operations-production-support.md` for post-deployment phases.
- `operations/METHOD-0006-context-curation-engine.md` for context management during AI agent implementation.
- `templates/decisions/DEC-template.md` when drafting new Tree-of-Thought decisions.

By following the decision-derived structure above, teams can transplant RJW-IDD into any project while keeping the method faithful to the original Tree-of-Thought reasoning that shaped it.
