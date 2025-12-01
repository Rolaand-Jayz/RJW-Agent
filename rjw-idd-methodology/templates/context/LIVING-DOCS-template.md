# Living Documentation

> Copy this file into your project workspace (for example `docs/living-docs.md`). Do not edit the template in-place.

**Project:** [Project Name]
**Last Updated:** YYYY-MM-DD
**Maintainer:** Doc Steward

---

## Overview

This document serves as the **governed source of truth** for project knowledge that informs the Context Curation Engine. It captures persistent information about technologies, architecture, conventions, and rules that apply across all tasks.

> **Important:** Update this document whenever the project evolves. Changes to Living Documentation automatically propagate to active Context Indexes.

---

## 1. Technologies and Libraries

### 1.1 Languages

| Language | Version | Usage | Notes |
|----------|---------|-------|-------|
| [Language] | [Version] | [Primary/Secondary/Scripting] | [Constraints or requirements] |

**Language-Specific Conventions:**

- [Language]: Convention 1, Convention 2
- [Language]: Convention 1, Convention 2

### 1.2 Frameworks

| Framework | Version | Purpose | Configuration Reference |
|-----------|---------|---------|------------------------|
| [Framework] | [Version] | [Purpose] | `path/to/config` |

**Framework Guidelines:**

- [Framework]: Key guidelines and patterns to follow

### 1.3 Key Dependencies

| Dependency | Version Constraint | Purpose | Notes |
|------------|-------------------|---------|-------|
| [Package] | [^x.y / >=x.y] | [Purpose] | [Migration notes, deprecation warnings] |

**Dependency Management Rules:**

- New dependencies require `DEC-####` approval
- Version constraints: [Describe policy]
- Security updates: [Describe policy]

### 1.4 Development Tools

| Tool | Purpose | Required? | Configuration |
|------|---------|-----------|---------------|
| [Tool] | [Purpose] | Yes/No | `path/to/config` |

---

## 2. Architectural Decisions and Constraints

### 2.1 Architecture Style

**Current Architecture:**

- **Pattern:** [Monolith / Microservices / Modular Monolith / Hexagonal / etc.]
- **Key Boundaries:** [Domain ↔ Infrastructure, etc.]
- **Communication Patterns:** [Sync/Async, REST/GraphQL/gRPC/Events]

**Architecture Diagram:**

```text
[Include or reference architecture diagram]
```

### 2.2 Active Architectural Constraints

| Constraint | Description | Rationale | Reference |
|------------|-------------|-----------|-----------|
| [Constraint Name] | [What must/must not be done] | [Why this constraint exists] | `DEC-####` |

### 2.3 Key Design Decisions

| Decision | Summary | Date | Reference |
|----------|---------|------|-----------|
| `DEC-####` | [Brief summary] | YYYY-MM-DD | [Link] |

### 2.4 Deprecated Patterns

Patterns that should NOT be used in new code:

| Pattern | Replacement | Migration Status | Deadline |
|---------|-------------|------------------|----------|
| [Old Pattern] | [New Pattern] | [% migrated] | [Date if applicable] |

### 2.5 Technical Debt Register

Known technical debt items:

| Item | Impact | Priority | Tracked In |
|------|--------|----------|------------|
| [Debt Item] | [Low/Medium/High] | [P1/P2/P3] | [Issue ID] |

---

## 3. Coding Conventions and Patterns

### 3.1 Naming Conventions

| Element | Convention | Example | Enforcement |
|---------|------------|---------|-------------|
| Classes | [Convention] | `ExampleClass` | [Lint rule] |
| Functions/Methods | [Convention] | `example_function` | [Lint rule] |
| Variables | [Convention] | `exampleVariable` | [Lint rule] |
| Constants | [Convention] | `EXAMPLE_CONSTANT` | [Lint rule] |
| Files | [Convention] | `example_file.py` | [Lint rule] |
| Directories | [Convention] | `example_dir/` | [Manual review] |

### 3.2 Code Organization

**File Structure:**

```text
[Project root structure with annotations]
```

**File Guidelines:**

- Maximum file length: [N lines]
- Maximum function length: [N lines]
- Import ordering: [stdlib → third-party → local]

### 3.3 Standard Patterns

| Pattern | When to Use | Reference Implementation |
|---------|-------------|-------------------------|
| [Pattern Name] | [Use case description] | `path/to/example` |

**Pattern Guidelines:**

- [Pattern]: Detailed guidelines for correct usage

### 3.4 Error Handling

| Context | Pattern | Example |
|---------|---------|---------|
| [API Layer] | [Pattern] | [Brief example] |
| [Service Layer] | [Pattern] | [Brief example] |
| [Data Layer] | [Pattern] | [Brief example] |

### 3.5 Logging and Observability

| Level | Usage | Examples |
|-------|-------|----------|
| DEBUG | [When to use] | [Example messages] |
| INFO | [When to use] | [Example messages] |
| WARN | [When to use] | [Example messages] |
| ERROR | [When to use] | [Example messages] |

**Logging Requirements:**

- [Requirement 1]
- [Requirement 2]

### 3.6 Testing Conventions

| Test Type | Location | Naming | Coverage Requirement |
|-----------|----------|--------|---------------------|
| Unit | [Path] | [Convention] | [%] |
| Integration | [Path] | [Convention] | [%] |
| E2E | [Path] | [Convention] | [%] |

**Testing Guidelines:**

- [Guideline 1]
- [Guideline 2]

---

## 4. Task and Project-Specific Rules

### 4.1 Must-Follow Rules

These rules must always be followed. Violations require immediate correction.

- [ ] Rule 1: [Description]
- [ ] Rule 2: [Description]
- [ ] Rule 3: [Description]

### 4.2 Should-Follow Guidelines

These guidelines should be followed unless there's documented justification.

- Guideline 1: [Description]
- Guideline 2: [Description]

### 4.3 Current Restrictions

Temporary or permanent restrictions in effect:

| Restriction | Reason | Duration | Exception Process |
|-------------|--------|----------|-------------------|
| [Restriction] | [Reason] | [Permanent/Until date] | [How to get exception] |

### 4.4 Approval Requirements

| Change Type | Approval Required From | Documentation Required |
|-------------|----------------------|----------------------|
| [Change Type] | [Role/Team] | [Artefacts needed] |

### 4.5 Quality Gates

| Gate | Criteria | Enforcement | Bypass Process |
|------|----------|-------------|----------------|
| [Gate Name] | [Pass criteria] | [CI/Manual] | [How to bypass if needed] |

---

## 5. Agent Instructions

### 5.1 Agent Behavioral Rules

Rules that AI agents must follow:

**Must Do:**

- [ ] [Instruction 1]
- [ ] [Instruction 2]
- [ ] [Instruction 3]

**Must Not Do:**

- [ ] [Prohibition 1]
- [ ] [Prohibition 2]
- [ ] [Prohibition 3]

### 5.2 Context Preferences

How agents should prioritize context:

| Context Type | Priority | Notes |
|--------------|----------|-------|
| [Type] | High/Medium/Low | [When to include] |

### 5.3 Escalation Triggers

Agents must escalate to human review when:

- [Trigger 1]
- [Trigger 2]
- [Trigger 3]

### 5.4 Output Requirements

All agent outputs must:

- [Requirement 1]
- [Requirement 2]

---

## 6. Environment and Configuration

### 6.1 Environments

| Environment | Purpose | Access | Notes |
|-------------|---------|--------|-------|
| Development | Local development | All developers | |
| Staging | Pre-production testing | Team + QA | |
| Production | Live users | Restricted | |

### 6.2 Configuration Management

| Config Type | Location | Format | Secrets Handling |
|-------------|----------|--------|------------------|
| [Type] | [Path/Service] | [Format] | [How secrets are managed] |

### 6.3 Feature Flags

| Flag | Purpose | Default | Environments Enabled |
|------|---------|---------|---------------------|
| [Flag Name] | [Purpose] | On/Off | [Environments] |

---

## 7. Security and Compliance

### 7.1 Security Requirements

| Requirement | Description | Verification |
|-------------|-------------|--------------|
| [Requirement] | [Description] | [How verified] |

### 7.2 Data Handling Rules

| Data Type | Classification | Handling Rules |
|-----------|----------------|----------------|
| [Type] | [PII/Sensitive/Public] | [Rules] |

### 7.3 Compliance Requirements

| Regulation | Applicability | Key Requirements |
|------------|---------------|------------------|
| [Regulation] | [Scope] | [Key requirements] |

---

## 8. Integration Points

### 8.1 External Systems

| System | Purpose | Protocol | Documentation |
|--------|---------|----------|---------------|
| [System] | [Purpose] | [REST/GraphQL/etc.] | [Link to docs] |

### 8.2 Internal Services

| Service | Owner | Interface | Notes |
|---------|-------|-----------|-------|
| [Service] | [Team] | [Type] | [Notes] |

---

## 9. Change Management

### 9.1 Recent Changes

| Date | Section | Change | Reference |
|------|---------|--------|-----------|
| YYYY-MM-DD | [Section] | [Description] | `change-YYYYMMDD-##` |

### 9.2 Pending Updates

| Section | Planned Change | Target Date | Owner |
|---------|----------------|-------------|-------|
| [Section] | [Description] | YYYY-MM-DD | [Role] |

### 9.3 Review Schedule

- **Last Review:** YYYY-MM-DD
- **Next Scheduled Review:** YYYY-MM-DD
- **Review Frequency:** [Monthly/Quarterly/etc.]

---

## Cross-References

- Context Curation Engine: `operations/METHOD-0006-context-curation-engine.md`
- Context Index Template: `templates/context/CTX-INDEX-template.md`
- Change Log: `docs/change-log.md`
- Decision Records: `docs/decisions/`

---

## Audit Trail

| Action | Date | Actor | Notes |
|--------|------|-------|-------|
| Created | YYYY-MM-DD | [Role/Name] | Initial creation |
| Reviewed | YYYY-MM-DD | [Role/Name] | Quarterly review |
| Updated | YYYY-MM-DD | [Role/Name] | [Description] |
