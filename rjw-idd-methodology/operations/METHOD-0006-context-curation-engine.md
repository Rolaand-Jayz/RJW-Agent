# METHOD-0006 — Context Curation Engine

This document defines the **Context Curation Engine**, a methodology framework for continuously managing and curating the context available to AI agents during implementation. It ensures agents see only what is relevant to their current task while maintaining a governed source of truth for project knowledge.

> **TL;DR:** The Context Curation Engine is a process framework that guides how AI agent context is managed on each turn—dropping irrelevant details and loading only what's needed for the current step. Every task gets a Context Index that tracks in-scope files, decisions, and assumptions.
>
> **Note:** This document describes a **methodology framework**, not implemented tooling. The processes and rules defined here should be followed by agents and teams; actual implementation of automated tooling is optional and project-specific.

---

## 1. Overview

### 1.1 Purpose

AI agents working on complex projects often struggle with context limits and relevance filtering. The Context Curation Engine addresses these challenges by defining processes for:

- **Active Context Management** — Continuously evaluating what information matters for the current task
- **Context Update Triggers** — Specifying when context refreshes should occur as new features or components are introduced
- **Living Documentation Integration** — Maintaining a governed source of truth that informs context selection
- **Task-Scoped Indexes** — Creating per-task documents that explicitly list in-scope information

### 1.2 Framework Principles

| Principle | Description |
|-----------|-------------|
| **Relevance First** | Only load context that directly applies to the current task step |
| **Continuous Curation** | Evaluate context on every turn; remove stale information proactively |
| **Governed Source of Truth** | Living docs serve as the authoritative reference for context decisions |
| **Explicit Scoping** | Every task has a Context Index documenting what's in and out of scope |
| **Propagation on Change** | When changes occur, update affected context indexes following defined rules |

### 1.3 Integration with RJW-IDD Layers

```text
┌─────────────────────────────────────────────────────────────────┐
│                      Context Curation Engine                     │
├─────────────────────────────────────────────────────────────────┤
│  Discovery Layer        │  Execution Layer       │  Operations   │
│  - Research context     │  - Implementation      │  - Incident   │
│  - Evidence context     │    context             │    context    │
│  - Spec context         │  - Test context        │  - Runbook    │
│                         │  - Integration context │    context    │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Living Documents   │
                    │  (Source of Truth)   │
                    └─────────────────────┘
```

---

## 2. Context Index

### 2.1 Definition

A **Context Index** is a task-specific document that lists the files, decisions, technical details, and assumptions that are in-scope for a particular task. It serves as the agent's "working set" of relevant information.

### 2.2 Context Index Structure

Each Context Index contains:

| Section | Purpose | Contents |
|---------|---------|----------|
| **Task Scope** | Define task boundaries | Task ID, objectives, constraints |
| **Affected Areas** | Map to code/docs | Files, modules, endpoints, APIs |
| **Technical Context** | Relevant decisions | Architecture decisions, patterns, conventions |
| **Assumptions** | Explicit assumptions | What the agent should assume true |
| **Dependencies** | Related work | Upstream/downstream task dependencies |
| **Change History** | What changed | Structured changelog of relevant changes |

### 2.3 Creating a Context Index

When initiating a new task:

1. **Identify Task Boundaries**
   - Define clear objectives and acceptance criteria
   - Specify what is explicitly out of scope

2. **Map Affected Areas**
   - List files and modules the task may touch
   - Identify affected endpoints or interfaces
   - Note integration points with other systems

3. **Gather Technical Context**
   - Reference relevant decision records (`DEC-####`)
   - Include applicable specifications (`SPEC-####`)
   - Link to coding conventions and patterns

4. **Document Assumptions**
   - State what the agent should assume true
   - Note provisional assumptions that need validation
   - Flag constraints from existing architecture

5. **Register Dependencies**
   - Identify tasks that must complete first
   - Note tasks that depend on this work
   - Track parallel work that may conflict

### 2.4 Context Index Lifecycle

```text
┌──────────────────────────────────────────────────────────────────────┐
│                      Context Index Lifecycle                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Create           Update on           Automatic         Archive       │
│  ──────►  Use  ─────────────► Use ───────────────► Use ──────────►    │
│                 each turn           propagation       on complete     │
│                                                                        │
│  [Task Start]  [Active Work]  [Change Detection]  [Task End]         │
│                                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Turn-Based Context Curation

### 3.1 Context Evaluation Cycle

On every agent turn, the Context Curation Engine performs:

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Turn-Based Context Cycle                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. EVALUATE ──► 2. REMOVE ──► 3. LOAD ──► 4. PROCEED           │
│                                                                   │
│  Assess current    Drop stale    Pull missing   Execute with     │
│  context validity  or irrelevant relevant info  curated context  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Evaluation Criteria

| Criterion | Question | Action if False |
|-----------|----------|-----------------|
| **Relevance** | Does this relate to the current step? | Remove from active context |
| **Currency** | Is this information still accurate? | Refresh or remove |
| **Completeness** | Are there gaps in required context? | Load missing information |
| **Consistency** | Does context align with Living Docs? | Reconcile discrepancies |

### 3.3 Context Scoring

Assign a relevance score (0.0 - 1.0) to context items to guide prioritization. Scoring can be performed by the agent, team, or automated tooling if implemented.

**Scoring Guidelines:**

- **1.0** — Item is directly required for current step (e.g., file being modified, decision being implemented)
- **0.8** — Item provides essential context (e.g., related specs, immediate dependencies)
- **0.6** — Item provides helpful background (e.g., architectural patterns, coding conventions)
- **0.4** — Item may be needed later in the task (e.g., integration points, downstream consumers)
- **0.2** — Item is peripherally related (e.g., similar features, historical context)
- **0.0** — Item has no bearing on current task

**Recommended Actions by Score:**

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| 0.8 - 1.0 | Directly relevant | Keep in active context |
| 0.5 - 0.79 | Potentially relevant | Keep; demote if unused |
| 0.2 - 0.49 | Background context | Load on demand only |
| 0.0 - 0.19 | Not relevant | Remove from context |

### 3.4 Context Window Management

When approaching context limits:

1. **Prioritize by Relevance Score** — Highest scores stay
2. **Summarize Lower-Priority Items** — Compress rather than remove
3. **Reference Rather Than Include** — Point to documents instead of including content
4. **Archive Context History** — Store removed context for potential reload

---

## 4. Context Update Process

### 4.1 Change Detection Triggers

When a new feature or component is introduced that can affect downstream code or behavior, Context Indexes should be updated. The following events should trigger context updates:

> **Implementation Note:** These triggers can be implemented as manual checklists, CI/CD hooks, or automated tooling depending on project needs. The methodology defines what should happen; implementation approach is project-specific.

**Trigger Events:**

| Event Type | Detection Method | Update Action |
|------------|------------------|---------------|
| New file added | Code review / file watch | Add to affected area maps |
| File modified | Diff analysis / commit review | Update change history |
| API change | Interface comparison / review | Flag dependent contexts |
| Decision created | DEC-#### creation | Link to relevant indexes |
| Spec updated | SPEC-#### modification | Propagate to task contexts |
| Dependency change | Package file review | Update technical context |

### 4.2 Context Update Contents

When triggered, the Context Index should be updated to include:

#### 4.2.1 Affected Areas Reference

```markdown
## Affected Areas Update — YYYY-MM-DD

### Files/Modules/Endpoints Added or Modified

| Path | Change Type | Description |
|------|-------------|-------------|
| `src/module/file.py` | Modified | Updated API signature |
| `api/v2/endpoint` | Added | New REST endpoint |
| `docs/runbook.md` | Modified | Deployment steps updated |

### Impact Assessment

- **Upstream Impact:** List of components that feed into this change
- **Downstream Impact:** List of components that depend on this change
- **Integration Points:** Affected system boundaries
```

#### 4.2.2 Technical Description

```markdown
## Technical Change Description

### Summary

Brief description of what changed and why (1-2 sentences).

### Technical Details

- **Change Category:** Feature / Bug Fix / Refactor / Documentation
- **Architectural Impact:** None / Minor / Significant
- **Pattern Changes:** Any new patterns introduced or existing patterns modified
- **Convention Updates:** Any coding convention changes
```

#### 4.2.3 Structured Changelog Entry

```markdown
## Changelog Entry

| Field | Value |
|-------|-------|
| **Change ID** | `CTX-YYYYMMDD-##` |
| **Date** | YYYY-MM-DD |
| **What Changed** | Concise description of the change |
| **Why** | Rationale for making this change |
| **Potential Impact** | Areas that may be affected |
| **Related IDs** | DEC-####; SPEC-####; REQ-#### |
```

### 4.3 Update Propagation Rules

The following rules define how changes should propagate to affected Context Indexes. Teams may implement these as checklists, scripts, or automated workflows.

**When a decision is created/updated:**

- Update all context indexes that reference this decision
- Add a changelog entry summarizing the decision
- Notify owners of tasks with overlapping scope

**When a specification changes:**

- Update context indexes for related requirements
- Flag implementation tasks as potentially stale
- Add technical description of the spec delta

**When code files change:**

- Update context indexes that list this file
- Assess downstream dependencies
- Add affected areas reference

**When documentation changes:**

- Update context indexes referencing this documentation
- Reconcile living docs if a source doc changed
- Add changelog entry if behavioral guidance changed

---

## 5. Living Documentation

### 5.1 Purpose

Living Documentation serves as the **governed source of truth** for the Context Curation Engine. It captures persistent project knowledge that informs context selection decisions.

### 5.2 Living Docs Structure

Living Documentation explicitly captures:

| Section | Purpose | Example Contents |
|---------|---------|------------------|
| **Technologies & Libraries** | Tech stack inventory | Languages, frameworks, dependencies |
| **Architectural Decisions** | Design constraints | Patterns, boundaries, trade-offs |
| **Coding Conventions** | Style and patterns | Naming, formatting, idioms |
| **Task/Project Rules** | Project-specific guidance | Constraints, requirements, preferences |
| **Agent Instructions** | AI-specific rules | What agents must/must not do |

### 5.3 Technologies and Libraries Section

Document all technologies in use:

```markdown
## Technologies and Libraries

### Languages

| Language | Version | Usage | Notes |
|----------|---------|-------|-------|
| Python | 3.11+ | Primary backend | Type hints required |
| TypeScript | 5.x | Frontend | Strict mode enabled |

### Frameworks

| Framework | Version | Purpose | Configuration |
|-----------|---------|---------|---------------|
| FastAPI | 0.100+ | REST API | See `api/config.py` |
| React | 18.x | UI Components | See `frontend/README.md` |

### Key Dependencies

| Dependency | Purpose | Version Constraints |
|------------|---------|---------------------|
| SQLAlchemy | ORM | ^2.0 (no 1.x patterns) |
| Pydantic | Validation | v2 API only |
```

### 5.4 Architectural Decisions Section

Reference key architectural constraints:

```markdown
## Architectural Decisions

### Current Architecture Style

- **Pattern:** Hexagonal / Clean Architecture
- **Key Boundaries:** Domain ↔ Infrastructure ↔ Presentation
- **Communication:** Sync REST for external; Async events for internal

### Active Constraints

| Constraint | Rationale | Reference |
|------------|-----------|-----------|
| No direct DB access from handlers | Separation of concerns | DEC-0001 |
| All mutations via domain services | Transaction boundaries | DEC-0003 |
| Feature flags for new capabilities | Gradual rollout | SPEC-0101 |

### Deprecated Patterns (Do Not Use)

| Pattern | Replacement | Migration Status |
|---------|-------------|------------------|
| Raw SQL queries | SQLAlchemy ORM | 80% migrated |
| Callback-style async | async/await | Complete |
```

### 5.5 Coding Conventions Section

Capture style and pattern requirements:

```markdown
## Coding Conventions

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `UserService` |
| Functions | snake_case | `get_user_by_id` |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Private | Leading underscore | `_internal_helper` |

### Code Organization

- **File length:** Max 500 lines; split if larger
- **Function length:** Max 50 lines; extract if larger
- **Import order:** stdlib → third-party → local

### Patterns in Use

| Pattern | When to Use | Reference Implementation |
|---------|-------------|-------------------------|
| Repository | Data access | `src/repositories/user_repo.py` |
| Service | Business logic | `src/services/user_service.py` |
| DTO | API boundaries | `src/schemas/user_schema.py` |
```

### 5.6 Task/Project Rules Section

Document project-specific constraints:

```markdown
## Task and Project Rules

### Must-Follow Rules

- [ ] All API changes require OpenAPI spec update
- [ ] Database migrations require DBA review
- [ ] Security-sensitive code requires security sign-off
- [ ] External integrations require integration tests

### Project-Specific Conventions

| Convention | Description | Enforcement |
|------------|-------------|-------------|
| Feature branches | All work in feature branches | CI check |
| Semantic commits | Conventional commit format | Pre-commit hook |
| Test coverage | Min 80% for new code | CI gate |

### Current Restrictions

- **No new dependencies** without DEC-#### approval
- **No breaking changes** to public API without migration path
- **No PII in logs** — use redaction utilities
```

### 5.7 Living Docs Maintenance

Living Documentation must be updated:

| Trigger | Required Update | Responsible Role |
|---------|-----------------|------------------|
| New technology added | Technologies section | Doc Steward |
| Architecture decision made | Decisions section | Spec Curator |
| Convention changed | Conventions section | Doc Steward |
| New project rule | Rules section | Governance Sentinel |
| Agent behavior change | Agent Instructions | Agent Conductor |

---

## 6. Context Curation Workflow

### 6.1 Task Initiation

When starting a new task:

```text
1. Create Context Index from template (CTX-INDEX-template.md)
2. Populate task scope and objectives
3. Identify affected areas from code analysis
4. Load relevant Living Docs sections
5. Reference applicable decisions and specs
6. Document initial assumptions
7. Register with Context Curation Engine
```

### 6.2 During Task Execution

On each turn:

```text
1. Engine evaluates current context
   - Score relevance of each item
   - Identify stale information
   - Detect missing required context

2. Engine curates context
   - Remove items below relevance threshold
   - Load missing high-priority items
   - Summarize medium-priority items

3. Check for propagated updates
   - Process any automatic context updates
   - Incorporate new changelog entries
   - Flag conflicts for resolution

4. Agent proceeds with curated context
```

### 6.3 On Change Detection

When the agent makes changes:

```text
1. Detect change type (code, spec, decision, doc)
2. Identify affected downstream contexts
3. Generate update package:
   - Affected areas reference
   - Technical description
   - Changelog entry
4. Propagate to affected Context Indexes
5. Notify dependent tasks if necessary
```

### 6.4 Task Completion

When completing a task:

```text
1. Finalize Context Index changelog
2. Update Living Docs if conventions changed
3. Propagate final context updates
4. Archive Context Index for reference
5. Deregister from active curation
```

---

## 7. Templates

### 7.1 Context Index Template

Use `templates/context/CTX-INDEX-template.md` for creating task context indexes.

### 7.2 Living Docs Template

Use `templates/context/LIVING-DOCS-template.md` for initializing project living documentation.

### 7.3 Context Update Template

For documenting context propagation updates:

```markdown
# Context Update — CTX-YYYYMMDD-##

**Source Change:** [Change ID or description]
**Propagated To:** [List of affected Context Indexes]
**Date:** YYYY-MM-DD

## Affected Areas

| Path | Change Type | Description |
|------|-------------|-------------|
| | | |

## Technical Description

[Brief technical summary]

## Changelog Entry

- **What Changed:** 
- **Why:** 
- **Potential Impact:** 

## Propagation Status

| Context Index | Status | Notes |
|---------------|--------|-------|
| CTX-TASK-001 | Updated | |
| CTX-TASK-002 | Pending | Awaiting owner review |
```

---

## 8. Integration with Agent Trust Framework

### 8.1 Trust-Level Context Access

| Trust Level | Context Access | Curation Authority |
|-------------|----------------|-------------------|
| Level 0 (Supervised) | Read-only; human-curated context | None |
| Level 1 (Guided) | Read with automated curation | Request additions |
| Level 2 (Autonomous) | Full read; propose updates | Update own task context |
| Level 3 (Trusted Partner) | Full access | Update any context; modify Living Docs |

### 8.2 Context Curation Escalation

Agents should escalate to human review when:

- Context conflicts are detected between sources
- Living Docs appear outdated relative to code
- Assumed context cannot be verified
- Change propagation affects high-risk areas

---

## 9. Governance and Audit

### 9.1 Context Index Audit Trail

All Context Indexes maintain:

- Creation timestamp and creator
- All modification timestamps and modifiers
- Changelog of all entries
- Propagation history (incoming and outgoing)

### 9.2 Living Docs Version Control

Living Documentation:

- Tracked in version control with full history
- Changes require changelog entry
- Major changes require DEC-#### approval
- Quarterly review by Governance Sentinel

### 9.3 Metrics and Health Checks

Monitor context curation effectiveness through periodic assessment. These metrics should be measured during retrospectives or audits.

**Measurement Methodology:**

| Metric | How to Measure | Target | Action if Below Target |
|--------|----------------|--------|------------------------|
| **Context relevance hit rate** | Review completed tasks; count how often loaded context was actually used vs. unused | > 85% used | Review curation criteria; tighten relevance scoring |
| **Stale context incidents** | Count tasks where outdated context caused rework or errors | < 5% of tasks | Increase update frequency; improve trigger coverage |
| **Propagation completeness** | Audit changes; verify all affected indexes were updated | 100% coverage | Review propagation rules; add missing triggers |
| **Living Docs currency** | Check last review date in Living Docs | < 30 days since review | Schedule review; assign owner |

**Health Check Cadence:**

- **Weekly:** Review propagation completeness for recent changes
- **Monthly:** Assess relevance hit rate from completed tasks
- **Quarterly:** Full Living Docs review and stale context audit

---

## 10. Related Documentation

- `core/METHOD-0001-core-method.md` — Core methodology principles
- `governance/METHOD-0002-phase-driver-checklists.md` — Unified Lifecycle & Checklists
- `governance/METHOD-0003-role-handbook.md` — Role definitions
- `operations/METHOD-0004-ai-agent-workflows.md` — AI Agent Handbook
- `operations/METHOD-0005-operations-production-support.md` — Operations support
- `templates/context/CTX-INDEX-template.md` — Context Index template
- `templates/context/LIVING-DOCS-template.md` — Living Documentation template
