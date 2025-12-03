# Three-Pathway System Migration Guide

## Overview

This document describes the consolidation from the 6-pathway system to exactly 3 deployment pathways in RJW-IDD methodology.

## Changes Summary

### Previous System (6 Pathways)
- Minimal Risk (Section 2.1)
- Low Risk (Section 2.2)  
- Medium Risk (Section 2.3)
- High Risk (Section 3)
- Critical Risk (Section 4)
- Prototype Mode (Section 6)

### New System (3 Pathways)
- **Streamlined Path (Section 2.1)** — Consolidates Minimal/Low/Medium/High/Critical into single production path
- **YOLO Path (Section 2.2)** — Formalized autonomous self-approval mode
- **Prototype Path (Section 2.3)** — Moved from Section 6, unchanged in functionality

## Implementation Status

### Code Changes ✅ COMPLETE
- [x] `src/governance/manager.py` - Added `RiskLevel` enum with 3 pathways
- [x] `src/governance/manager.py` - Added `RiskClassifier` class
- [x] `src/governance/manager.py` - Updated trust authorization logic
- [x] `src/discovery/research.py` - Added `UserEvidenceParser` class
- [x] `src/discovery/research.py` - Added user research handling
- [x] `src/interaction/optimizer.py` - Added `process_user_research()` method
- [x] Tests added - 95 tests passing

### Documentation Changes 🚧 IN PROGRESS

Files that need updates:

#### 1. `rjw-idd-methodology/governance/METHOD-0002-phase-driver-checklists.md`

**Section 1: Risk Selection Logic**
- Replace risk classification flowchart with deployment pathway flowchart
- Update from "6 risk levels" to "3 deployment pathways"
- New flowchart: Is Prototype? → Yes: Section 2.3 | No: Want YOLO? → Yes: Section 2.2 | No: Section 2.1

**Sections 2.1-2.3: Replace with Three Pathways**
```markdown
### 2.1 Streamlined Path
- Use for: All production-ready changes
- Graduated response based on scope (Trivial/Simple/Standard/Complex/Critical)
- User requirements exception documented
- User research handling documented

### 2.2 YOLO Path  
- Use for: Autonomous self-approval mode
- ChecklistEnforcer validation
- Trust level: Autonomous+ required
- Auto-approve on pass, auto-reject on fail

### 2.3 Prototype Path
- Move content from Section 6 here
- Keep/Flex/Unknown tagging unchanged
- No functionality changes
```

**Section 3-4: Rename and Consolidate**
- Section 3 becomes "Full Discovery + Execution Loop (For Complex/Critical Streamlined Changes)"
- Section 4 content merges into Section 3 as "Critical Scope Requirements"
- Remove as separate sections since now part of Streamlined Path

**Section 5: Agent Trust Integration**
- Update pathway access tables to show 3 pathways instead of 6

**Section 6: Delete**
- Content moved to Section 2.3

**Section 8: Quick-Start Pathways Summary**
- Update from 5 pathways (A-E) to 3 pathways:
  - Pathway A: Streamlined (Trivial Scope) - 5 minutes
  - Pathway B: Streamlined (Simple-Standard Scope) - 30 min to 2 hours
  - Pathway C: Streamlined (Complex Scope) - 1-5 days
  - Pathway D: Streamlined (Critical Scope) - 5-15 days
  - Pathway E: YOLO - Variable (checklist-driven)
  - Pathway F: Prototype - 2 days to 4 weeks

**Section 9: Implementing Lifecycle**
- Update RiskLevel enum example to show 3 values
- Update RiskClassifier code to show new classify() logic
- Update ChecklistEnforcer to remove risk-specific checklists

#### 2. `README.md`

**Section "Core Methodology Components"**
- Update METHOD-0002 description:
  ```markdown
  The **single source of truth** for all process checklists:
  - **Three Deployment Pathways** — Streamlined, YOLO, and Prototype
  - **Streamlined Path** — Single production path with graduated response
  - **YOLO Path** — Autonomous self-approval with checklist validation
  - **Prototype Path** — Relaxed gates for POC/spike work
  - **Agent Trust Integration** — Trust levels linked to pathway access
  ```

**Section "Implementing RJW-IDD in Your Agent"**
- Update RiskLevel enum example
- Update risk classification logic example

#### 3. `docs/README.md`

Update table:
```markdown
| **Unified Lifecycle & Checklists** | `governance/METHOD-0002-phase-driver-checklists.md` | All process checklists (Streamlined, YOLO, Prototype pathways) |
```

## User Evidence Handling

### New Capabilities ✅ IMPLEMENTED

1. **User Requirements Exception**
   - User requirements do NOT require research-based evidence
   - Only the user can document evidence for their own requirements
   - Exception implemented in `require_evidence_for_artifact(is_user_requirement=True)`

2. **User-Provided Research**
   - Automatically parsed from any format (plain text, markdown, bullets, etc.)
   - Automatically reformatted to EVD-#### template
   - Preserved with full traceability

3. **Priority Weighting**
   - User research gets equal weight as agent research by default
   - User research gets elevated weight ONLY when user explicitly specifies
   - Implemented via `user_priority` parameter

4. **Automatic Parsing**
   - `UserEvidenceParser.parse_user_research()` extracts structured data
   - Handles: title, summary, key insights, sources, methodology, conclusions
   - Supports: URLs, citations, markdown sections, bullet lists

5. **Evidence Reformatting**
   - `UserEvidenceParser.reformat_to_evidence()` generates EVD-#### format
   - Follows `rjw-idd-methodology/templates/evidence/EVD-template.md` structure
   - Marks as `source: user-provided`
   - Includes original raw input for traceability

### API Usage

```python
from src.discovery.research import ResearchHarvester
from src.interaction.optimizer import PromptOptimizer

# Harvest user-provided research
harvester = ResearchHarvester()
evd_id = harvester.harvest_user_research(
    raw_input="User's research content...",
    user_priority=False,  # Equal weight (default)
    curator="User Name"
)

# Or through optimizer
optimizer = PromptOptimizer()
result = optimizer.process_user_research(
    research_content="User's findings...",
    user_priority=True,  # Elevated weight (explicit)
    curator="Security Team"
)
```

## Testing

All 95 tests passing:
- 23 tests for new RiskClassifier and three pathways
- 17 tests for UserEvidenceParser and user research handling
- 9 tests for interaction optimizer user research processing
- 46 existing tests remain passing (backward compatibility)

## Backward Compatibility

The implementation maintains backward compatibility:
- Old risk levels (minimal, low, medium, high, critical) still work in `_check_trust_authorization()`
- Existing code using old risk levels continues to function
- Gradual migration path available

## Next Steps

1. Complete METHOD-0002 documentation updates
2. Update README.md with three-pathway references
3. Update docs/README.md
4. Create migration examples for existing agents
5. Update any addon documentation that references old pathways
