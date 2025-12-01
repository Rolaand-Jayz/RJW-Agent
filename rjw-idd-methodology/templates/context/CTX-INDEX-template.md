# CTX-INDEX-XXXX — Task Context Index

> Copy this file into your project workspace (for example `docs/context/CTX-INDEX-0001.md`). Do not edit the template in-place.

**Task ID:** TASK-XXXX
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Owner:** [Role/Name]

---

## 1. Task Scope

### 1.1 Objectives

Describe what this task aims to accomplish:

1. Primary objective
2. Secondary objectives (if any)

### 1.2 Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### 1.3 Out of Scope

Explicitly list what is NOT part of this task:

- Item 1
- Item 2

### 1.4 Constraints

| Constraint | Description | Source |
|------------|-------------|--------|
| Time | Deadline or time-box | Project plan |
| Technical | Technical limitations | Architecture |
| Resource | Resource constraints | Team capacity |

---

## 2. Affected Areas

### 2.1 Files and Modules

| Path | Type | Relationship | Notes |
|------|------|--------------|-------|
| `src/module/file.py` | Source | Primary | Main implementation file |
| `tests/test_file.py` | Test | Supporting | Test coverage |
| `docs/api.md` | Doc | Update needed | API documentation |

### 2.2 Endpoints and Interfaces

| Endpoint/Interface | Type | Impact | Notes |
|--------------------|------|--------|-------|
| `POST /api/v1/resource` | REST API | Modified | New parameter added |
| `EventBus.publish()` | Internal | Unchanged | Dependency only |

### 2.3 Integration Points

| System | Integration Type | Direction | Notes |
|--------|------------------|-----------|-------|
| Database | Data persistence | Read/Write | Uses `users` table |
| Cache | Performance | Read | Redis cache layer |
| External API | Third-party | Outbound | Payment processor |

---

## 3. Technical Context

### 3.1 Relevant Decisions

| Decision ID | Title | Relevance |
|-------------|-------|-----------|
| `DEC-0001` | Decision title | Why this decision matters for this task |
| `DEC-0002` | Decision title | Why this decision matters for this task |

### 3.2 Applicable Specifications

| Spec ID | Title | Relevance |
|---------|-------|-----------|
| `SPEC-0001` | Spec title | How this spec applies |
| `SPEC-0002` | Spec title | How this spec applies |

### 3.3 Architecture Patterns

| Pattern | Usage | Reference |
|---------|-------|-----------|
| Repository Pattern | Data access | `src/repositories/` |
| Service Layer | Business logic | `src/services/` |

### 3.4 Coding Conventions

Key conventions applicable to this task:

- Convention 1: Description
- Convention 2: Description
- Convention 3: Description

---

## 4. Assumptions

### 4.1 Verified Assumptions

Assumptions that have been confirmed:

| Assumption | Verification | Date |
|------------|--------------|------|
| Database schema is stable | Confirmed with DBA | YYYY-MM-DD |
| API versioning follows semver | Per SPEC-0001 | YYYY-MM-DD |

### 4.2 Working Assumptions

Assumptions being treated as true but not yet verified:

| Assumption | Risk if False | Validation Plan |
|------------|---------------|-----------------|
| Cache invalidation is handled | Medium | Verify in integration test |
| Rate limiting is in place | Low | Check API gateway config |

### 4.3 Provisional Assumptions

Assumptions known to be temporary:

| Assumption | Reason Provisional | Resolution Plan |
|------------|-------------------|-----------------|
| Mock external API | Service not available | Replace before prod |
| Hardcoded config values | Speed of development | Externalize in config |

---

## 5. Dependencies

### 5.1 Upstream Dependencies

Tasks that must complete before this task can proceed:

| Task ID | Description | Status | Blocking? |
|---------|-------------|--------|-----------|
| TASK-001 | Database migration | Complete | No |
| TASK-002 | API authentication | In Progress | Yes |

### 5.2 Downstream Dependencies

Tasks that depend on this task completing:

| Task ID | Description | Impact if Delayed |
|---------|-------------|-------------------|
| TASK-004 | Frontend integration | UI work blocked |
| TASK-005 | Performance testing | Cannot proceed |

### 5.3 Parallel Work

Other work happening concurrently that may interact:

| Task ID | Description | Potential Conflicts |
|---------|-------------|---------------------|
| TASK-003 | Refactor user service | May touch same files |

---

## 6. Change History

### 6.1 Relevant Prior Changes

Changes that preceded and informed this task:

| Change ID | Date | Description | Impact on This Task |
|-----------|------|-------------|---------------------|
| `CTX-20240101-01` | 2024-01-01 | Added user authentication | Provides auth context |
| `CTX-20240115-01` | 2024-01-15 | Refactored data layer | Changed repository pattern |

### 6.2 Changes Made During This Task

Log changes as they occur:

| Change ID | Date | What Changed | Why | Potential Impact |
|-----------|------|--------------|-----|------------------|
| `CTX-YYYYMMDD-##` | YYYY-MM-DD | Description | Rationale | Downstream effects |

---

## 7. Context Curation Status

### 7.1 Current Context Relevance

Assign relevance scores (0.0-1.0) to track context priority. Update scores as task progresses.

> **Scoring Guide:** 1.0 = essential for current step; 0.8 = directly relevant; 0.6 = helpful background; 0.4 = may need later; 0.2 = peripherally related; 0.0 = not relevant. See METHOD-0006 Section 3.3 for detailed guidance.

| Context Category | Relevance Score | Last Evaluated | Notes |
|------------------|-----------------|----------------|-------|
| Task Scope | [Score] | YYYY-MM-DD | [Notes] |
| Affected Areas | [Score] | YYYY-MM-DD | [Notes] |
| Technical Context | [Score] | YYYY-MM-DD | [Notes] |
| Assumptions | [Score] | YYYY-MM-DD | [Notes] |

### 7.2 Context Removed

Items removed from active context during curation:

| Item | Removal Date | Reason | Archived Location |
|------|--------------|--------|-------------------|
| | | | |

### 7.3 Context Added

Items added to context during task execution:

| Item | Addition Date | Reason | Source |
|------|---------------|--------|--------|
| | | | |

---

## 8. Cross-References

### 8.1 Related Context Indexes

| Context ID | Task | Relationship |
|------------|------|--------------|
| `CTX-INDEX-0001` | Task description | Shared dependency |

### 8.2 Living Documentation

| Living Doc Section | Relevance |
|--------------------|-----------|
| Technologies & Libraries | Tech stack context |
| Architectural Decisions | Pattern guidance |
| Coding Conventions | Style requirements |

### 8.3 Governance Links

| Artefact | Purpose |
|----------|---------|
| `docs/change-log.md` | Track changes |
| `DEC-####` | Related decisions |
| `SPEC-####` | Related specifications |

---

## 9. Notes

### 9.1 Open Questions

Questions that need resolution:

1. Question 1 — Status: Open/Resolved
2. Question 2 — Status: Open/Resolved

### 9.2 Learnings

Insights gained during task execution:

- Learning 1
- Learning 2

### 9.3 Recommendations

Suggestions for future work:

- Recommendation 1
- Recommendation 2

---

## Audit Trail

| Action | Date | Actor | Notes |
|--------|------|-------|-------|
| Created | YYYY-MM-DD | Role/Name | Initial creation |
| Updated | YYYY-MM-DD | Role/Name | Description of update |
| Archived | YYYY-MM-DD | Role/Name | Task completed |
