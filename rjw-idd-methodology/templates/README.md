# RJW-IDD Templates

This directory contains boilerplate templates for all artefact types used in the RJW-IDD methodology. Copy templates into your project workspace; **never modify the originals**.

## Directory Structure

```text
templates/
├── decisions/              # Decision record templates
│   └── DEC-template.md     # Tree-of-Thought decision capture
├── requirements/           # Requirement templates
│   └── REQ-template.md     # Requirement specification
├── specs/                  # Specification templates
│   └── SPEC-template.md    # Technical specification
├── evidence/               # Evidence templates
│   └── EVD-template.md     # Research evidence capture
├── testing/                # Test case templates
│   └── TEST-template.md    # Test case definition
├── documentation/          # Documentation templates
│   └── DOC-template.md     # Standards, runbooks, guides
├── governance/             # Governance templates
│   ├── CHANGE-LOG-template.md              # Change tracking
│   ├── STAGE-AUDIT-LOG-template.md         # Phase audit reflections
│   ├── REQ-LEDGER-template.md              # Requirement traceability
│   └── LIVING-DOCS-RECONCILIATION-template.md  # Documentation gap tracking
├── context/                # Context curation templates
│   ├── CTX-INDEX-template.md               # Task context index
│   └── LIVING-DOCS-template.md             # Project living documentation
├── PROTO-template.md       # Prototype record (POC/spike)
├── DEC-LITE-template.md    # Lightweight decision (Low/Medium risk)
└── AGENT-TRUST-template.md # Agent trust level changes
```

## Template Categories

### Decisions (`decisions/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `DEC-template.md` | Capture strategic choices with options, trade-offs, and rationale | `DEC-####` |

### Requirements (`requirements/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `REQ-template.md` | Define what the system must do or how it must behave | `REQ-####` |

### Specifications (`specs/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `SPEC-template.md` | Technical design addressing requirements | `SPEC-####` |

### Evidence (`evidence/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `EVD-template.md` | Research findings supporting decisions | `EVD-####` |

### Testing (`testing/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `TEST-template.md` | Verify specifications meet acceptance criteria | `TEST-####` |

### Documentation (`documentation/`)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `DOC-template.md` | Standards, runbooks, guides, and references | `DOC-####` |

### Governance (`governance/`)

| Template | Purpose | Usage |
|----------|---------|-------|
| `CHANGE-LOG-template.md` | Track methodology/project changes | `docs/change-log.md` |
| `STAGE-AUDIT-LOG-template.md` | Phase gate audit reflections | `logs/LOG-####-stage-audits.md` |
| `REQ-LEDGER-template.md` | Requirement traceability matrix | `artifacts/ledgers/requirement-ledger.md` |
| `LIVING-DOCS-RECONCILIATION-template.md` | Documentation debt tracking | `docs/living-docs-reconciliation.md` |

### Prototypes (Root Level)

| Template | Purpose | Identifier Pattern |
|----------|---------|-------------------|
| `PROTO-template.md` | Rapid POC/spike documentation with Keep/Flex/Unknown tagging | `PROTO-####` |

### Context Curation (`context/`)

| Template | Purpose | Usage |
|----------|---------|-------|
| `CTX-INDEX-template.md` | Task-specific context index for AI agent work | `docs/context/CTX-INDEX-####.md` |
| `LIVING-DOCS-template.md` | Project living documentation as governed source of truth | `docs/living-docs.md` |

## How to Use

### 1. Copy the Template

```bash
cp rjw-idd-methodology/templates/decisions/DEC-template.md \
   my-project/docs/decisions/DEC-0001.md
```

### 2. Rename with Sequential ID

Use monotonically increasing identifiers within your project namespace.

### 3. Fill in the Template

Replace placeholder values (XXXX, YYYY-MM-DD, etc.) with actual content.

### 4. Link to Related Artefacts

Populate traceability sections to maintain the audit trail.

### 5. Update Governance Logs

Record the new artefact in your change log and update relevant ledgers.

## Traceability Guidelines

Every artefact should trace to related artefacts:

```text
Evidence (EVD) → Requirements (REQ) → Specifications (SPEC) → Tests (TEST)
                          ↓
                    Decisions (DEC)
                          ↓
                  Documentation (DOC)
```

Maintain bidirectional links where possible to support audits.

## Integration with Method Phases

| Phase | Primary Templates |
|-------|-------------------|
| **Discovery — Research** | `EVD-template.md`, `DEC-template.md` |
| **Discovery — Specification** | `REQ-template.md`, `SPEC-template.md`, `DEC-template.md` |
| **Execution** | `TEST-template.md`, `DOC-template.md` |
| **Governance** | All governance templates |
| **Context Curation** | `CTX-INDEX-template.md`, `LIVING-DOCS-template.md` |

## Add-on Specific Templates

Domain-specific add-ons provide additional templates:

- **3D Game Core:** `addons/3d-game-core/specs/templates/`
- **Video AI Enhancer:** `addons/video-ai-enhancer/specs/templates/`

These extend the base templates with domain-specific sections and acceptance criteria.

## Implementing Template Management in Your Agent

When building an agent that uses RJW-IDD templates, implement these patterns for template handling:

### Template Loading and Instantiation

```python
from pathlib import Path
from datetime import datetime
import re

class TemplateManager:
    """Manages RJW-IDD templates for agent use."""
    
    def __init__(self, templates_dir: str):
        self.templates_dir = Path(templates_dir)
        self.id_counters = {}  # Track ID sequences per type
    
    def load_template(self, template_path: str) -> str:
        """Load a template file."""
        full_path = self.templates_dir / template_path
        return full_path.read_text()
    
    def get_next_id(self, prefix: str) -> str:
        """Generate next sequential ID for artifact type."""
        if prefix not in self.id_counters:
            self.id_counters[prefix] = self._scan_existing_ids(prefix)
        self.id_counters[prefix] += 1
        return f"{prefix}-{self.id_counters[prefix]:04d}"
    
    def instantiate_decision(self, title: str, context: str,
                             options: list, chosen: str, 
                             rationale: str) -> dict:
        """Create a decision record from template."""
        template = self.load_template("decisions/DEC-template.md")
        dec_id = self.get_next_id("DEC")
        
        content = template.replace("DEC-XXXX", dec_id)
        content = content.replace("[Title]", title)
        content = content.replace("YYYY-MM-DD", datetime.now().strftime("%Y-%m-%d"))
        content = content.replace("[Context]", context)
        content = content.replace("[Options]", "\n".join(f"- {o}" for o in options))
        content = content.replace("[Decision]", chosen)
        content = content.replace("[Rationale]", rationale)
        
        return {
            'id': dec_id,
            'content': content,
            'type': 'decision'
        }
    
    def instantiate_requirement(self, description: str,
                                acceptance_criteria: list,
                                evidence_refs: list = None) -> dict:
        """Create a requirement from template."""
        template = self.load_template("requirements/REQ-template.md")
        req_id = self.get_next_id("REQ")
        
        content = template.replace("REQ-XXXX", req_id)
        content = content.replace("[Description]", description)
        content = content.replace(
            "[Acceptance Criteria]",
            "\n".join(f"- [ ] {c}" for c in acceptance_criteria)
        )
        content = content.replace(
            "[Evidence]",
            "\n".join(evidence_refs or ["None"])
        )
        
        return {
            'id': req_id,
            'content': content,
            'type': 'requirement',
            'evidence_refs': evidence_refs or []
        }
    
    def instantiate_spec(self, title: str, requirements: list,
                         design: str, interfaces: list = None) -> dict:
        """Create a specification from template."""
        template = self.load_template("specs/SPEC-template.md")
        spec_id = self.get_next_id("SPEC")
        
        content = template.replace("SPEC-XXXX", spec_id)
        content = content.replace("[Title]", title)
        content = content.replace(
            "[Requirements]",
            "\n".join(f"- {r}" for r in requirements)
        )
        content = content.replace("[Design]", design)
        
        return {
            'id': spec_id,
            'content': content,
            'type': 'spec',
            'requirement_refs': requirements
        }
```

### Traceability Management

```python
class TraceabilityManager:
    """Manages artifact traceability per RJW-IDD guidelines."""
    
    def __init__(self):
        self.artifacts = {}  # id -> artifact
        self.links = []  # (from_id, to_id, link_type)
    
    def register_artifact(self, artifact: dict):
        """Register an artifact for traceability."""
        self.artifacts[artifact['id']] = artifact
        
        # Auto-link based on references
        for ref in artifact.get('evidence_refs', []):
            self.add_link(artifact['id'], ref, 'derived_from')
        for ref in artifact.get('requirement_refs', []):
            self.add_link(artifact['id'], ref, 'implements')
    
    def add_link(self, from_id: str, to_id: str, link_type: str):
        """Add a traceability link between artifacts."""
        self.links.append((from_id, to_id, link_type))
    
    def get_trace_chain(self, artifact_id: str) -> dict:
        """Get full traceability chain for an artifact.
        
        Returns the chain: Evidence → Requirements → Specs → Tests
        """
        chain = {
            'artifact': artifact_id,
            'derived_from': [],
            'implements': [],
            'verified_by': []
        }
        
        for from_id, to_id, link_type in self.links:
            if from_id == artifact_id:
                chain.get(link_type, []).append(to_id)
            elif to_id == artifact_id:
                # Reverse lookup
                if link_type == 'implements':
                    chain['derived_from'].append(from_id)
                elif link_type == 'verifies':
                    chain['verified_by'].append(from_id)
        
        return chain
    
    def validate_traceability(self) -> list:
        """Validate all artifacts have required traceability."""
        issues = []
        
        for artifact_id, artifact in self.artifacts.items():
            if artifact['type'] == 'requirement':
                # Requirements should link to evidence
                if not artifact.get('evidence_refs'):
                    issues.append(f"{artifact_id}: No evidence linked")
            
            elif artifact['type'] == 'spec':
                # Specs should link to requirements
                if not artifact.get('requirement_refs'):
                    issues.append(f"{artifact_id}: No requirements linked")
            
            elif artifact['type'] == 'test':
                # Tests should link to specs
                if not artifact.get('spec_refs'):
                    issues.append(f"{artifact_id}: No specs linked")
        
        return issues
```

### Ledger Management

```python
class RequirementLedger:
    """Manages requirement traceability ledger."""
    
    def __init__(self):
        self.entries = []
    
    def add_entry(self, req_id: str, evidence_ids: list,
                  spec_ids: list, test_ids: list, status: str):
        """Add or update a ledger entry."""
        entry = {
            'req_id': req_id,
            'evidence_ids': evidence_ids,
            'spec_ids': spec_ids,
            'test_ids': test_ids,
            'status': status,
            'updated': datetime.utcnow().isoformat()
        }
        
        # Update existing or add new
        for i, existing in enumerate(self.entries):
            if existing['req_id'] == req_id:
                self.entries[i] = entry
                return
        self.entries.append(entry)
    
    def get_coverage_report(self) -> dict:
        """Generate coverage report."""
        total = len(self.entries)
        with_specs = sum(1 for e in self.entries if e['spec_ids'])
        with_tests = sum(1 for e in self.entries if e['test_ids'])
        
        return {
            'total_requirements': total,
            'with_specifications': with_specs,
            'with_tests': with_tests,
            'spec_coverage': with_specs / total if total else 0,
            'test_coverage': with_tests / total if total else 0
        }
    
    def to_markdown(self) -> str:
        """Export ledger as markdown table."""
        lines = [
            "| REQ ID | Evidence | Specs | Tests | Status |",
            "|--------|----------|-------|-------|--------|"
        ]
        
        for entry in self.entries:
            lines.append(
                f"| {entry['req_id']} | "
                f"{', '.join(entry['evidence_ids'])} | "
                f"{', '.join(entry['spec_ids'])} | "
                f"{', '.join(entry['test_ids'])} | "
                f"{entry['status']} |"
            )
        
        return "\n".join(lines)
```

### Integration Example

```python
class RJWIDDTemplateAgent:
    """Agent with integrated template management."""
    
    def __init__(self, project_root: str, templates_dir: str):
        self.template_mgr = TemplateManager(templates_dir)
        self.traceability = TraceabilityManager()
        self.ledger = RequirementLedger()
        self.project_root = Path(project_root)
    
    def process_evidence_to_requirement(self, evidence: dict) -> dict:
        """Convert curated evidence into a requirement."""
        # Create requirement from evidence
        req = self.template_mgr.instantiate_requirement(
            description=f"Implement capability based on {evidence['evd_id']}",
            acceptance_criteria=evidence.get('implications', []),
            evidence_refs=[evidence['evd_id']]
        )
        
        # Register for traceability
        self.traceability.register_artifact(req)
        
        # Update ledger
        self.ledger.add_entry(
            req_id=req['id'],
            evidence_ids=[evidence['evd_id']],
            spec_ids=[],
            test_ids=[],
            status='drafted'
        )
        
        # Save to project
        self._save_artifact(req, 'requirements')
        
        return req
    
    def create_spec_for_requirements(self, req_ids: list, 
                                     design: str) -> dict:
        """Create specification addressing requirements."""
        spec = self.template_mgr.instantiate_spec(
            title=f"Specification for {', '.join(req_ids)}",
            requirements=req_ids,
            design=design
        )
        
        self.traceability.register_artifact(spec)
        
        # Update ledger entries
        for req_id in req_ids:
            for entry in self.ledger.entries:
                if entry['req_id'] == req_id:
                    entry['spec_ids'].append(spec['id'])
                    entry['status'] = 'specified'
        
        self._save_artifact(spec, 'specs')
        
        return spec
    
    def _save_artifact(self, artifact: dict, category: str):
        """Save artifact to project directory."""
        path = self.project_root / category / f"{artifact['id']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(artifact['content'])
```

## Related Documentation

- Core Method: `core/METHOD-0001-core-method.md`
- Unified Lifecycle & Checklists: `governance/METHOD-0002-phase-driver-checklists.md`
- Role Handbook: `governance/METHOD-0003-role-handbook.md`
- Unified Agent Handbook: `operations/METHOD-0004-ai-agent-workflows.md`
- Operations Support: `operations/METHOD-0005-operations-production-support.md`
- Context Curation Engine: `operations/METHOD-0006-context-curation-engine.md`
