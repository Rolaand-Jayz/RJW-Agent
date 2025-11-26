# Living Documentation Reconciliation Log

> Copy this file into your project workspace (for example `docs/living-docs-reconciliation.md`). Do not edit the template in-place.

Track documentation gaps and ensure documentation updates ship alongside code changes.

## Outstanding Documentation Gaps

| gap_id | doc_id | description | related_change | owner | due_date | status |
|--------|--------|-------------|----------------|-------|----------|--------|
| GAP-001 | `DOC-####` | Description of gap | `change-YYYYMMDD-##` | Role | YYYY-MM-DD | Open/In Progress/Resolved |

## Status Definitions

| Status | Description |
|--------|-------------|
| **Open** | Gap identified, not yet addressed |
| **In Progress** | Documentation update underway |
| **Resolved** | Gap closed, documentation updated |
| **Deferred** | Gap acknowledged, scheduled for future resolution |

## Gap Categories

| Category | Count | Open | In Progress | Resolved | Deferred |
|----------|-------|------|-------------|----------|----------|
| User Documentation | 0 | 0 | 0 | 0 | 0 |
| API Documentation | 0 | 0 | 0 | 0 | 0 |
| Runbooks | 0 | 0 | 0 | 0 | 0 |
| Architecture Docs | 0 | 0 | 0 | 0 | 0 |
| Standards | 0 | 0 | 0 | 0 | 0 |

## Recently Resolved Gaps

| gap_id | doc_id | resolution_date | change_log_ref |
|--------|--------|-----------------|----------------|
| GAP-### | `DOC-####` | YYYY-MM-DD | `change-YYYYMMDD-##` |

## Documentation Debt Summary

- **Total Open Gaps:** 0
- **Critical Gaps (blocking release):** 0
- **Average Age of Open Gaps:** 0 days
- **Last Review Date:** YYYY-MM-DD

## Guidelines

1. **Gap Identification:** Log gaps when code changes affect documentation but docs are not updated in the same changeset.
2. **Blocking Gaps:** Mark gaps as blocking if they prevent users from successfully using the product.
3. **Review Cadence:** Review this log at each phase gate and before releases.
4. **Resolution:** Update the status and reference the change log entry when gaps are resolved.
5. **Integration Guard:** Consider implementing a CI guard to prevent merges with unresolved blocking gaps (see `METHOD-0004` for reference).

## Cross-References

- Documentation Standards: `docs/standards/DOC-0006`
- Change Log: `docs/change-log.md`
- Phase Checklists: `METHOD-0002-phase-driver-checklists.md`
